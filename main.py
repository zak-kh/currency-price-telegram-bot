import asyncio

# aiogram
from aiogram import Bot, Dispatcher, filters, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.session.aiohttp import AiohttpSession

# price fetcher of websites
from PriceGetter.main import fetch_text, return_price, find_tag, get_change

# type hints
from typing import Final

# configs
import configs

dp = Dispatcher()


@dp.message(filters.CommandStart())
async def start(msg: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💵 دریافت قیمت دلار', callback_data='dollar_price')],
        [InlineKeyboardButton(text='💶 دریافت قیمت یورو', callback_data='euro_price')],
        [InlineKeyboardButton(text='🟨 دریافت قیمت بیت کوین', callback_data='btc_price')],
        [InlineKeyboardButton(text='🟡 دریافت قیمت طلا', callback_data='gold_price')],
    ])
    await msg.answer('لطفا گزینه مورد نظرتون رو انتخاب کنید.', reply_markup=markup)


def get_price(url: str, currency: str, toman=False):
    text = fetch_text(url)
    tag = find_tag(text, 'span', 'price')
    currency_price = int(return_price(tag) // 10) if toman else return_price(tag)
    change = get_change(text)
    return f'🪙 قیمت {currency}: {currency_price:,} \n تغیر امروز: {change}'


@dp.callback_query()
async def price_dollar(call: CallbackQuery):
    url: Final['str'] = 'https://www.tgju.org/profile/'

    match call.data:
        case 'btc_price':
            btc_price = f'{url}crypto-bitcoin'
            text_ = get_price(btc_price, 'بیت کوین')
            await call.bot.send_message(call.message.chat.id, text_)
        case 'dollar_price':
            dollar_url = f'{url}price_dollar_rl'
            text_ = get_price(dollar_url, 'دلار', True)
            await call.bot.send_message(call.message.chat.id, text_)
        case 'euro_price':
            euro_url = f'{url}price_eur'
            text_ = get_price(euro_url, 'یورو', True)
            await call.bot.send_message(call.message.chat.id, text_)
        case 'gold_price':
            gold_url = f'{url}geram18'
            text_ = get_price(gold_url, 'طلا', True)
            await call.bot.send_message(call.message.chat.id, text_)
        case _:
            await call.bot.send_message(call.message.chat.id, 'دستور ناشناخته ❌')


@dp.message(F.text.lower() == 'قیمت')
async def price(msg: Message):
    await start(msg=msg)


async def main():
    proxy = AiohttpSession('http://127.0.0.1:12334')
    bot = Bot(session=proxy, token=configs.TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
