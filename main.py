import json
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, PollAnswer
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from decouple import config
from aiogram.enums import ChatAction


# local modules
from state import UserState
import keyboards as kb
from ai import ai_response, ai_response_course_info, ai_test
from test import *

# from api import create_user, get_user_info_by_tg_id

TOKEN = config('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
ChannelName = "@zayavkalar_infosi"


with open("data.json", "r", encoding="utf-8") as file:
    translations = json.load(file)


def get_text(lang, category, key):
    return translations.get(lang, {}).get(category, {}).get(key, f"[{key}]")


user_lang = {"uz":"🇺🇿 uz", "eng":"🇺🇸 eng", "ru":"🇷🇺 ru"}
@router.message(F.text.startswith("/start"))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    # try:
        # if get_user_info_by_tg_id(user_id):
        #     lang = get_user_info_by_tg_id(user_id)["language"]
        #     lang = user_lang[lang]
        #     await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
        #     await state.set_state(UserState.mainmenucheck)
        #     await state.update_data(language=lang)
    # except:
    await bot.send_message(
        chat_id=user_id,
        text=translations['start'],
        reply_markup=kb.start_key(),
        parse_mode='HTML'
    )
    await state.set_state(UserState.language)


@router.message(UserState.language)
async def ask_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text in {"🇺🇸 eng":"🇺🇸 eng","🇺🇿 uz":"🇺🇿 uz","🇷🇺 ru":"🇷🇺 ru",}:
        await state.update_data(language=message.text)
        data = await state.get_data()
        lang = data['language']
        await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'phone'), reply_markup=kb.ask_phone(lang))
        await state.set_state(UserState.phone)



@router.message(UserState.phone)
async def check_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'name'), reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserState.fio)
    else:
        text = message.text
        if message.text.startswith("+998") and len(text) == 13 and text[1:].isdigit():
            await state.update_data(phone=message.text)
            await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'name'), reply_markup=ReplyKeyboardRemove())
            await state.set_state(UserState.fio)
        else:
            await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'error_phone'))



@router.message(UserState.fio)
async def fio_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    ok = True
    for i in message.text:
        if not i.isalpha():
            await bot.send_message(chat_id=user_id,text=get_text(lang, 'message_text', 'error_name'))
            ok = False
            break
    if ok:
        await state.update_data(user_name=message.text)
        msg_text = (
            f"{get_text(lang, 'message_text', 'confirmed_userinfo')}\n"
            f"{get_text(lang, 'message_text', 'conf_phone')} {data["phone"]}\n"
            f"{get_text(lang, 'message_text', 'conf_name')} {message.text}"
        )

        await bot.send_message(chat_id=user_id,text=msg_text, reply_markup=kb.conf(lang))
        await state.set_state(UserState.conf)



@router.message(UserState.conf)
async def conf(message: Message, state: FSMContext):
     user_id = message.from_user.id
     data = await state.get_data()
     lang = data['language']
     if message.text == get_text(lang, "buttons", "confirm"):
         msg_text = (
             f"{get_text(lang, 'message_text', 'telefon')} {data["phone"]}\n"
             f"{get_text(lang, 'message_text', 'ismi')} {data["user_name"]}"
         )

         await bot.send_message(chat_id=ChannelName, text=msg_text, reply_markup=kb.user_account(user_id, lang))
         await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
         await state.set_state(UserState.mainmenucheck)
         # if create_user(user_id, data["phone"], data["user_name"], lang):
         #     msg_text = (
         #         f"{get_text(lang, 'message_text', 'telefon')} {data["phone"]}\n"
         #         f"{get_text(lang, 'message_text', 'ismi')} {data["user_name"]}"
         #     )
         #
         #     await bot.send_message(chat_id=ChannelName, text=msg_text, reply_markup=kb.user_account(user_id,lang))
         #     await message.answer(text=get_text(lang, 'message_text', 'menu'),reply_markup=kb.menu(lang))
         #     await state.set_state(UserState.mainmenucheck)
         # else:
         #     await message.answer(text=create_user(user_id, data["phone"], data["user_name"], lang), reply_markup=kb.conf(lang))
     elif message.text == get_text(lang, "buttons", "rejected"):
         await bot.send_message(
             chat_id=user_id,
             text=translations['start'],
             reply_markup=kb.start_key(),
             parse_mode='HTML'
         )
         await state.set_state(UserState.language)




# ******** CHECK MAIN MENU BUTTONS ******** #
@router.message(UserState.mainmenucheck)
async def main_menu_check(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "loc"):
        await bot.send_location(chat_id=user_id, latitude=41.3340125, longitude=69.3708906)
        await message.answer(text=get_text(lang, 'message_text', 'show_location'), reply_markup=kb.back(lang))
        await state.set_state(UserState.back_from_show_location)

    elif message.text == get_text(lang, "buttons", "contact_menu"):
        await message.answer(text=get_text(lang, 'message_text', 'show_phone'), reply_markup=kb.back(lang))
        await state.set_state(UserState.back_from_show_phone)

    elif message.text == get_text(lang, "buttons", "price"):
        await message.answer(text=get_text(lang, 'message_text', 'course_price'), reply_markup=kb.back(lang))
        await state.set_state(UserState.back_from_price)

    elif message.text == get_text(lang, "buttons", "course_info_menu"):
        await message.answer(text=get_text(lang, 'message_text', 'ai'), reply_markup=kb.back(lang))
        await state.set_state(UserState.back_from_course_info_menu)
    elif message.text == get_text(lang, "buttons", "test"):
        await message.answer(text=get_text(lang, 'message_text', 'test'), reply_markup=kb.test_start(lang))
        await state.set_state(UserState.test_start)




@router.message(UserState.back_from_show_location)
async def back_from_show_location(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
    await state.set_state(UserState.mainmenucheck)



@router.message(UserState.back_from_show_phone)
async def back_from_show_phone(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
    await state.set_state(UserState.mainmenucheck)



@router.message(UserState.back_from_price)
async def back_from_price(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "back"):
        await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
        await state.set_state(UserState.mainmenucheck)
    # else:
    #     await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
    #     response_text = await ai_response(lang, message.text)
    #     await bot.send_message(chat_id=user_id, text=response_text, reply_markup=kb.back(lang))




@router.message(UserState.back_from_course_info_menu)
async def back_from_show_location(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "back"):
        await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
        await state.set_state(UserState.mainmenucheck)
    else:
        await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        response_text = await ai_response_course_info(lang, message.text)
        await bot.send_message(chat_id=user_id, text=response_text, reply_markup=kb.back(lang))



@router.message(UserState.test_start)
async def test_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == get_text(lang, "buttons", "back"):
        await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
        await state.set_state(UserState.mainmenucheck)
    elif message.text == get_text(lang, "buttons", "test_start"):
        await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        question,answer = await beginner_test(1)
        await bot.send_poll(
            chat_id=message.chat.id,
            question=f"{question[0]}",
            options=[f"A: {question[1]}", f"B: {question[2]}", f"C: {question[3]}", f"D: {question[4]}"],
            is_anonymous=True,
            allows_multiple_answers=False
        )
        await state.set_state(UserState.questions)


@router.poll_answer(UserState.questions)
async def questions(poll_answer: PollAnswer, state: FSMContext):
    # user_id = message.from_user.id
    user_id = poll_answer.user.id
    print(user_id)
    data = await state.get_data()
    lang = data['language']
    res = poll_answer.option_ids
    print(res)
