from json import load
from time import time
from logging import INFO, basicConfig
# import aiohttp
from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling

from core.searching_answers import *

with open("src/package/client.json", "r") as telegram_data:
    data = load(telegram_data)
basicConfig(level=INFO)

PROXY_URL = 'http://89.208.219.121:8080'
bot = Bot(token=data["telegram_token"], proxy=PROXY_URL)
# bot = Bot(token=data["telegram_token"])
client = Dispatcher(bot)

admin_id, id_users = [489951151, 857280061], \
                     [id_user.split(',')[0] for id_user in open("src/package/analytics.txt", "r")]


def analytics(message: Message) -> None:
    with open('src/package/analytics.txt', '+r') as user_id:
        if str(message.from_user.id) not in user_id.read():
            user_id.write(f'{message.from_user.id}, {message.from_user.username}, {message.from_user.first_name}\n')


def post(message: Message, final_text='') -> tuple:
    if 'all' not in message.text:
        post_text = message.text.replace('post ', '').split(' ')
        user_id = post_text[0]
        for text in post_text:
            final_text += f'{text} '
        return user_id, final_text.replace(user_id, '')


@client.message_handler(commands=["start", "help"])
async def manual(msg: Message):
    with open("src/package/client_lock.json", "r") as file:
        sys = load(file)
    await msg.answer(f"""👋Привет, {msg.from_user.first_name}.\n
❗Для начала работы, отправь мне ссылку на тест и я постараюсь найти ответы.\n📝Пример ссылки: {sys['example']}\n
⚠️Если возникла какая-либо проблема, ошибка, баг обратитесь в чат поддержки👨🏼‍🔧: {sys['help_place']}.
Там Вам помогут с сложившейся ситуацией.🎯\n
💯Также можешь меня оценить,\n просто написав мне оценку👇\n
🤖Версия бота: {sys['version']}
🪄Ссылка на бота: {sys['link']}
📌ВК создателя: {sys['vk']}""")
    analytics(msg)


@client.message_handler(commands=['admin', 'analytics'])
async def admin(msg: Message, counter=0):
    with open("src/package/analytics.txt", "r") as analytic:
        if msg.from_user.id in admin_id:
            for number, id_user in enumerate(analytic.readlines()):
                await msg.answer(f'{number + 1}. User: {id_user}')
                counter = number + 1
            await msg.answer(f'🙈Всего пользователей: {counter}')
        else:
            await msg.answer("⚠️Для начала, отправь ссылку на тест, и я попробую его решить.🤡")


@client.message_handler(content_types=['text'])
async def get_text_messages(msg: Message, trouble=None):
    user_text = msg.text
    if user_text.startswith("https://uchebnik.mos.ru"):
        try:
            start_time = time()
            await msg.answer(f"👽Начал решать ({type_test(user_text)})🔗")

            for task_number, task in enumerate(get_cdz_answers(user_text)):
                await msg.answer(f"✏️Вопрос №{task_number + 1}: {task[0]}\n\n✅Ответ: {task[1]}")

            await msg.answer(f"⏳Решено за {'%s секунд' % round((time() - start_time), 1)}")

        except Exception as e:
            await msg.answer('⚠️Хм странно, но я ничего не нашел. Проверь правильность ссылки или нажми 👉/help👈')

            trouble = '⚠️{}⚠️'.format(e)
            trouble += '(Не корректная ссылка)' if 'training_tasks' in trouble else str()

    elif 'post all' in user_text and msg.from_user.id == admin_id[0]:
        post_text = user_text.replace('post ', '').replace('all ', '')
        for user in id_users:
            await bot.send_message(user, post_text)

    elif 'post' in user_text and msg.from_user.id in admin_id:
        user_id, final_text = post(msg)
        await bot.send_message(user_id, final_text)

    elif user_text.isdigit():
        await msg.answer('Спасибо за оценку😊')

    else:
        await msg.answer("⚠️Для начала, отправь ссылку на тест, и я попробую его решить.🛸")

    info = f"Text: {user_text}\nTrouble: {trouble}\nUser: (id: {msg.from_user.id}, name: {msg.from_user.first_name}," \
           f" username: {msg.from_user.username})"
    await bot.send_message(admin_id[0], info)
    analytics(msg)


@client.message_handler(
    content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker',
                   'venue', 'video', 'video_note', 'voice'])
async def get_text_messages(msg: Message):
    await msg.answer("⚠️Для начала, отправь ссылку на тест, и я попробую его решить.🛸")
    info = f"Text: {msg.text}\nUser(id: {msg.from_user.id}, name: {msg.from_user.first_name}," \
           f" username: {msg.from_user.username})"
    await bot.send_message(admin_id[0], info)


start_polling(client, skip_updates=True) if __name__ == "__main__" else print("it's not lib")
