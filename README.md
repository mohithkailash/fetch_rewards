# Receipt Processor

A REST API service that processes receipts and calculates reward points based on specific rules.

## Features

- Process receipts and calculate points based on:
  - Retailer name alphanumeric characters
  - Round dollar amounts
  - Multiples of 0.25
  - Item counts
  - Item description lengths
  - Purchase time and date
- Validation for all input fields
- Error handling with descriptive messages
- In-memory storage for receipt data

## Technology Stack

- Python 3.9
- Flask 3.0.3
- Docker

## Installation

### Local Setup

1. Clone the repository

```bash
git clone https://github.com/mohithkailash/fetch_rewards.git
cd fetch_rewards
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
python app/app.py
```

### Docker Setup

1. Build the Docker image

```bash
docker build -t receipt-processor .
```

2. Run the container

```bash
docker run -p 7000:7000 receipt-processor
```

## API Documentation

### Process Receipt

This application is available at http://127.0.0.1:7000

`POST /receipts/process`

Processes a receipt and returns an ID for points calculation.

#### Request Body

```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },
    {
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },
    {
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },
    {
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },
    {
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}
```

#### Response

```json
{
  "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```

![image](https://github.com/user-attachments/assets/2e0bd6f1-4275-4054-bf33-e1991818805d)


### Get Points

`GET /receipts/{id}/points`

Returns the points awarded for a receipt.

#### Response

```json
{
  "points": 28
}
```
![image](https://github.com/user-attachments/assets/536dc4e1-1904-4718-8f0e-d2fd556960ff)


## Error Handling

- Invalid JSON format: 400 Bad Request
- Missing required fields: 400 Bad Request
- Invalid data types: 400 Bad Request
- Receipt not found: 404 Not Found
- Invalid content type: 415 Unsupported Media Type

## Project Structure

```
FETCH_BACKEND/
├── app/
│   ├── app.py           # Application configuration and server
│   ├── validation.py    # Input validation functions
│   ├── calculations.py  # Points calculation logic
│   ├── exceptions.py    # Custom exceptions
│   └── tests/
│       └── test.py      # Unit and integration tests
├── Dockerfile          # Docker configuration
└── requirements.txt    # Python dependencies
```

## Testing

Run the test suite:

```bash
docker run receipt-processor sh -c "python -m unittest tests/test.py -v"
```

The test suite includes:

- Unit tests for each calculation rule
- Input validation tests
- API endpoint integration tests
- Error handling tests

## Points Calculation Rules

1. One point for every alphanumeric character in the retailer name
2. 50 points if the total is a round dollar amount
3. 25 points if the total is a multiple of 0.25
4. 5 points for every two items
5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned
6. 6 points if the day in the purchase date is odd
7. 10 points if the time of purchase is between 2:00pm and 4:00pm

## Future Improvements

- Persistent storage including Data models or DTOs
- API authentication
- Rate limiting
- Response caching
- Swagger/OpenAPI documentation
