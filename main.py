import asyncio

# aiogram
from aiogram import Bot, Dispatcher, filters, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.client.session.aiohttp import AiohttpSession

# price fetcher from website
from PriceGetter.main import fetch_text, return_price, find_tag, get_change

# type hints
from typing import Final

# configs
import configs

# helper
import helper

dp = Dispatcher()


@dp.message(filters.CommandStart())
async def start(msg: Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🟨 دریافت قیمت بیت کوین', callback_data='btc_price')],
        [InlineKeyboardButton(text='💵 دریافت قیمت دلار', callback_data='dollar_price')],
        [InlineKeyboardButton(text='💶 دریافت قیمت یورو', callback_data='euro_price')],
        [InlineKeyboardButton(text='🟡 دریافت قیمت طلا 18 عیار', callback_data='gold_price')],
    ])
    await msg.answer('لطفا گزینه مورد نظرتون رو انتخاب کنید.', reply_markup=markup)


def get_price(url: str, currency: str, toman: bool):
    text = fetch_text(url)
    tag = find_tag(text, 'span', 'price')
    currency_price = int(return_price(tag) // 10) if toman else return_price(tag)
    change = get_change(text)
    return f'🪙 قیمت {currency}: {currency_price:,} \n\n📊 تغیر امروز: {change} '


@dp.callback_query()
async def price_dollar(call: CallbackQuery):
    url: Final['str'] = 'https://www.tgju.org/profile/'

    async def send_price(url, currency, toman=False):
        currency_url = f'https://www.tgju.org/profile/{url}'
        price_msg = get_price(currency_url, currency, toman=toman)
        await call.bot.send_message(call.message.chat.id, price_msg)

    match call.data:
        case 'btc_price':
            await send_price('crypto-bitcoin', 'بیت کوین')
        case 'dollar_price':
            await send_price('price_dollar_rl', 'دلار', toman=True)
        case 'euro_price':
            await send_price('price_eur', 'یورو', toman=True)
        case 'gold_price':
            await send_price('geram18', 'طلا 18 عیار', toman=True)
        case _:
            await call.bot.send_message(call.message.chat.id, 'دستور ناشناخته ❌')


@dp.message(F.text.lower() == 'قیمت')
async def price(msg: Message):
    await start(msg=msg)


@dp.message(F.text == 'admin')
@helper.admin_filter(configs.ADMINS)
async def price(msg: Message):
    await start(msg=msg)


async def main():
    proxy = AiohttpSession('http://127.0.0.1:12334')
    bot = Bot(session=proxy, token=configs.TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
