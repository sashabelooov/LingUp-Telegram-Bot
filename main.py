import json
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import  Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from decouple import config
from aiogram.enums import ChatAction
from aiogram.types import PollAnswer
from aiogram import F


# local modules
from state import UserState
import keyboards as kb
from ai import ai_response, ai_response_course_info, ai_test
from test import get_random_questions

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

    question, answer = await get_random_questions()

    await state.update_data(correct_answer=int(answer))
    await state.update_data(counter=0)
    await state.update_data(total_questions=1)

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question[0],
        options=[
            f"A) {question[1]}", f"B) {question[2]}",
            f"C) {question[3]}", f"D) {question[4]}"
        ],
        is_anonymous=False,
        allows_multiple_answers=False,
        reply_markup=kb.back(lang)
    )

    await state.set_state(UserState.questions)




@router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    data = await state.get_data()
    lang = data['language']
    user_id = poll_answer.user.id
    selected = poll_answer.option_ids[0]

    correct = data.get("correct_answer")
    counter = data.get("counter", 0)
    total = data.get("total_questions", 1)

    # To‘g‘ri javob bo‘lsa, counter ni oshiramiz
    if selected == correct:
        counter += 1

    total += 1

    if total > 10:
        msg_text = get_text(lang, 'message_text', 'result_test')
        replace_counter = msg_text.format(counter=counter)

        await bot.send_message(chat_id=user_id, text=replace_counter, reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
        await state.set_state(UserState.mainmenucheck)
        return

    # Yangi savol yuboriladi
    question, answer = await get_random_questions()
    await state.update_data(correct_answer=int(answer))
    await state.update_data(counter=counter)
    await state.update_data(total_questions=total)

    await bot.send_poll(
        chat_id=user_id,
        question=question[0],
        options=[
            f"A) {question[1]}", f"B) {question[2]}",
            f"C) {question[3]}", f"D) {question[4]}"
        ],
        is_anonymous=False,
        allows_multiple_answers=False,
        reply_markup=kb.back(lang)
    )

    await state.set_state(UserState.questions)







