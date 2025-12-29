# 📜 Certificate Management System (CMS)

A web-based Certificate Management System built using **Streamlit** to streamline the process of student certificate submission and faculty access. Students can upload certificates in PDF format, and teachers can view and download certificates for their assigned students.

---

## 🛠 Features

### 👩‍🎓 Student Panel
- Upload multiple PDF certificates (maximum 30 files)
- Select certificate category (Workshop / Course / Event)
- Roll number validation  
  *(Example: 2024PECAI101 → 2024PECAI600)*
- Certificates stored in a structured folder format by roll number
- Automatic logging of uploads into a Google Sheet

---

### 👨‍🏫 Teacher Panel
- Teacher login using ID (A1, A2, …)
- View students allocated to the logged-in teacher
- Download certificates of assigned students
- View certificate names and download status

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2️⃣ Create Virtual Environment (Windows)

```bash
python -m venv venv
venv\Scripts\activate
```
### 3️⃣ Install Dependencies

```bash
pip install streamlit gspread pandas google-auth
```
### 4️⃣ Google API Setup

1. Go to **Google Cloud Console**
2. Create a new project or select an existing one
3. Enable the **Google Sheets API**
4. Create a **Service Account**
5. Download the service account JSON key
6. Place the JSON file in the project root directory as:service_account.json
### 5️⃣ Configure Project

- In the code, set your Google Sheet ID:
```bash
SPREADSHEET_ID = "your-google-sheet-id"
```
- The application will automatically create an uploads/ folder to store uploaded PDF certificates.
### 6️⃣ Run the Streamlit Application
```bash
streamlit run web.py
```
