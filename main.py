import asyncio

from aiogram import Bot, Dispatcher, filters, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.session.aiohttp import AiohttpSession
from DollarPrice.main import fetch_text, return_price, find_tag
from typing import Final

dp = Dispatcher()


@dp.message(filters.CommandStart())
async def start(msg: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💵 دریافت قیمت دلار', callback_data='dollar_price')],
        [InlineKeyboardButton(text='💶 دریافت قیمت یورو', callback_data='euro_price')],
    ])
    await msg.answer('لطفا گزینه مورد نظرتون رو انتخاب کنید.', reply_markup=markup)


def get_price(URL, currency):
    text = fetch_text(URL)
    tag = find_tag(text, 'span', 'price')
    price = return_price(tag)
    return f'🪙 قیمت {currency}: {price:,}'


@dp.callback_query()
async def price_dollar(call: CallbackQuery):
    if call.data == 'dollar_price':
        URL: Final['str'] = 'https://www.tgju.org/profile/price_dollar_rl'
        text_ = get_price(URL, 'دلار')
        await call.bot.send_message(call.from_user.id, text_)
    elif call.data == 'euro_price':
        URL: Final['str'] = 'https://www.tgju.org/profile/price_eur'
        text_ = get_price(URL, 'یورو')
        await call.bot.send_message(call.from_user.id, text_)
    else:
        await call.bot.send_message(call.from_user.id, 'دستور ناشناخته ❌')


async def main():
    TOKEN_: Final[str] = '8506432335:AAE5bhj_c1lXtXVsD9rykbCNZygoB2Hygc4'
    proxy = AiohttpSession('http://127.0.0.1:12334')
    bot = Bot(session=proxy, token=TOKEN_)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
