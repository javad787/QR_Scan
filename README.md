---

# 📚 QR Code Attendance System (Local Web App)

This project is a **local web application** for managing **student attendance** using **QR code scanning**.  
It allows scanning QR codes through a **mobile device**, confirming the student's identity with a **photo popup**, and recording attendance in **Excel format**.

---

## ✨ Features

- **Admin Panel (Desktop):**
  - View live list of present students.
  - Link for mobile devices to open the scanner.
  - Download attendance record in Excel.

- **Mobile Scanner (Phone):**
  - Access scanner page from phone browser.
  - Camera scanning of QR codes.
  - Student **photo**, **name**, and **ID** pop up after scanning.
  - Confirm or cancel attendance marking.

- **Attendance Management:**
  - Attendance status stored in memory.
  - Export final present/absent list into an Excel file.

---

## 🛠️ Tech Stack

- Python 3.x
- Flask
- Pandas
- HTML5 + JavaScript
- [html5-qrcode](https://github.com/mebjas/html5-qrcode) for camera scanning

---

## 📂 Project Structure

```
attendance_app/
├── app.py               # Main Flask server
├── people.xlsx          # List of students (ID, Name, Photo Path)
├── static/
│   ├── html5-qrcode.min.js
│   └── photos/           # Folder with student photos
├── templates/
│   ├── admin.html        # Admin panel
│   └── scan.html         # Mobile scanner page
└── README.md             # Project documentation
```

---

## 📋 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/qr-code-attendance.git
cd qr-code-attendance
```

### 2. Install required Python packages
```bash
pip install flask pandas openpyxl
```

### 3. Prepare your student list
- Edit `people.xlsx` file:
  - `ID`: Unique student number
  - `Name`: Student name
  - `Photo`: Path to student photo (e.g., `static/photos/john.jpg`)

### 4. Place student photos
- Store all student photos inside `static/photos/`.

### 5. Run the server
```bash
python app.py
```

The server will start at `http://localhost:5000`.

### 6. Open the Admin Panel
- On your **laptop**, visit: `http://localhost:5000`
- On your **mobile device** (connected to same WiFi):
  - Open: `http://<your-laptop-ip>:5000/scanner`
    - Example: `http://192.168.1.5:5000/scanner`

---

## 📷 Usage Workflow

1. Open the scanner page on your phone.
2. Scan a student's QR code (the QR code value must be the student's ID).
3. A popup will show:
   - Student photo
   - Student name
   - Student ID
4. Press **Submit** to mark as present, or **Cancel** to ignore.
5. On the Admin Panel, you will see the list of present students.
6. After finishing the session, download the **attendance Excel** report.

---

## 📈 Future Improvements

- Add admin login security.
- Allow generating QR codes for students automatically.
- Add face recognition (optional future version).
- Persistent database storage (SQLite/MySQL).

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## ✍️ Author

Built with ❤️ by [Javad78702]

---
