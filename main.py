from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)  # Создаем Фласк-приложение

DB_FILE = "data/db.json"


# При запуске = читать из файла
def load_messages():
    with open(DB_FILE, "r") as json_file:  # Открывает файл, в переменную
        data = json.load(json_file)  # Читает файл в формате JSON
        return data["messages"]


all_messages = load_messages()  # Список всех сообщений


# При сообщении = записывать в файл
def save_messages():
    with open(DB_FILE, "w") as json_file:
        data = {
            "messages": all_messages
        }
        json.dump(data, json_file)


def add_message(text, sender):
    current_time = datetime.now().strftime("%H:%M:%S")  # "20:56"
    new_message = {
        "text": text,
        "sender": sender,
        "time": current_time
    }
    all_messages.append(new_message)
    save_messages()


def print_message(message):
    print(f"[{message['sender']}]: {message['text']} / {message['time']}")


def print_all_messages():
    for msg in all_messages:
        print_message(msg)


@app.route("/")  # Создаем раздел на сайте
def main_page():
    return render_template("index.html")


@app.route("/get_messages")
def get_messages():
    return {"messages": all_messages}


@app.route("/send_message")
def send_message():
    text = request.args["text"]  # Получаем текст от пользователя
    sender = request.args["name"]  # Получаем имя отправителя
    if len(sender) < 3 or len(sender) > 100:
        sender = 'ERROR'
    if len(text) < 1 or len(text) > 3000:
        text = 'ERROR'
    add_message(text, sender)

@app.route("/chat")
def display_chat():
    return render_template("form.html")


app.run()
