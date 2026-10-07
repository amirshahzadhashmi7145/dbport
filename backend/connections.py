from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

connections = []

@app.route('/connections', methods=['POST'])
def create_connection():
    data = request.json
    connection = {
        'id': len(connections),
        'name': data['name'],
        'dialect': data['dialect'],
        'host': data['host'],
        'port': data['port'],
        'database': data['database'],
        'mode': data['mode'],
        'introspection_status': data['introspection_status'],
        'created_at': datetime.utcnow().isoformat(),
        'status_url': f"/connections/{len(connections)}"
    }
    connections.append(connection)
    return jsonify(connection), 201
