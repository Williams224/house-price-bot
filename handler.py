import json
import os
import sys
from bs4 import BeautifulSoup


here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


def hello(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        response = "Please /start, {}".format(first_name)

        if "start" in message:
            response = "Hello {}".format(first_name)

        if "house price" in message:
            response = requests.get("https://www.zoopla.co.uk/property/29-aldwell-close/wootton/northampton/nn4-6ax/16417240")
            soup = BeautifulSoup(response.text, "html.parser")
            for el in soup.findAll("p"):
                if "pdp-estimate__price ui-text-t3" in str(el) and "pcm" not in el.text:
                    price = el.text

            response = "Current estimated price = {}".format(price)

        else:
            response = "Send house price"

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)





    except Exception as e:
        print(e)

    return {"statusCode": 200}
