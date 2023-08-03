from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters, FSMContext
from aiogram.utils import executor
import conf
import datetime
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.handler import CancelHandler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os.path
import aiosqlite


TEST_MODE = True

if conf.VPS:
    TEST_MODE = False

##------------------Блок ініціалізації-----------------##
if TEST_MODE:
    API_Token = conf.API_TOKEN_Test
    URL = 'http://127.0.0.1:8000/dr/'
else:
    API_Token = conf.TOKEN

ADMIN_ID = conf.ADMIN_ID
bot = Bot(token=API_Token)

# webhook settings
WEBHOOK_HOST = 'https://vmi957205.contaboserver.net'
WEBHOOK_PATH = '/prod_terinfobot'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip 127.0.0.1
WEBAPP_PORT = 3007
bot = Bot(token=API_Token)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")


class Registration(StatesGroup):
    code = State()
    name = State()
    info = State()


class Publications(StatesGroup):
    data = State()
    sum = State()
    allowed = State()
    text = State()


async def isDriverInBase(id):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(f'SELECT id FROM adminkaDrivers_driver WHERE telegramId={id}')
        rows = await cursor.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False


async def countOfUserBublicationsToday(id):
    driver_id = await getDriverIdByTelegramId(id)
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(f"SELECT * FROM adminkaDrivers_publications WHERE driver_id={driver_id} AND strftime('%Y-%m-%d','now')=strftime('%Y-%m-%d',data)") #AND strftime('%Y-%m-%d','now')=strftime('%Y-%m-%d',data)
        rows = await cursor.fetchall()
        return len(rows)


async def getDriverIdByTelegramId(id):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(f'SELECT id FROM adminkaDrivers_driver WHERE telegramId={id}')
        rows = await cursor.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return False


async def codeValid(code):
    res = await getCodeIdByCode(code)
    if res:
        return True
    else:
        return False


async def getCodeIdByCode(code):
    async with aiosqlite.connect(db_path) as db:
        cursor = await db.execute(f'SELECT id FROM adminkaDrivers_cod WHERE cod={code}')
        rows = await cursor.fetchall()
    if len(rows) > 0:
        return rows[0][0]
    else:
        return False


async def userRegistration(name,info,cod,telegramId):
    codid = await getCodeIdByCode(cod)
    async with aiosqlite.connect(db_path) as db:
        await db.execute("INSERT INTO adminkaDrivers_driver (name,text,cod_id,telegramId) VALUES (?,?,?,?)", (name,info,codid,telegramId))
        await db.commit()


async def addPublications(telegid,date,sum,allowed,text):
    driver = await getDriverIdByTelegramId(telegid)
    dateNow = datetime.datetime.now()
    datenow = dateNow.strftime("%Y-%m-%d")
    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            f"INSERT INTO adminkaDrivers_publications (data,text,driver_id,dataOfStartRoute,summ,allowed,PublicationsAllowed) VALUES (?,?,?,?,?,?,?)",
            (datenow, text, driver, date, sum, allowed, False))
        await db.commit()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    res = await isDriverInBase(message.from_user.id)
    if res:
        countOfUserBublications = await countOfUserBublicationsToday(message.from_user.id)
        if  countOfUserBublications > 1:
            await message.answer("Вибачте, дозволено лише 2 публікації на день")
        else:
            await message.answer("Напишіть дату відправлення наприклад 2023-11-15")
            await Publications.data.set()

    else:
        await message.answer("Рееструємся. Введіть ваш код!")
        await Registration.code.set()


@dp.message_handler(state=Registration.code)
async def get_pokaznik(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    async with state.proxy() as data:
        data['code'] = message.text
    res = await codeValid(message.text)
    if res:
        await message.answer("Код прийнято. Введіть ваше Імя")
        await Registration.next()
    else:
        await message.answer("Код невірний. Доступ заборонено")
        await state.finish()
        raise CancelHandler()


@dp.message_handler(state=Registration.name)
async def get_pokaznik(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    async with state.proxy() as data:
        data['name'] = message.text
    await Registration.next()
    await message.answer("Введіть додаткову інформацію!")


@dp.message_handler(state=Registration.info)
async def get_pokaznik(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    async with state.proxy() as data:
        data['info'] = message.text
    await userRegistration(name=data['name'], info=data['info'], cod=data['code'],telegramId=message.from_user.id)
    await state.finish()
    await message.answer(f"Реєстрацію Завершено - {data['name']} - {data['info']}")


@dp.message_handler(state=Publications.data)
async def get_pokaznik(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await message.answer("Напишіть ціну")
    await Publications.next()


@dp.message_handler(state=Publications.sum)
async def get_pokaznik(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sum'] = message.text
    await message.answer("Опишіть дозволи")
    await Publications.next()


@dp.message_handler(state=Publications.allowed)
async def get_pokaznik(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['alowed'] = message.text
    await message.answer("Additional information")
    await Publications.next()


@dp.message_handler(state=Publications.text)
async def get_pokaznik(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer(f"Information add - {data['date']} - {data['sum']}- {data['alowed']}- {data['text']}")
    await addPublications(telegid=message.from_user.id,date =data['date'], sum=data['sum'], allowed=data['alowed'], text=data['text'])
    await state.finish()


if TEST_MODE:
    print("Bot running")
    #dp.middleware.setup(MidlWare())
    executor.start_polling(dp, skip_updates=True)
else:
    async def on_startup(dp):
        await bot.set_webhook(WEBHOOK_URL)

    async def on_shutdown(dp):

        await bot.delete_webhook()
        await dp.storage.close()
        await dp.storage.wait_closed()

    if __name__ == '__main__':
       # dp.middleware.setup(MidlWare())
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )


