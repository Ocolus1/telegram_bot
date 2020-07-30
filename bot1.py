import telepot
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from func import _start, _bountyoptions
from datetime import datetime
import string
from random import choices
import time
import csv


# app configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    # Set the secret key to a sufficiently random value
    SECRET_KEY=os.urandom(24),
    DEBUG=True
)


# initialise the cursor
db = SQLAlchemy(app)

token = 'TOKEN'

# initialise the bot
bot = telepot.Bot(token)


class Email(db.Model):
    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, default=0, unique=True)
    email = db.Column(db.String(512))
    pub_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Tweet(db.Model):
    __tablename__ = "tweet"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, default=0)
    username = db.Column(db.String(512))
    pub_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Telegram(db.Model):
    __tablename__ = "telegram"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, default=0)
    username = db.Column(db.String(512))
    pub_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Facebook(db.Model):
    __tablename__ = "facebook"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, default=0)
    username = db.Column(db.String(512))
    pub_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Ethaddress(db.Model):
    __tablename__ = "ethaddress"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, default=0)
    address = db.Column(db.String(512))
    pub_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Link(db.Model):
    __tablename__ = "link"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(512), unique=True)
    email = db.Column(db.String(225), default="john@gmail.com")
    twitter = db.Column(db.String(225), default="tweetuser")
    telegram = db.Column(db.String(225), default="teleuser")
    facebook = db.Column(db.String(225), default="facebookuser")
    ethaddress = db.Column(db.String(225), default="ethuser")
    fname = db.Column(db.String(225))
    gen_c = db.Column(db.String(4), unique=True)
    referal = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gen_c = self.generate_short_link()
        self.email = self.emails()
        self.twitter = self.twitters()
        self.telegram = self.telegrams()
        self.facebook = self.facebooks()
        self.ethaddress = self.eth()

    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        gen_c = "".join(choices(characters, k=8))

        link = self.query.filter_by(gen_c=gen_c).first()

        if link:
            return self.generate_short_link()

        return gen_c

    def emails(self):
        update = last_update()
        chat_id = get_chat_id(update)
        result = Email.query.filter_by(chat_id=chat_id).first()
        # email = result.email
        return result.email

    def twitters(self):
        update = last_update()
        chat_id = get_chat_id(update)
        result = Tweet.query.filter_by(chat_id=chat_id).first()
        # twitter = result.username
        return result.username

    def telegrams(self):
        update = last_update()
        chat_id = get_chat_id(update)
        result = Telegram.query.filter_by(chat_id=chat_id).first()
        # tele = result.username
        return result.username

    def facebooks(self):
        update = last_update()
        chat_id = get_chat_id(update)
        result = Facebook.query.filter_by(chat_id=chat_id).first()
        # face = result.username
        return result.username

    def eth(self):
        update = last_update()
        chat_id = get_chat_id(update)
        result = Ethaddress.query.filter_by(chat_id=chat_id).first()
        # eth = result.address
        return result.address


# func that get user id
def get_chat_id(update):
    chat_id = update["message"]["chat"]["id"]
    return chat_id


# func that get message text
def get_text(update):
    text = update["message"]["text"]
    return text


# func that gets the last update
def last_update():
    response = bot.getUpdates()
    total_updates = len(response) - 1
    return response[total_updates]  # get the last recorded message


# func that sends msg to the usr
def send_msg(chat_id, msg_text):
    response = bot.sendMessage(chat_id, msg_text)
    return response


def _help():
    return """
/twitter - Input your twitter username
/clear - clear Referal List
/reflist - view my Referrals List
/mylink - get my affiliate link
/start - start
"""


def _feed():
    return "feedddd"


def _email():
    update = last_update()
    chat_id = get_chat_id(update)
    result = Email.query.filter_by(chat_id=chat_id).first()
    if result: 
        email = result.email 
        tot = "Your email - {} \n /changeemail - to change email ".format(email)
        return tot
    else:
        msg = "Enter your email address"
        chat_id = update["message"]["chat"]["id"]
        bot.sendMessage(chat_id, msg)
        x = update["update_id"]
        response = bot.getUpdates(offset=(x + 1), timeout=3600)
        total_updates = len(response) - 1
        try:
            text = response[total_updates]["message"]["text"]
            email = Email(chat_id=chat_id, email=text)
            db.session.add(email)
            db.session.commit()
        except:
            return "An error occurred"
        return "Email is saved"


def _changeemail():
    update = last_update()
    msg = "Enter your email address"
    chat_id = update["message"]["chat"]["id"]
    bot.sendMessage(chat_id, msg)
    x = update["update_id"]
    response = bot.getUpdates(offset=(x + 1), timeout=3600)
    total_updates = len(response) - 1
    try:
        text = response[total_updates]["message"]["text"]
        result = Email.query.filter_by(chat_id=chat_id).first()
        result.email  = text
        db.session.commit()
        return "Email is saved"
    except:
        return "An error occurred"


