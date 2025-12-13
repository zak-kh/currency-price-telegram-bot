import asyncio

from aiogram import Bot, Dispatcher, filters, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import Command
from DollarPrice.main import fetch_text, return_price, find_tag
from typing import Final

dp = Dispatcher()


@dp.message(filters.CommandStart())
async def start(msg: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💵 دریافت قیمت دلار', callback_data='dollar_price')],
        [InlineKeyboardButton(text='💶 دریافت قیمت یورو', callback_data='euro_price')],
        [InlineKeyboardButton(text='💛 دریافت قیمت طلا', callback_data='gold_price')],
    ])
    await msg.answer('لطفا گزینه مورد نظرتون رو انتخاب کنید.', reply_markup=markup)


def get_price(URL, currency):
    text = fetch_text(URL)
    tag = find_tag(text, 'span', 'price')
    price = return_price(tag)
    return f'🪙 قیمت {currency}: {price:,}'


@dp.callback_query()
async def price_dollar(call: CallbackQuery):
    URL: Final['str'] = 'https://www.tgju.org/profile/'

    if call.data == 'dollar_price':
        dollar_url = f'{URL}price_dollar_rl'
        text_ = get_price(dollar_url, 'دلار')
        await call.bot.send_message(call.message.chat.id, text_)
    elif call.data == 'euro_price':
        euro_url = f'{URL}price_eur'
        text_ = get_price(euro_url, 'یورو')
        await call.bot.send_message(call.message.chat.id, text_)
    elif call.data == 'gold_price':
        gold_url = f'{URL}geram18'
        text_ = get_price(gold_url, 'طلا')
        await call.bot.send_message(call.message.chat.id, text_)
    else:
        await call.bot.send_message(call.message.chat.id, 'دستور ناشناخته ❌')


@dp.message(F.text.lower() == 'قیمت')
async def price(msg: Message):
    await start(msg=msg)


async def main():
    TOKEN_: Final[str] = '8506432335:AAE5bhj_c1lXtXVsD9rykbCNZygoB2Hygc4'
    proxy = AiohttpSession('http://127.0.0.1:12334')
    bot = Bot(session=proxy, token=TOKEN_)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
