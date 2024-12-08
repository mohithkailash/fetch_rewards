from datetime import datetime
import math

# Rule 1
def get_retailer_points(retailer):
    return sum(c.isalnum() for c in retailer)

# Rule 2
def get_round_dollar_points(total):
    return 50 if float(total).is_integer() else 0

# Rule 3
def get_multiple_of_quarter_points(total):
    return 25 if float(total) % 0.25 == 0 else 0

# Rule 4
def get_items_pairs_points(items):
    return (len(items) // 2) * 5

# Rule 5
def get_description_length_points(items):
    points = 0
    for item in items:
        desc_length = len(item['shortDescription'].strip())
        if desc_length % 3 == 0:
            points += math.ceil(float(item['price']) * 0.2)
    return points

# Rule 6
def get_odd_day_points(purchase_date):
    date = datetime.strptime(purchase_date, '%Y-%m-%d')
    return 6 if date.day % 2 == 1 else 0

# Rule 7
def get_time_range_points(purchase_time):
    time = datetime.strptime(purchase_time, '%H:%M').time()
    if datetime.strptime('14:00', '%H:%M').time() <= time <= datetime.strptime('16:00', '%H:%M').time():
        return 10
    return 0

# Calculate points based on above rules
def calculate_points(receipt):
    points = 0
    points += get_retailer_points(receipt['retailer'])
    points += get_round_dollar_points(receipt['total'])
    points += get_multiple_of_quarter_points(receipt['total'])
    points += get_items_pairs_points(receipt['items'])
    points += get_description_length_points(receipt['items'])
    points += get_odd_day_points(receipt['purchaseDate'])
    points += get_time_range_points(receipt['purchaseTime'])
    return points
