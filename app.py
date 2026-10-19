from flask import Flask, render_template, request, jsonify, Response
import csv
import io

try:
    import ai_model
except ImportError:
    ai_model = None

app = Flask(__name__)

# Initial sample dataset with unique IDs and confidence scores
complaints_db = [
    {
        "id": "GRM-1001",
        "village": "Rampur",
        "category": "Water Supply & Sanitation",
        "department": "Rural Water Supply & Sanitation Dept",
        "complaint": "Main drinking water pipeline leak near primary school.",
        "priority": "Critical",
        "confidence": 95,
        "status": "Pending"
    },
    {
        "id": "GRM-1002",
        "village": "Chandanpur",
        "category": "Electricity & Power",
        "department": "State Electricity Distribution Board",
        "complaint": "Transformer spark and power outage in Ward 3.",
        "priority": "High",
        "confidence": 88,
        "status": "In Progress"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() or request.form
        email = (data.get('email') or data.get('username') or '').strip().lower()
        password = (data.get('password') or '').strip()
        role = data.get('role', 'officer')

        if role == 'mla':
            if email == 'admin@gramguard.gov.in' and password == 'admin1234':
                return jsonify({'success': True, 'role': 'mla'})
            return jsonify({'success': False, 'message': 'Invalid MLA Email or Password'}), 401

        valid_officers = ['officer@gramguard.gov.in', 'admin@gramguard.gov.in', 'admin']
        if email in valid_officers and password == 'admin123':
            return jsonify({'success': True, 'role': 'officer'})
        
        return jsonify({'success': False, 'message': 'Invalid Officer Email or Password'}), 401

    return render_template('login.html')

@app.route('/api/complaints', methods=['GET', 'POST'])
def handle_complaints():
    if request.method == 'POST':
        data = request.get_json() or {}
        village = data.get('village', '').strip()
        user_category = data.get('category', '').strip()
        complaint_text = data.get('complaint', '').strip()

        if not village or not complaint_text:
            return jsonify({'success': False, 'message': 'Village and complaint details are required'}), 400

        pred_category, priority, department, confidence = "General", "Medium", "Panchayat Raj", 70
        if ai_model and hasattr(ai_model, 'predict'):
            try:
                pred_category, priority, department, confidence = ai_model.predict(complaint_text)
            except Exception as e:
                print(f"AI Model Execution Warning: {e}")

        final_category = user_category if (user_category and user_category != 'Auto-Detect') else pred_category

        # Generate unique ID (GRM-1003, GRM-1004, ...)
        last_num = int(complaints_db[-1]['id'].split('-')[1]) if complaints_db else 1000
        new_id = f"GRM-{last_num + 1}"

        new_complaint = {
            "id": new_id,
            "village": village,
            "category": final_category,
            "department": department,
            "complaint": complaint_text,
            "priority": priority,
            "confidence": confidence,
            "status": "Pending"
        }

        complaints_db.append(new_complaint)
        return jsonify({'success': True, 'message': 'Grievance registered successfully', 'data': new_complaint}), 201

    return jsonify(complaints_db)

@app.route('/api/complaints/track/<string:complaint_id>', methods=['GET'])
def track_complaint(complaint_id):
    clean_id = complaint_id.strip().upper()
    if not clean_id.startswith('GRM-') and clean_id.isdigit():
        clean_id = f"GRM-{clean_id}"

    for item in complaints_db:
        if item['id'] == clean_id:
            is_unsolved = item.get('status') in ['Pending', 'In Progress']
            is_high_priority = item.get('priority') in ['Critical', 'High']

            if is_unsolved and is_high_priority:
                level = "MLA Level Oversight 🏛️ (High Priority Unresolved)"
                level_badge = "bg-Critical"
            else:
                level = "Officer Level Processing 🏢"
                level_badge = "bg-Low"

            return jsonify({
                'success': True,
                'complaint': item,
                'level': level,
                'level_badge': level_badge
            })

    return jsonify({'success': False, 'message': f'Complaint ID "{clean_id}" not found.'}), 404

@app.route('/api/mla/complaints', methods=['GET'])
def get_mla_complaints():
    filtered = [
        item for item in complaints_db 
        if item.get('priority') in ['Critical', 'High'] and item.get('status') != 'Resolved'
    ]
    return jsonify(filtered)

@app.route('/api/complaints/<string:complaint_id>/status', methods=['PUT'])
def update_status(complaint_id):
    data = request.get_json() or {}
    new_status = data.get('status')

    for item in complaints_db:
        if item['id'] == complaint_id:
            item['status'] = new_status
            return jsonify({'success': True, 'message': 'Status updated'})

    return jsonify({'success': False, 'message': 'Complaint ID not found'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total = len(complaints_db)
    urgent = sum(1 for c in complaints_db if c.get('priority') in ['Critical', 'High'] and c.get('status') != 'Resolved')
    resolved = sum(1 for c in complaints_db if c.get('status') == 'Resolved')
    duplicates = sum(1 for c in complaints_db if c.get('status') == 'Duplicate')

    return jsonify({
        'total': total,
        'high_priority': urgent,
        'resolved': resolved,
        'duplicates': duplicates
    })

@app.route('/api/complaints/export', methods=['GET'])
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Village', 'Category', 'Department', 'Complaint Details', 'Priority', 'AI Confidence', 'Status'])

    for c in complaints_db:
        writer.writerow([c['id'], c['village'], c['category'], c['department'], c['complaint'], c['priority'], f"{c.get('confidence', 70)}%", c['status']])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=gramguard_grievance_report.csv'}
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)