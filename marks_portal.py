import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ------------------------------------------------------------
# 1. SETTINGS
# ------------------------------------------------------------
USERS_FILE = "users.csv"    # stores username, password, role, name
MARKS_FILE = "marks.csv"    # stores marks of every student
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer"]
PASS_MARK = 40              # minimum marks needed in every subject

st.set_page_config(page_title="Student Marks Portal", page_icon="🎓")


# ------------------------------------------------------------
# 2. FILE FUNCTIONS (load and save data)
# ------------------------------------------------------------
def create_files_if_missing():
    """Creates users.csv and marks.csv with demo data on the first run."""
    if not os.path.exists(USERS_FILE):
        users = pd.DataFrame({
            "username": ["teacher", "aman", "simran", "rahul"],
            "password": ["teacher123", "aman123", "simran123", "rahul123"],
            "role":     ["teacher", "student", "student", "student"],
            "name":     ["Teacher", "Aman", "Simran", "Rahul"],
        })
        users.to_csv(USERS_FILE, index=False)

    if not os.path.exists(MARKS_FILE):
        marks = pd.DataFrame({
            "username":  ["aman", "simran", "rahul"],
            "Maths":     [78, 92, 45],
            "Physics":   [65, 88, 38],
            "Chemistry": [70, 85, 50],
            "English":   [82, 79, 60],
            "Computer":  [90, 95, 55],
        })
        marks.to_csv(MARKS_FILE, index=False)


def load_users():
    return pd.read_csv(USERS_FILE, dtype=str)       # dtype=str keeps passwords as text


def load_marks():
    marks = pd.read_csv(MARKS_FILE)
    marks["username"] = marks["username"].astype(str)
    return marks


def save_users(users):
    users.to_csv(USERS_FILE, index=False)


def save_marks(marks):
    marks.to_csv(MARKS_FILE, index=False)


# ------------------------------------------------------------
# 3. HELPER FUNCTIONS (calculations using NumPy)
# ------------------------------------------------------------
def add_result_columns(marks_df):
    """Adds Total, Average and Result columns to a marks table."""
    df = marks_df.copy()
    values = df[SUBJECTS].to_numpy()                      # NumPy array of marks
    df["Total"] = values.sum(axis=1)
    df["Average"] = values.mean(axis=1).round(2)
    df["Result"] = np.where(np.all(values >= PASS_MARK, axis=1), "PASS", "FAIL")
    return df


# ------------------------------------------------------------
# 4. LOGIN PAGE
# ------------------------------------------------------------
def login_page():
    st.title("🎓 Student Marks Portal")
    st.subheader("Please login")

    role = st.radio("Login as", ["Student", "Teacher"], horizontal=True)
    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()

        # find a row where username, password and role all match
        match = users[
            (users["username"] == username)
            & (users["password"] == password)
            & (users["role"] == role.lower())
        ]

        if match.empty:
            st.error("Wrong username, password or role. Please try again.")
        else:
            # remember the user (session_state survives page reruns)
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = role.lower()
            st.session_state["name"] = match.iloc[0]["name"]
            st.rerun()

    st.info("Demo → Teacher: teacher / teacher123   |   Student: aman / aman123")


