import time
from datetime import datetime, timezone, timedelta
import logging
import requests
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List of your API keys
api_keys_coingecko = [
    "Your coingecko api key",
    "Your coingecko api key"
]


def parse_timestamp(timestamp_str):
    try:
        # If the timestamp has nanosecond precision, trim it to microseconds (6 digits)
        if '.' in timestamp_str:
            timestamp_str = timestamp_str[:timestamp_str.index('Z')]  # Remove 'Z' temporarily
            timestamp_str = timestamp_str[:26] + 'Z'  # Keep up to 6 digits of microseconds and append 'Z'

        # Format with or without fractional seconds (now only up to microseconds)
        timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

        # Convert to Unix timestamp
        unix_timestamp = int(timestamp_dt.timestamp())
        return unix_timestamp

    except ValueError as e:
        print(f"Error parsing timestamp: {e}")
        return None


def get_block_timestamp(height, max_retries=4, backoff_factor=1):
    url = f"https://allora-rpc.testnet.allora.network/block?height={height}"
    retries = 0

    while retries < max_retries:
        try:
            # Sending GET request to the API
            response = requests.get(url)
            response.raise_for_status()  # Raises an error if the request fails

            # Parsing the JSON response
            data = response.json()

            # Extracting the block timestamp as a string
            timestamp_str = data['result']['block']['header']['time']

            # Parse the timestamp into a Unix timestamp
            unix_timestamp = parse_timestamp(timestamp_str)

            if unix_timestamp is not None:
                return unix_timestamp

        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"Attempt {retries}/{max_retries} failed with error: {e}")

            if retries >= max_retries:
                print("Max retries exceeded")
                return None

            # Exponential backoff before the next retry
            time.sleep(backoff_factor * (2 ** retries))

    return None


def get_token_price_history(symbol, end_time):
    base_url = "https://api.coingecko.com/api/v3/coins/"

    selected_key = random.choice(api_keys_coingecko)
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": selected_key
    }

    # Ensure end_time is an integer Unix timestamp
    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        end_time = int(end_time.timestamp())

    # Calculate from_time (15 minutes before end_time)
    from_time = end_time - 15 * 60
    end_time = end_time + 2 * 60  # Adding 2 minutes for safety

    url = f"{base_url}{symbol}/market_chart/range?vs_currency=usd&from={from_time}&to={end_time}"
    logging.info(f"Fetching token price history from: {url}")

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        # Get the last price and timestamp
        last_price = data['prices'][-1][1]
        timestamp = data['prices'][-1][0]

        return last_price, timestamp
    else:
        logging.error(f"Failed to fetch price history: HTTP {response.status_code}")
        raise ValueError("Unsupported token")


def get_token_price(token, block_number):

    # Normalize the token name by converting to lower case
    token = token.lower()

    for attempt in range(3):
        try:
            block_timestamp = get_block_timestamp(block_number)

            # If a block timestamp was retrieved, fetch and log the token price
            if block_timestamp:
                # Use timezone-aware UTC datetime
                readable_block_timestamp = datetime.fromtimestamp(block_timestamp, timezone.utc).strftime(
                    '%Y-%m-%d %H:%M:%S UTC')

                price, data_timestamp = get_token_price_history(token, block_timestamp)

                # Convert data_timestamp to UTC-aware datetime
                readable_data_timestamp = datetime.fromtimestamp(data_timestamp / 1000, timezone.utc).strftime(
                    '%Y-%m-%d %H:%M:%S UTC')

                logging.info(f"Requested the price of {token.upper()} at block time: {readable_block_timestamp}")
                logging.info(f"Price of {token.upper()} : {price} USD at data time: {readable_data_timestamp}")

                return price
            else:
                logging.error(f"Attempt {attempt + 1}: Failed to get block timestamp.")

        except Exception as e:
            logging.error(f"Attempt {attempt + 1}: Error occurred - {str(e)}")

        # Wait 0.5 seconds before the next attempt
        time.sleep(0.5)

    # If all retries fail
    logging.error("Failed to get block timestamp after 3 retries.")
    return None

