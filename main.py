# -*- encoding: utf-8 -*-

import telebot
from telebot import types

from secret_file import secret_token

bot = telebot.TeleBot(secret_token())

user_data = {

}

lessons = [
    'Введение и общая структура экономики',
    'Промышленность и индустриализация',
    'Сельское хозяйство и продовольственное обеспечение',
    'Финансовая система и военные расходы',
    'Ленд-лиз и внешнеэкономическая помощь',
    'Заключение'
]

lesson_pages = {
    'Введение и общая структура экономики': [
        '''
Экономика Советского Союза в годы Второй мировой войны представляла собой централизованную систему, в которой государственное планирование играло ключевую роль.

Советское руководство осуществляло мобилизацию всех доступных ресурсов для защиты страны. С начала войны экономика СССР была переориентирована на обеспечение оборонной промышленности, что выражалось в перераспределении бюджетных средств, увеличении государственных расходов и активной координации работы всех отраслей экономики.

Основой системы являлась команда-административная модель, где решения принимались на высшем уровне, а контроль за исполнением возлагался на специализированные комитеты, такие как Государственный плановый комитет и Государственный комитет по бюджету.

Такой подход позволял оперативно реагировать на изменения в обстановке, хотя и имел свои недостатки, связанные с дефицитом товаров народного потребления и сложностями в управлении распределением ресурсов.
        '''
    ],
    'Промышленность и индустриализация': [
        '''
Предвоенная индустриализация (1928–1941)

Одной из ключевых задач советской экономики в предвоенный период была форсированная индустриализация, направленная на создание мощной промышленной базы, способной обеспечить обороноспособность страны. Первый пятилетний план (1928–1932) заложил основу для развития тяжелой промышленности, включая металлургию, машиностроение и энергетику. Вторая пятилетка (1933–1937) и третья (1938–1941, прервана войной) продолжили этот курс, уделяя особое внимание оборонному сектору.

К 1941 году СССР вышел на второе место в мире по объёмам промышленного производства, уступая лишь США. Были построены гиганты индустрии, такие как Магнитогорский металлургический комбинат, Уралмаш, Горьковский автомобильный завод (ГАЗ) и Сталинградский тракторный завод, который в годы войны стал ключевым производителем танков Т-34.
        ''', '''
Эвакуация промышленности и перестройка экономики в годы войны (1941–1945)

С началом Великой Отечественной войны перед СССР встала задача сохранения промышленного потенциала. В 1941–1942 годах была проведена беспрецедентная эвакуация предприятий из западных регионов на Урал, в Сибирь и Среднюю Азию. Всего было перемещено более 2,5 тыс. заводов и фабрик, а также около 10–12 млн рабочих и их семей.

Этот процесс потребовал колоссальных усилий: предприятия разбирались, перевозились и заново запускались в рекордные сроки. Например, Запорожский авиационный завод был эвакуирован в Омск и уже через три месяца возобновил выпуск штурмовиков Ил-2.
        ''', '''
Рост военного производства и роль централизованного планирования

Несмотря на потерю значительных территорий, СССР сумел не только восстановить, но и превзойти довоенные объёмы производства вооружений. К 1943 году советская промышленность выпускала больше танков, самолётов и артиллерии, чем Германия.

Ключевыми факторами успеха стали:
• Жёсткая централизация управления (ГКО – Государственный комитет обороны).
• Переориентация гражданских предприятий на военные нужды (например, часовые заводы стали выпускать взрыватели для снарядов).
• Использование труда женщин и подростков, которые составили до 50% рабочих на заводах.
        ''', '''
Итоги и значение индустриализации для победы

Благодаря проведённой в 1930-е годы индустриализации и эффективной мобилизации экономики в годы войны СССР смог обеспечить Красную Армию необходимым вооружением и техникой. К 1945 году советская промышленность производила в 5 раз больше артиллерийских орудий и в 2 раза больше танков, чем в 1941 году.

Опыт военной перестройки экономики оказал значительное влияние на послевоенное развитие СССР, закрепив приоритет тяжёлой и оборонной промышленности.
        '''
    ]
}


@bot.message_handler(func=lambda message: message.text in [
    '/start',
    '🔠 Главное меню'
])
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
def handle_text(message):
    new_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    new_markup.add(
        types.KeyboardButton('Введение и общая структура экономики'),
        types.KeyboardButton('Промышленность и индустриализация'),
        types.KeyboardButton('Сельское хозяйство и продовольственное обеспечение'),
        types.KeyboardButton('Финансовая система и военные расходы'),
        types.KeyboardButton('Ленд-лиз и внешнеэкономическая помощь'),
        types.KeyboardButton('Заключение'),
        types.KeyboardButton('⬅ Назад'),
    )
    bot.send_message(message.chat.id, 'Выбери главу', reply_markup=new_markup)


@bot.message_handler(func=lambda message: message.text == '❓ Тесты')
def nahui_handler(message):
    bot.send_message(message.chat.id, 'Выбери тест')


@bot.message_handler(func=lambda message: message.text == '❌ Я пожалуй откажусь')
def nahui_handler(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, '', reply_markup=markup)


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
    if page == len(pages)-1:
        buttons.append('📖 К тестам')
    buttons.append('🔠 Главное меню')
    markup.add(*[types.KeyboardButton(b) for b in buttons])

    bot.send_message(chat_id, pages[page], reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text in ['⬅ Назад', '➡ Далее'])
def paginate_handler(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        bot.send_message(message.chat.id, 'Сначала выбери урок.')
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
        bot.send_message(message.chat.id, 'Сначала выбери урок.')
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
    bot.send_message(message.chat.id, 'щта')


bot.polling(none_stop=True, interval=0)