# ------------------------------------------------------------
# 5. TEACHER PAGE
# ------------------------------------------------------------
def teacher_page():
    st.title("👩‍🏫 Teacher Dashboard")
    tab1, tab2, tab3 = st.tabs(["➕ Add / Update Marks", "🧑‍🎓 Add New Student", "📋 View All Marks"])

    users = load_users()
    students = users[users["role"] == "student"]

    # ---------- TAB 1: enter marks ----------
    with tab1:
        if students.empty:
            st.warning("No students yet. Add a student in the next tab.")
        else:
            # dropdown showing student names
            chosen_name = st.selectbox("Select student", students["name"].tolist())
            chosen_username = students[students["name"] == chosen_name].iloc[0]["username"]

            marks = load_marks()
            old = marks[marks["username"] == chosen_username]   # existing marks (if any)

            st.write("Enter marks (0 to 100):")
            new_marks = {}
            for subject in SUBJECTS:
                default = int(old.iloc[0][subject]) if not old.empty else 0
                new_marks[subject] = st.number_input(
                    subject, min_value=0, max_value=100, value=default,
                    key=f"{subject}_{chosen_username}",
                )

            if st.button("Save Marks"):
                marks = marks[marks["username"] != chosen_username]   # remove old row
                new_row = {"username": chosen_username, **new_marks}
                marks = pd.concat([marks, pd.DataFrame([new_row])], ignore_index=True)
                save_marks(marks)
                st.success(f"Marks saved for {chosen_name}!")

    # ---------- TAB 2: add a new student ----------
    with tab2:
        if "message" in st.session_state:
            st.success(st.session_state.pop("message"))   # show the message once

        new_name = st.text_input("Student full name")
        new_username = st.text_input("Username for login").strip().lower()
        new_password = st.text_input("Password for student", type="password")

        if st.button("Create Student"):
            if not new_name or not new_username or not new_password:
                st.error("Please fill all the fields.")
            elif new_username in users["username"].values:
                st.error("This username already exists. Choose another one.")
            else:
                new_user = pd.DataFrame([{
                    "username": new_username, "password": new_password,
                    "role": "student", "name": new_name,
                }])
                save_users(pd.concat([users, new_user], ignore_index=True))
                # save a message, then refresh the page so the new student
                # appears in the dropdown of the first tab
                st.session_state["message"] = f"Student '{new_name}' created! Now add their marks in the first tab."
                st.rerun()

    # ---------- TAB 3: view all marks ----------
    with tab3:
        marks = load_marks()
        if marks.empty:
            st.info("No marks have been entered yet.")
        else:
            # join marks with names so we can show names instead of usernames
            table = marks.merge(users[["username", "name"]], on="username", how="left")
            table = add_result_columns(table)
            show = table[["name"] + SUBJECTS + ["Total", "Average", "Result"]]
            show = show.rename(columns={"name": "Student"})
            st.dataframe(show, hide_index=True)

            # NumPy statistics
            all_values = table[SUBJECTS].to_numpy()
            col1, col2, col3 = st.columns(3)
            col1.metric("Class Average", f"{all_values.mean():.2f}")
            col2.metric("Topper", table.loc[table["Total"].idxmax(), "name"])
            pass_percent = (table["Result"] == "PASS").mean() * 100
            col3.metric("Pass %", f"{pass_percent:.0f}%")

            # Matplotlib chart: average marks of each subject
            fig, ax = plt.subplots()
            ax.bar(SUBJECTS, all_values.mean(axis=0), color="lightgreen")
            ax.set_title("Class Average per Subject")
            ax.set_ylabel("Average Marks")
            ax.set_ylim(0, 100)
            st.pyplot(fig)


# ------------------------------------------------------------
# 6. STUDENT PAGE
# ------------------------------------------------------------
def student_page():
    st.title(f"🧑‍🎓 Welcome, {st.session_state['name']}!")

    marks = load_marks()
    my_marks = marks[marks["username"] == st.session_state["username"]]   # ONLY my row

    if my_marks.empty:
        st.info("Your marks have not been added yet. Please check with your teacher.")
        return

    my_result = add_result_columns(my_marks).iloc[0]

    # table of my marks
    st.subheader("Your Marks")
    table = pd.DataFrame({"Subject": SUBJECTS, "Marks": [int(my_result[s]) for s in SUBJECTS]})
    st.dataframe(table, hide_index=True)

    # summary numbers
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", f"{my_result['Total']:.0f} / {len(SUBJECTS) * 100}")
    col2.metric("Average", f"{my_result['Average']:.2f}")
    col3.metric("Result", my_result["Result"])

    # chart: my marks vs class average
    st.subheader("Your Marks vs Class Average")
    my_values = my_marks[SUBJECTS].to_numpy()[0]
    class_avg = marks[SUBJECTS].to_numpy().mean(axis=0)

    x = np.arange(len(SUBJECTS))          # positions 0,1,2,3,4
    fig, ax = plt.subplots()
    ax.bar(x - 0.2, my_values, width=0.4, label="You", color="skyblue")
    ax.bar(x + 0.2, class_avg, width=0.4, label="Class average", color="lightgray")
    ax.axhline(PASS_MARK, color="red", linestyle="--", label="Pass mark")
    ax.set_xticks(x)
    ax.set_xticklabels(SUBJECTS)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Marks")
    ax.legend()
    st.pyplot(fig)


# ------------------------------------------------------------
# 7. MAIN PROGRAM
# ------------------------------------------------------------
def main():
    create_files_if_missing()

    # first time: nobody is logged in
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
        return

    # sidebar with logout button
    st.sidebar.write(f"Logged in as: **{st.session_state['name']}**")
    st.sidebar.write(f"Role: {st.session_state['role'].title()}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # show the correct page for the role
    if st.session_state["role"] == "teacher":
        teacher_page()
    else:
        student_page()


main()
