from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import qrcode
import csv
import os
import io
import pandas as pd
from PIL import Image
import base64

app = Flask(__name__)

# Configuration
CSV_FILE = 'students.csv'  # CSV with columns: id,name,photo_path
PRESENT_FILE = 'present.txt'  # Temporary storage for present student IDs
QR_CODES_DIR = 'qrcodes'  # Directory for QR code images
HOST_IP = '0.0.0.0'  # Update to your local IP for LAN access
PORT = 5000
BASE_URL = f'http://{HOST_IP}:{PORT}'

# Ensure directories exist
if not os.path.exists(PRESENT_FILE):
    open(PRESENT_FILE, 'w').close()
if not os.path.exists(QR_CODES_DIR):
    os.makedirs(QR_CODES_DIR)
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'photo_path'])


# Load students from CSV
def load_students():
    students = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students[row['id']] = {'name': row['name'], 'photo_path': row['photo_path']}
    return students


# Save present student
def save_present_student(student_id):
    with open(PRESENT_FILE, 'a') as f:
        f.write(student_id + '\n')


# Get present students
def get_present_students():
    present = set()
    if os.path.exists(PRESENT_FILE):
        with open(PRESENT_FILE, 'r') as f:
            present = set(line.strip() for line in f if line.strip())
    return present


# Generate QR code for a student ID
def generate_qr_code(student_id):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(student_id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_path = os.path.join(QR_CODES_DIR, f'{student_id}.png')
    img.save(qr_path)
    return qr_path


# Generate QR code for mobile page
def generate_mobile_qr_code():
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f'{BASE_URL}/mobile')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


@app.route('/')
def admin():
    qr_code = generate_mobile_qr_code()
    students = load_students()
    present_ids = get_present_students()
    present_students = [
        {'id': sid, 'name': students[sid]['name'], 'photo_path': students[sid]['photo_path']}
        for sid in present_ids if sid in students
    ]
    return render_template('admin.html', qr_code=qr_code, present_students=present_students)


@app.route('/mobile')
def mobile():
    return render_template('mobile.html')


@app.route('/create_qrcode', methods=['GET', 'POST'])
def create_qrcode():
    if request.method == 'POST':
        student_id = request.form.get('id')
        name = request.form.get('name')
        photo_path = request.form.get('photo_path')

        # Validate inputs
        if not student_id or not name or not photo_path:
            return render_template('create_qrcode.html', error="All fields are required")

        # Check if ID already exists
        students = load_students()
        if student_id in students:
            return render_template('create_qrcode.html', error="Student ID already exists")

        # Append to CSV
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([student_id, name, photo_path])

        # Generate QR code
        generate_qr_code(student_id)

        return render_template('create_qrcode.html', success=f"QR code generated for {name} (ID: {student_id})")

    return render_template('create_qrcode.html')


@app.route('/get_student/<student_id>')
def get_student(student_id):
    students = load_students()
    if student_id in students:
        student = students[student_id]
        # Convert photo to base64
        try:
            with open(student['photo_path'], 'rb') as f:
                photo_data = base64.b64encode(f.read()).decode()
            return jsonify({
                'id': student_id,
                'name': student['name'],
                'photo': photo_data
            })
        except:
            return jsonify({'error': 'Photo not found'}), 404
    return jsonify({'error': 'Student not found'}), 404


@app.route('/mark_present/<student_id>', methods=['POST'])
def mark_present(student_id):
    students = load_students()
    if student_id in students:
        save_present_student(student_id)
        return jsonify({'success': True})
    return jsonify({'error': 'Student not found'}), 404


@app.route('/export_excel')
def export_excel():
    students = load_students()
    present_ids = get_present_students()

    data = []
    for sid, info in students.items():
        status = 'Present' if sid in present_ids else 'Absent'
        data.append({'ID': sid, 'Name': info['name'], 'Status': status})

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')
    output.seek(0)

    return send_file(
        output,
        download_name='attendance.xlsx',
        as_attachment=True,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if __name__ == '__main__':
    app.run(host=HOST_IP, port=PORT, debug=False)