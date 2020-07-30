import requests as requests
import random

url = "https://api.telegram.org/bot1306743577:AAFN6ckiseuRbtjtFgJA2fumYC8OHv_EFHA/"


# func that get user id
def get_chat_id(update):
    chat_id = update["message"]["chat"]["id"]
    return chat_id


# func that get message text
def get_text(update):
    text = update["message"]["text"]
    return text


# func that gets the last update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]  # get the last recorded message


# func that sends msg to the usr
def send_msg(chat_id, msg_text):
    params = {"chat_id": chat_id, "text": msg_text}
    response = requests.post(url + "sendMessage", data=params)
    return response


# the main func
def main():
    update_id = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        if update_id == update["update_id"]:
            if get_text(update).lower() == "hi" or get_text(update).lower() == "hello":
                my_msg = "Hello Welcome to our bot. Type 'Play' to roll the dice."
                send_msg(get_chat_id(update), my_msg)
            elif get_text(update).lower() == "play":
                _1 = random.randint(1, 6)
                _2 = random.randint(1, 6)
                _3 = random.randint(1, 6)
                my_msg1 = "You have " + str(_1) + " and " + str(_2) + " and " + str(
                    _3) + "!\n Your result is " + str(_1 + _2 + _3) + "!!!"
                send_msg(get_chat_id(update), my_msg1)
            else:
                send_msg(get_chat_id(update),
                        "Sorry! I do not understand what you mean :(")
            update_id += 1


# calling the main function
# main()