def _twitter():
    update = last_update()
    chat_id = get_chat_id(update)
    result = Tweet.query.filter_by(chat_id=chat_id).first()
    if result: 
        user = result.username
        tot = "Your username - {} \n /changetwitter - to change twitter username".format(user)
        return tot
    else:
        msg = "Input your twitter username"
        chat_id = update["message"]["chat"]["id"]
        bot.sendMessage(chat_id, msg)
        x = update["update_id"]
        response = bot.getUpdates(offset=(x + 1), timeout=3600)
        total_updates = len(response) - 1
        try:
            text = response[total_updates]["message"]["text"]
            tweet = Tweet(chat_id=chat_id, username=text)
            db.session.add(tweet)
            db.session.commit()
        except:
            return "An error occurred"
        return "Twitter username is saved"


def _changetwitter():
    update = last_update()
    msg = "Input your twitter username"
    chat_id = update["message"]["chat"]["id"]
    bot.sendMessage(chat_id, msg)
    x = update["update_id"]
    response = bot.getUpdates(offset=(x + 1), timeout=3600)
    total_updates = len(response) - 1
    try:
        text = response[total_updates]["message"]["text"]
        result = Tweet.query.filter_by(chat_id=chat_id).first()
        result.username =  text
        db.session.commit()
        return "Twitter username is saved"
    except:
        return "An error occurred"


def _tele():
    update = last_update()
    chat_id = get_chat_id(update)
    result = Telegram.query.filter_by(chat_id=chat_id).first()
    if result: 
        user = result.username
        tot = "Your username - {} \n /changetele - to change telegram username".format(user)
        return tot
    else:
        msg = "Input your telegram username"
        chat_id = update["message"]["chat"]["id"]
        bot.sendMessage(chat_id, msg)
        x = update["update_id"]
        response = bot.getUpdates(offset=(x + 1), timeout=3600)
        total_updates = len(response) - 1
        try:
            text = response[total_updates]["message"]["text"]
            tele = Telegram(chat_id=chat_id, username=text)
            db.session.add(tele)
            db.session.commit()
        except:
            return "An error occurred"
        return "Telegram username is saved"


def _changetele():
    update = last_update()
    msg = "Input your telegram username"
    chat_id = update["message"]["chat"]["id"]
    bot.sendMessage(chat_id, msg)
    x = update["update_id"]
    response = bot.getUpdates(offset=(x + 1), timeout=3600)
    total_updates = len(response) - 1
    try:
        text = response[total_updates]["message"]["text"]
        result = Telegram.query.filter_by(chat_id=chat_id).first()
        result.username = text
        db.session.commit()
        return "Telegram username is saved"
    except:
        return "An error occurred"


def _facebook():
    update = last_update()
    chat_id = get_chat_id(update)
    result = Facebook.query.filter_by(chat_id=chat_id).first()
    if result: 
        user = result.username
        tot = "Your username - {} \n /changeface - to change facebook username".format(user)
        return tot
    else:
        msg = "Input your Facebook name"
        chat_id = update["message"]["chat"]["id"]
        bot.sendMessage(chat_id, msg)
        x = update["update_id"]
        response = bot.getUpdates(offset=(x + 1), timeout=3600)
        total_updates = len(response) - 1
        try:
            text = response[total_updates]["message"]["text"]
            face = Facebook(chat_id=chat_id, username=text)
            db.session.add(face)
            db.session.commit()
        except:
            return "An error occurred"
        return "Facebook name is saved"


def _changeface():
    update = last_update()
    msg = "Input your Facebook name"
    chat_id = update["message"]["chat"]["id"]
    bot.sendMessage(chat_id, msg)
    x = update["update_id"]
    response = bot.getUpdates(offset=(x + 1), timeout=3600)
    total_updates = len(response) - 1
    try:
        text = response[total_updates]["message"]["text"]
        result = Facebook.query.filter_by(chat_id=chat_id).first()
        result.username = text
        db.session.commit()
        return "Facebook name is saved"
    except:
        return "An error occurred"


def _ethaddress():
    update = last_update()
    chat_id = get_chat_id(update)
    result = Ethaddress.query.filter_by(chat_id=chat_id).first()
    if result: 
        address = result.address
        tot = "Your username - {} \n /changeeth - to change ethaddress username".format(address)
        return tot
    else:
        msg = "Enter your erc 20 waallet address"
        chat_id = update["message"]["chat"]["id"]
        bot.sendMessage(chat_id, msg)
        x = update["update_id"]
        response = bot.getUpdates(offset=(x + 1), timeout=3600)
        total_updates = len(response) - 1
        try:
            text = response[total_updates]["message"]["text"]
            eth = Ethaddress(chat_id=chat_id, address=text)
            db.session.add(eth)
            db.session.commit()
        except:
            return "An error occurred"
        return "Your wallet address is saved"


