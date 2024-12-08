from datetime import datetime

# Validation functions
def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time_format(time_str):
    try:
        datetime.strptime(time_str, '%H:%M')
        return True
    except ValueError:
        return False

def validate_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

#Validate receipt
def validate_receipt(receipt):
    if not isinstance(receipt, dict):
        return False, "Receipt must be a JSON object"

    required_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
    missing_fields = [field for field in required_fields if field not in receipt]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    if not isinstance(receipt['retailer'], str):
        return False, "Retailer must be a string"

    if not validate_date_format(receipt['purchaseDate']):
        return False, "Invalid date format. Use YYYY-MM-DD"

    if not validate_time_format(receipt['purchaseTime']):
        return False, "Invalid time format. Use HH:MM"

    if not validate_float(receipt['total']):
        return False, "Total must be a valid number"

    if not isinstance(receipt['items'], list):
        return False, "Items must be a list"

    for idx, item in enumerate(receipt['items']):
        if not isinstance(item, dict):
            return False, f"Item {idx} must be an object"
        if 'shortDescription' not in item:
            return False, f"Item {idx} missing shortDescription"
        if 'price' not in item:
            return False, f"Item {idx} missing price"
        if not validate_float(item['price']):
            return False, f"Item {idx} has invalid price"

    return True, ""
