from flask import Flask, request, jsonify, render_template, Response
import csv
import io
from detector.core import load_data, process_login, get_recent_logs
from detector.models import init_db, Log

app = Flask(__name__)
# ... (rest of init)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    logs = get_recent_logs(user_id)
    return jsonify(logs)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to receive a new login event.
    Payload: { "user_id": "u1", "timestamp": "...", "ip": "...", "success": true/false }
    """
    data = request.json
    try:
        result = process_login(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    """
    Returns the current dataset for visualization.
    """
    # In a real app, this would query the DB. 
    # For now, we return simulated data from memory or DB.
    return jsonify({"message": "Not implemented yet"})

@app.route('/api/export', methods=['GET'])
def export_logs():
    """
    Export all logs to CSV.
    """
    # Fetch all logs (limit to 1000 for safety)
    logs = get_recent_logs(user_id=None, limit=1000)
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write Header
    writer.writerow(['Time', 'User ID', 'IP Address', 'Location', 'Status', 'Details'])
    
    # Write Rows
    for log in logs:
        writer.writerow([
            log['timestamp'],
            log['user_id'],
            log['ip_address'],
            log['location'],
            log['status'],
            log['details']
        ])
        
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=login_logs.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