def _changeeth():
    update = last_update()
    msg = "Enter your erc 20 waallet address"
    chat_id = update["message"]["chat"]["id"]
    bot.sendMessage(chat_id, msg)
    x = update["update_id"]
    response = bot.getUpdates(offset=(x + 1), timeout=3600)
    total_updates = len(response) - 1
    try:
        text = response[total_updates]["message"]["text"]
        result = Ethaddress.query.filter_by(chat_id=chat_id).first()
        result.address = text
        db.session.commit()
        return "Your wallet address is saved"
    except:
        return "An error occurred"


def _mylink():
    update = last_update() 
    chat_id = get_chat_id(update)
    fname = update["message"]["chat"]["first_name"]
    links = Link.query.filter_by(chat_id=chat_id).first()
    if links:
        gen_c = links.gen_c
        msg = "https://telegram.me/cypherSpotBot?start={}".format(gen_c)
        send_msg(chat_id, msg)
    else:
        try:
            link = Link(chat_id=chat_id, fname=fname)
            db.session.add(link)
            db.session.commit()
        except:
            return "An error occured"
        lin = Link.query.filter_by(chat_id=chat_id).first()
        gen = lin.gen_c
        ms = "https://telegram.me/cypherSpotBot?start={}".format(gen)
        send_msg(chat_id, ms)
    return "That is your referal link"


def _reflist():
    update = last_update()
    chat_id = get_chat_id(update)
    link = Link.query.filter_by(chat_id=chat_id).first()
    reflist = link.referal
    msg = "You have " + str(reflist) + " referals"
    return msg


def _top():
    link = Link.query.order_by(Link.referal.desc()).all()
    for lin in link[:10]:
        return str(lin.fname) + " " + str(lin.referal)


def _clear():
    update = last_update()
    chat_id = get_chat_id(update)
    link = Link.query.filter_by(chat_id=chat_id).first()
    link.referal = 0
    db.session.commit()
    return "Your referal list has been cleared"


def _export():
    link = db.engine.execute('SELECT * FROM link')
    with open("wub.csv", "w") as csv_file:
        fieldnames = ['id', 'chat_id', 'email', 'twitter', 'telegram',
        'facebook', 'ethaddress', 'fname', 'gen_c', 'referal', 'pub_date']
        writer = csv.writer(csv_file)
        writer.writerow(fieldnames)
        for lin in link:
            writer.writerow(lin)
    return "file exported to wub.csv"


error_msg= """
/twitter - Input your twitter username
/clear - clear Referal List
/reflist - view my Referrals List
/mylink - get my affiliate link
/start - start
"""

# the main func 
def main():
    update_id = last_update()["update_id"]
    while True:
        update = last_update()
        if update_id == update["update_id"]:
            commands = {
                '/start': _start,
                '/help': _help,
                '/feed': _feed,
                '/bountyoptions': _bountyoptions,
                '/email': _email,
                '/twitter': _twitter,
                '/telegram': _tele,
                '/facebook': _facebook,
                '/ethaddress': _ethaddress,
                '/mylink': _mylink,
                '/reflist': _reflist,
                '/top': _top,
                '/clear': _clear,
                '/sheldoncooper': _export,
                '/changeemail': _changeemail,
                '/changetwitter': _changetwitter,
                '/changetele': _changetele,
                '/changeface': _changeface,
                '/changeeth': _changeeth
            }
            if token:
                chat_id = get_chat_id(update)
                cmd = get_text(update)  # command
                func = commands.get(cmd.split()[0].lower())
                link = Link.query.all()
                for lin in link:
                    gen_c = lin.gen_c
                    if func and cmd.endswith(gen_c):
                        if cmd.startswith('/start'):
                            command, payload = cmd.split(" ")
                            link = Link.query.filter_by(gen_c=payload).first()
                            chat = Link.query.filter_by(chat_id=chat_id).first()
                            if link and not chat:
                                link.referal += 1
                                db.session.commit()
                                bot.sendMessage(chat_id, func(), parse_mode="Markdown")
                                time.sleep(1)
                                # bot.sendMessage(chat_id, "You have been added to your referal")
                            elif link and chat:
                                bot.sendMessage(chat_id, "User already exist")
                else:
                    if func and not cmd.endswith(gen_c):
                        bot.sendMessage(chat_id, func(), parse_mode='Markdown')
                    else:
                        bot.sendMessage(chat_id, error_msg)
            update_id += 1


if __name__ == "__main__":
    main()