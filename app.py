from flask import Flask, render_template, request, jsonify, send_file, redirect
import pandas as pd

app = Flask(__name__)
attendance = {}

# Load people from Excel
people = pd.read_excel('people.xlsx')

# Initialize attendance
for idx, row in people.iterrows():
    attendance[str(row['ID'])] = {
        'name': row['Name'],
        'photo': row['Photo'],
        'present': False
    }

@app.route('/')
def admin():
    present_list = [info for id, info in attendance.items() if info['present']]
    return render_template('admin.html', present=present_list)

@app.route('/scanner')
def scanner():
    return render_template('scan.html')

@app.route('/mark_present', methods=['POST'])
def mark_present():
    data = request.get_json()
    student_id = data.get('id')
    if student_id in attendance:
        return jsonify({
            'status': 'success',
            'name': attendance[student_id]['name'],
            'photo': '/' + attendance[student_id]['photo'],
            'number': student_id
        })
    else:
        return jsonify({'status': 'error', 'message': 'ID not found'})

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    data = request.get_json()
    student_id = data.get('id')
    if student_id in attendance:
        attendance[student_id]['present'] = True
        return jsonify({'status': 'marked'})
    else:
        return jsonify({'status': 'error', 'message': 'ID not found'})

@app.route('/download')
def download():
    df = pd.DataFrame([
        {'ID': id, 'Name': info['name'], 'Present': info['present']}
        for id, info in attendance.items()
    ])
    df.to_excel('attendance_result.xlsx', index=False)
    return send_file('attendance_result.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
