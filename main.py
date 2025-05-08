# -*- encoding: utf-8 -*-
import json
import time

import telebot
from telebot import types

from secret_file import secret_token

bot = telebot.TeleBot(secret_token())

user_data = {}

with open('src/lessons.json', 'r', encoding='utf-8') as lesson_data_file:
    lesson_pages = json.load(lesson_data_file)

with open('src/tests.json', 'r', encoding='utf-8') as tests_data_file:
    tests = json.load(tests_data_file)['tests']

lessons = lesson_pages.keys()


@bot.message_handler(func=lambda message: message.text in ['/start', '🔠 Главное меню'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('🧠 Уроки')
    btn2 = types.KeyboardButton('❓ Тесты')
    btn3 = types.KeyboardButton('❌ Я пожалуй откажусь')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, (
        'Привет, друг!\n'
        'Давай изучать историю вместе 😎'
    ), reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🧠 Уроки')
def choose_lesson_handler(message):
    new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    new_markup.add(
        *[types.KeyboardButton(name) for name in lessons],
        types.KeyboardButton('🔠 Главное меню'),
    )
    bot.send_message(message.chat.id, 'Выбери главу', reply_markup=new_markup)


@bot.message_handler(func=lambda message: message.text in ['❓ Тесты', '📖 К тестам'])
def choose_test_handler(message):
    new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    new_markup.add(
        *[types.KeyboardButton(test['name']) for test in tests],
        types.KeyboardButton('🔠 Главное меню'),
    )
    bot.send_message(message.chat.id, 'Выбери тест', reply_markup=new_markup)


@bot.message_handler(func=lambda msg: msg.text in [test['name'] for test in tests])
def start_test_handler(message):
    user_id = message.from_user.id
    selected_test = next(test for test in tests if test['name'] == message.text)

    user_data[user_id] = {'test': selected_test, 'question_index': 0, 'score': 0}
    send_test_question(message.chat.id, user_id)


def send_test_question(chat_id, user_id):
    data = user_data.get(user_id)
    if not data or 'test' not in data:
        bot.send_message(chat_id, 'Ошибка: нет данных о тесте.')
        return

    test_data = data['test']
    question_index = data.get('question_index', 0)
    score = data.get('score', 0)

    questions = test_data['questions']
    if question_index >= len(questions):
        bot.send_message(chat_id, f'Тест завершен!\nВаш результат: {score} из {len(questions)}.')
        del user_data[user_id]
        return

    question = questions[question_index]
    markup = types.InlineKeyboardMarkup()
    for idx, answer in enumerate(question['answers']):
        markup.add(types.InlineKeyboardButton(answer, callback_data=f'test_answer_{idx}'))

    bot.send_message(
        chat_id,
        f"🔹 Вопрос {question_index + 1}/{len(questions)}:\n{question['task']}",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('test_answer_'))
def test_answer_handler(call):
    user_id = call.from_user.id
    data = user_data.get(user_id)

    if not data or 'test' not in data:
        bot.send_message(call.message.chat.id, 'Тест не найден')
        return

    test_data = data['test']
    question_index = data['question_index']
    answer_idx = int(call.data.split('_')[2])
    selected_answer = test_data['questions'][question_index]['answers'][answer_idx]
    correct_answer = test_data['questions'][question_index]['correct']

    if selected_answer == correct_answer:
        data['score'] = data.get('score', 0) + 1
        response = '✅ Правильно!'
    else:
        response = f'❌ Неправильно. Правильный ответ: {correct_answer}'

    data['question_index'] += 1

    bot.send_message(call.message.chat.id, response)
    send_test_question(call.message.chat.id, user_id)


@bot.message_handler(func=lambda message: message.text == '❌ Я пожалуй откажусь')
def rejection_handler(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'ля ты криса')
    with open('src/photo.bmp', 'rb') as photo:
        for i in range(50):
            photo.seek(0)
            bot.send_photo(message.chat.id, photo)


def send_lesson_page(chat_id, user_id):
    data = user_data.get(user_id)
    if not data:
        bot.send_message(chat_id, 'Ошибка: нет данных о главе.')
        return

    lesson = data['lesson']
    page = data['page']
    pages = lesson_pages[lesson]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    if page > 0:
        buttons.append('⬅ Назад')
    if page < len(pages) - 1:
        buttons.append('➡ Далее')
    if page == len(pages) - 1:
        buttons.append('📖 К тестам')
    buttons.append('🔠 Главное меню')
    markup.add(*[types.KeyboardButton(b) for b in buttons])

    bot.send_message(chat_id, pages[page], reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text in ['⬅ Назад', '➡ Далее'])
def paginate_handler(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.send_message(message.chat.id, 'Сначала выбери урок')
        return

    direction = message.text
    if direction == '➡ Далее':
        user_data[user_id]['page'] += 1
    elif direction == '⬅ Назад':
        user_data[user_id]['page'] -= 1

    send_lesson_page(message.chat.id, user_id)


@bot.message_handler(func=lambda message: message.text in lesson_pages)
def lesson_handler(message):
    user_id = message.from_user.id
    lesson = message.text

    user_data[user_id] = {'lesson': lesson, 'page': 0}
    send_lesson_page(message.chat.id, user_id)


@bot.message_handler(func=lambda msg: msg.text == '⏭ Следующая глава')
def next_chapter_handler(message):
    user_id = message.from_user.id
    data = user_data.get(user_id)

    if not data:
        bot.send_message(message.chat.id, 'Сначала выбери урок')
        return

    current_lesson = data['lesson']
    current_page = data['page']

    pages = lesson_pages[current_lesson]

    if current_page + 1 < len(pages):
        user_data[user_id]['page'] += 1
        send_lesson_page(message.chat.id, user_id)
        return

    lesson_index = lessons.index(current_lesson)
    if lesson_index + 1 >= len(lessons):
        bot.send_message(message.chat.id, 'Это была последняя глава 🎉')
        return

    next_lesson = lessons[lesson_index + 1]
    user_data[user_id] = {
        'lesson': next_lesson,
        'page': 0
    }

    send_lesson_page(message.chat.id, user_id)


@bot.message_handler(func=lambda message: True)
def fallback_handler(message):
    bot.send_message(message.chat.id, 'кнопочки жми я не понимаю')


bot.polling(none_stop=True, interval=0)
