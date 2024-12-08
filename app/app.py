from flask import Flask, request, jsonify
import uuid
from datetime import datetime
from .exceptions import *
from .validation import validate_receipt
from .rules import calculate_points

app = Flask(__name__)
receipts = {}

@app.errorhandler(ReceiptProcessorError)
def handle_error(error):
    return jsonify({"error": error.message}), error.status_code

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    if not request.is_json:
        raise InvalidJSONError()

    try:
        receipt = request.get_json()
        if receipt is None:
            raise InvalidJSONError()

        is_valid, error_message = validate_receipt(receipt)
        if not is_valid:
            raise ValidationError(error_message)

        receipt_id = str(uuid.uuid4())
        receipts[receipt_id] = calculate_points(receipt)
        return jsonify({"id": receipt_id})
        
    except ReceiptProcessorError:
        raise
    except Exception as e:
        raise ValidationError(str(e))

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    if id not in receipts:
        raise ReceiptNotFoundError()
    return jsonify({"points": receipts[id]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)