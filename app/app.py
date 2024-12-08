from flask import Flask, request, jsonify
import uuid
from validation import validate_receipt
from rules import calculate_points

app = Flask(__name__)

# In-memory storage
receipts = {}

# Endpoint: /receipts/process
@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    try:
        receipt = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON format"}), 400
    
    
    is_valid, error_message = validate_receipt(receipt)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = calculate_points(receipt)
    return jsonify({"id": receipt_id})

#Endpoint: /receipts/{id}/points
@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    if id not in receipts:
        return jsonify({"error": "Receipt not found"}), 404
    return jsonify({"points": receipts[id]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)