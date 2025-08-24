import random
import os
import telebot
from config import token

bot=telebot.TeleBot(token)

facts = [
    "BMW расшифровывается как Bayerische Motoren Werke — «Баварские моторные заводы».",
    "Компания основана в 1916 году в Мюнхене, Германия.",
    "Сначала BMW производила авиационные двигатели, а не автомобили.",
    "Синий и белый логотип символизирует флаг Баварии.",
    "Знаменитая «двойная решётка радиатора» впервые появилась в 1933 году",
    "BMW владеет марками Mini и Rolls-Royce Motor Cars.",
    "Родстер BMW 507 1950-х годов — один из самых редких BMW.",
    "Первый электрический BMW — это BMW 1602e, выпущенный в 1972 году.",
    "Подразделение BMW M GmbH (Motorsport) создано в 1972 году.",
    "Слоган BMW — «Автомобиль для удовольствия от вождения» (The Ultimate Driving Machine)."
]

@bot.message_handler(commands=["start"])
def start1(message):
    bot.send_message(message.chat.id, "Привет я твой Телеграм Бот, если ты хочешь поиграть в квиз то нажми на /startquiz а если ты хочешь узнать о обо мне больше то нажми на /info ")

@bot.message_handler(commands=["info"])
def info1(message):
    bot.send_message(message.chat.id, "Привет я твой Телеграм Бот, и я могу отправить тебе фотки разных модель бмв как например /bmwm5f90 /bmw3series /bmw5series /bmwi4 /bmwm4Coupe /bmwX5 ну а если ты хочешь рандомные фото о бмв то нажми на /bmwrandom я могу ещё отправить 10 разных фактов о бмв для этого нажми на /fact . А здесь ты можешь найти все комманды /commands")

@bot.message_handler(commands=["commands"])
def commands1(message):
    bot.send_message(message.chat.id, "/start /info /commands /startquiz /fact /bmwm5f90 /bmw3series /bmw5series /bmwi4 /bmwm4Coupe /bmwX5 /bmwrandom")


@bot.message_handler(commands=["fact"])
def send_fact(message):
    fact = random.choice(facts)
    bot.reply_to(message, fact)

@bot.message_handler(commands=["bmwm5f90"])
def send_bmw1(message):
    with open("/Users/mikail/Desktop/Second_bot/images/bmw2.jpg", "rb") as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=["bmw3series"])
def send_bmw2(message):
    with open("/Users/mikail/Desktop/Second_bot/images/BMW 3 Series.jpg", "rb") as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=["bmw5series"])
def send_bmw3(message):
    with open("/Users/mikail/Desktop/Second_bot/images/BMW 5 Series.jpeg", "rb") as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=["bmwi4"])
def send_bmw4(message):
    with open("/Users/mikail/Desktop/Second_bot/images/BMW i4.jpg", "rb") as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=["bmwm4Coupe"])
def send_bmw5(message):
    with open("/Users/mikail/Desktop/Second_bot/images/BMW M4 Coupe.jpg", "rb") as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=["bmwX5"])
def send_bmw6(message):
    with open("/Users/mikail/Desktop/Second_bot/images/BMW X5.jpg", "rb") as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=["bmwrandom"])
def bmwrandom1(message):
    PHOTO_FOLDER = "/Users/mikail/Desktop/Second_bot/images"
    photos = [f for f in os.listdir(PHOTO_FOLDER) if os.path.isfile(os.path.join(PHOTO_FOLDER, f))]

    if not photos:
        bot.send_message(chat_id=message.chat.id, text="В папке нет фотографий.")
        return

    random_photo_name = random.choice(photos)
    random_photo_path = os.path.join(PHOTO_FOLDER, random_photo_name)

    with open(random_photo_path, 'rb') as photo_file:
        bot.send_photo(chat_id=message.chat.id, photo=photo_file)



quiz_questions = [
    {
        "question": "что такое бмв",
        "options": ["машина, самолёл, ручка"],
        "correct_answer": "машина"
    },
    {
        "question": "бмв или мерседес",
        "options": ["бмв, мерседес, бугатти"],
        "correct_answer": "бмв"
    }
]

user_data = {}

@bot.message_handler(commands=["startquiz"])
def start_quiz(message):
    user_id = message.from_user.id
    user_data[user_id] = {"score": 0, "question_index": 0}
    bot.reply_to(message, "Привет! давай сделаем маленький квиз!")
    ask_question(message)


def ask_question(message):
    user_id = message.from_user.id
    if user_data[user_id]["question_index"] < len(quiz_questions):
        question_data = quiz_questions[user_data[user_id]["question_index"]]
        options = "\n".join([f"{i + 1}. {option}" for i, option in enumerate(question_data["options"])])
        bot.reply_to(message, f"Вопрос {user_data[user_id]['question_index'] + 1}: {question_data['question']}\n{options}")
    else:
        show_result(message)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        return
    
    user_answer = message.text.strip()
    question_data = quiz_questions[user_data[user_id]["question_index"]]
    correct_answer = question_data["correct_answer"]

    if user_answer == correct_answer:
        user_data[user_id]["score"] += 1
        bot.reply_to(message, f" Молодец это было правильно! Твои баллы: {user_data[user_id]['score']}")
    else:
        bot.reply_to(message, f" К сажелению это было неправильно. Правильный ответ: {correct_answer}\nТвои баллы: {user_data[user_id]['score']}")

    user_data[user_id]["question_index"] += 1
    ask_question(message)

def show_result(message):
    user_id = message.from_user.id
    score = user_data[user_id]["score"]
    total = len(quiz_questions)
    bot.reply_to(message, f"Квиз уже завершён! Ты набрал {score} из {total} баллов. /start")
    del user_data[user_id]

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
