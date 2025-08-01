from config import SUPPORT_TOPICS
from api_price import get_token_price


def get_truth(topic, token, block_height):
    # check if topic is supported
    if topic in SUPPORT_TOPICS:
        # check if topic is prediction topic
        if topic == "13":
            return get_token_price(token, block_height)
        else:
            print("This is topic reputer logic is not implemented yet.")
            return None
    else:
        print("This is topic is not supported")
        return None
