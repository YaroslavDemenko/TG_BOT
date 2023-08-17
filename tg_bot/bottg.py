import telebot
import random

bot = telebot.TeleBot('6246805629:AAEOCEZW5mIFSjS9EJpK1FuP51n4Wc2YO9U')

tasks = [
    {
        'type': 'геометрия',
        'question': 'Найдите площадь круга радиусом 5 см?',
        'choices': {'a': '25п', 'b': '10п', 'c': '5п', 'd': '15п'},
        'correct': 'a',
    },
    {
        'type': 'алгебра',
        'question': 'Решите уравнение: 2x - 3 = 9',
        'choices': {'a': 'x=3', 'b': 'x=-3', 'c': 'x=6', 'd': 'x=-6'},
        'correct': 'c',
    },
    {
        'type': 'тригонометрия',
        'question': 'Найдите катет прямоугольного треугольника, если гипотенуза равна 10, а угол между гипотенузой и катетом равен 30 градусов',
        'choices': {'a': '5', 'b': '2.5', 'c': '7.5', 'd': '10'},
        'correct': 'b',
    },
]

user_scores = []
user_answers = {}

@bot.message_handler(commands=['task'])
def send_task(message):
    chat_id = message.chat.id
    if len(tasks) == 0:
        bot.send_message(chat_id, 'Задания закончились! Напиши /results, чтобы узнать свой результат!')
        return

    random_task = random.choice(tasks)

    question = random_task['question']
    choices = random_task['choices']

    choices_str = '\n'.join([f'{key}. {value}' for key, value in choices.items()])

    bot.reply_to(message, f'{random_task["type"]}:\n{question}\nВарианты ответов:\n{choices_str}')

    tasks.remove(random_task)

    user_answers[chat_id] = {
        'task': random_task,
        'answer': '',
    }

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in user_answers:
        bot.send_message(chat_id, 'Напиши /task, чтобы получить новое задание!')
        return

    user_task = user_answers[chat_id]['task']
    task_correct_answer = user_task['correct']
    user_choice = message.text.lower()

    if user_choice.startswith('/'):
        return

    if user_choice != 'a' and user_choice != 'b' and user_choice != 'c' and user_choice != 'd':
        bot.send_message(chat_id, 'Некорректный ввод! Введи букву варианта ответа: a, b, c или d')
        return
    
    user_answers[chat_id]['answer'] = user_choice

    if user_choice == task_correct_answer:
        bot.send_message(chat_id, 'Правильно!')
        user_scores.append(1)
    else:
        bot.send_message(chat_id, f'Неправильно! Правильный ответ: {user_task["choices"][task_correct_answer]}')
        user_scores.append(0)

    send_task(message)

@bot.message_handler(commands=['results'])
def show_results(message):
    chat_id = message.chat.id
    score = sum(user_scores)
    total = len(user_scores)
    bot.send_message(chat_id, f'У тебя {score} правильных ответов из {total} заданий за все время!')
    user_scores.clear()
    user_answers.clear()
    send_task(message)

bot.polling()