import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st
import os
import re

# ------------------ CONFIG ------------------
SERVICE_ACCOUNT_FILE = "service_account.json"
SPREADSHEET_ID = "1scuHemqjks2nomaRlLAl6UH1BZjM5RXHioexDUwkGpc"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ AUTH ------------------
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

gc = gspread.authorize(credentials)
worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1

# ------------------ HELPERS ------------------
def roll_to_number(roll):
    return int(re.search(r"\d+$", roll).group())

def valid_roll(roll):
    return re.match(r"2024PECAI([1-5]\d\d|600)$", roll)

def teacher_range(teacher_id):
    index = int(teacher_id[1:]) - 1
    start = 101 + index * 35
    end = start + 34
    return start, end

# ------------------ UI ------------------
st.set_page_config("CMS", layout="wide")
st.title("📜 Certificate Management System")

role = st.radio("Login as", ["Student", "Teacher"], horizontal=True)

# =========================================================
# 🎓 STUDENT PANEL
# =========================================================
if role == "Student":
    st.subheader("🎓 Student Certificate Upload (Max 30 PDFs)")

    student_name = st.text_input("Student Name")
    roll_no = st.text_input("Roll Number (2024PECAI101 - 2024PECAI600)")
    cert_name = st.text_input("Certificate Category (Workshop / Course / Event)")

    uploaded_files = st.file_uploader(
        "Upload Certificate PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Submit Certificates"):
        if not student_name or not roll_no or not cert_name:
            st.error("Fill all fields")
        elif not valid_roll(roll_no):
            st.error("Invalid Roll Number")
        elif not uploaded_files:
            st.error("Upload at least one PDF")
        elif len(uploaded_files) > 30:
            st.error("Maximum 30 PDFs allowed")
        else:
            roll_num = roll_to_number(roll_no)

            student_folder = os.path.join(UPLOAD_FOLDER, roll_no)
            os.makedirs(student_folder, exist_ok=True)

            for file in uploaded_files:
                file_name = file.name
                file_path = os.path.join(student_folder, file_name)

                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

                worksheet.append_row([
                    student_name,
                    roll_no,
                    roll_num,
                    cert_name,
                    f"{roll_no}/{file_name}"
                ])

            st.success(f"✅ {len(uploaded_files)} certificates uploaded successfully")

# =========================================================
# 👩‍🏫 TEACHER PANEL
# =========================================================
if role == "Teacher":
    st.subheader("👩‍🏫 Teacher Login")

    teacher_name = st.text_input("Teacher Name")
    teacher_id = st.text_input("Teacher ID (A1, A2...)")

    if st.button("Login"):
        if not re.match(r"A\d+", teacher_id):
            st.error("Invalid Teacher ID")
        else:
            st.session_state.teacher_id = teacher_id
            st.success("Login successful")

    if "teacher_id" in st.session_state:
        start_roll, end_roll = teacher_range(st.session_state.teacher_id)

        st.info(
            f"Allotted Students: "
            f"2024PECAI{start_roll} → 2024PECAI{end_roll}"
        )

        data = worksheet.get_all_records()
        df = pd.DataFrame(data)

        if df.empty:
            st.warning("No certificates uploaded yet")
        else:
            df["RollNum"] = df["RollNum"].astype(int)

            filtered = df[
                (df["RollNum"] >= start_roll) &
                (df["RollNum"] <= end_roll)
            ]

            if filtered.empty:
                st.warning("No certificates for your students")
            else:
                st.subheader("📂 Student Certificates")

                for roll, group in filtered.groupby("Roll No"):
                    st.markdown(f"## 🎓 {roll}")

                    for idx, row in group.iterrows():
                        pdf_path = os.path.join(
                            UPLOAD_FOLDER,
                            row["PDF File Name"]
                        )

                        st.write(f"📜 {row['Certificate Name']}")

                        if os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as f:
                                # Add unique key using roll and index
                                st.download_button(
                                    "⬇ Download",
                                    f,
                                    file_name=os.path.basename(pdf_path),
                                    mime="application/pdf",
                                    key=f"{row['Roll No']}_{idx}"
                                )
                        else:
                            st.error("PDF missing")

                    st.divider()
