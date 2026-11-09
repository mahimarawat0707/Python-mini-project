# 🎓 Student Marks Portal

A beginner-friendly web app built with **Python** and **Streamlit** where teachers manage student marks and students view only their own results, with charts.

> Mini project for **Python Programming (24CAH301)**, BCA, Chandigarh University.

---

## ✨ Features

### 👩‍🏫 Teacher login
- Create new student accounts
- Enter or update marks for 5 subjects
- View the whole class table (total, average, PASS/FAIL)
- See class average, topper, pass percentage and a subject-wise chart

### 🧑‍🎓 Student login
- See **only their own** marks
- View total, average and PASS/FAIL result
- Compare personal marks with the class average and the pass mark in a chart

### 🔐 Access control
- Login checks username, password **and** role together
- A student cannot open the teacher dashboard
- Data is saved permanently in CSV files

---

## 🛠️ Tech Stack

| Library | Used for |
|---|---|
| **Streamlit** | Web interface (login form, tabs, tables, buttons) |
| **Pandas** | Reading/writing CSV files, filtering and merging data |
| **NumPy** | Total, average, class statistics and pass/fail checks |
| **Matplotlib** | Bar charts |

---

## 📁 Project Structure

```
student-marks-portal/
├── marks_portal.py     # Main application (all the code)
├── requirements.txt    # Libraries needed
├── README.md           # This file
├── users.csv           # Auto-created: usernames, passwords, roles
└── marks.csv           # Auto-created: marks of every student
```

`users.csv` and `marks.csv` are created automatically with demo data the first time you run the app.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/mahimarawat0707/student-marks-portal.git
cd student-marks-portal
```

### 2. Install the libraries
```bash
pip install -r requirements.txt
```
On Windows you can also use `py -m pip install -r requirements.txt`.

### 3. Run the app
```bash
streamlit run marks_portal.py
```
On Windows, if `streamlit` is not recognised, use:
```bash
py -m streamlit run marks_portal.py
```

The app opens in your browser at **http://localhost:8501**.

> ⚠️ Run it with `streamlit run`, not `python marks_portal.py`, otherwise you will only see warnings in the terminal.

---

## 🔑 Demo Logins

| Role | Username | Password |
|---|---|---|
| Teacher | `teacher` | `teacher123` |
| Student | `aman` | `aman123` |
| Student | `simran` | `simran123` |
| Student | `rahul` | `rahul123` |

Choose the matching **Student / Teacher** option on the login page.

---

## ⚙️ How It Works

1. `main()` creates the CSV files if they are missing.
2. If nobody is logged in, the login page is shown.
3. On login, the user's details are stored in `st.session_state`.
4. The role decides which page opens: `teacher_page()` or `student_page()`.
5. The student page filters `marks.csv` by the logged-in username, so a student only ever sees their own row.
6. Logout clears the session and returns to the login page.

### Data files

**users.csv**

| username | password | role | name |
|---|---|---|---|
| aman | aman123 | student | Aman |

**marks.csv**

| username | Maths | Physics | Chemistry | English | Computer |
|---|---|---|---|---|---|
| aman | 78 | 65 | 70 | 82 | 90 |

A student **passes** only if they score at least **40 in every subject** (change `PASS_MARK` at the top of the code).

---

## 🧪 Tested Scenarios

- Correct and wrong login, and role mismatch
- Creating a student (empty fields and duplicate username are rejected)
- Saving and updating marks without duplicate rows
- Student sees only their own marks
- Student with no marks yet sees an information message
- Logout returns to the login page

---

## ⚠️ Limitations

- Passwords are stored as **plain text**, fine for learning but not for a real website
- CSV files are used instead of a database
- No forgot-password or change-password option
- Two teachers saving at the same moment may overwrite each other

## 🔮 Future Improvements

- [ ] Hash passwords with `hashlib`
- [ ] Use SQLite or MySQL instead of CSV files
- [ ] Change-password option and an admin role
- [ ] Grades, semester-wise marks and PDF report cards
- [ ] Deploy online with Streamlit Community Cloud

---

## 👩‍💻 Author

**Kumari Mahima**
UID: 24BCA10111 | Class: 24BCA5A
Bachelor of Computer Applications, Chandigarh University
Guided by: **Mr. Sujeet Kumar**

---

## 📄 License

This project is for educational purposes. Feel free to learn from it and improve it.
