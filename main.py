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
from ai import ai_response_course_info
from test import get_random_questions
from api import create_user

TOKEN = config('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
ChannelName = "@LingUp"


with open("data.json", "r", encoding="utf-8") as file:
    translations = json.load(file)




def get_text(lang, category, key):
    return translations.get(lang, {}).get(category, {}).get(key, f"[{key}]")

correct_languages = {
    "uz": "🇺🇿 uz",
    "ru": "🇷🇺 ru",
    "eng": "🇺🇸 eng",
}


@router.message(F.text.startswith("/start"))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        with open("user_lang.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            lang = data.get("user_lang", {}).get(str(user_id), [])[-1]
            lang = correct_languages[lang.split(" ")[1]]
            user = data.get("user", [])

            if user_id in user:
                await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
                await state.set_state(UserState.mainmenucheck)
                await state.update_data(language=lang)
            else:
                raise ValueError(f"User {user_id} not found in the user list.")  # Handle missing user
    except Exception as e:
        print(f"An error occurred: {e}")  # Print the error to debug
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

    # Check if the name consists of alphabetic characters and spaces
    if not all(i.isalpha() or i.isspace() for i in message.text):
        await bot.send_message(chat_id=user_id, text=get_text(lang, 'message_text', 'error_name'))
        ok = False

    # If valid, update user data and send confirmation
    if ok:
        await state.update_data(user_name=message.text)
        msg_text = (
            f"{get_text(lang, 'message_text', 'confirmed_userinfo')}\n"
            f"{get_text(lang, 'message_text', 'conf_phone')} {data['phone']}\n"
            f"{get_text(lang, 'message_text', 'conf_name')} {message.text}"
        )
        await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=kb.conf(lang))
        await state.set_state(UserState.conf)




@router.message(UserState.conf)
async def conf(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']

    file_path = "user_lang.json"
    if message.text == get_text(lang, "buttons", "confirm"):
        await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        await bot.send_chat_action(chat_id=user_id, action=ChatAction.TYPING)
        msg_text = (
            f"{get_text(lang, 'message_text', 'telefon')} {data['phone']}\n"
            f"{get_text(lang, 'message_text', 'ismi')} {data['user_name']}"
        )
        if create_user(data["user_name"], data["phone"], user_id):
            try:
                await bot.send_message(chat_id=-4937963060, text=msg_text, reply_markup=kb.user_account(user_id, lang))
            except Exception as e:
                print(f"Can't send message to channel: {e}")

            await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
            await state.set_state(UserState.mainmenucheck)

            file_path = "user_lang.json"
            user_data = {"user_lang": {}, "user": []}

            # Fayl mavjud emas yoki bo'sh bo'lsa, yangi yaratish
            try:
                with open(file_path, "r") as file:
                    user_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                # Fayl bo'sh yoki yaroqsiz bo'lsa, yangi yaratish
                user_data = {"user_lang": {}, "user": []}

            # Yangi ma'lumotlarni qo'shish
            if user_id not in user_data["user"]:
                user_data["user_lang"][str(user_id)] = [lang.split(" ")[1]]
                user_data["user"].append(user_id)

            # Ma'lumotlarni faylga yozish
            with open(file_path, "w", encoding="utf-8") as w:
                json.dump(user_data, w, ensure_ascii=False, indent=4)

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
        await bot.send_location(chat_id=user_id, latitude=41.3319662, longitude=69.3715129)
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

    elif message.text == get_text(lang, "buttons", "change_lang"):
        await message.answer(text=get_text(lang, 'message_text', 'change_language'), reply_markup=kb.change_language(lang))
        await state.set_state(UserState.change_language)


@router.message(UserState.change_language)
async def change_language(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']

    if message.text == get_text(lang, "buttons", "back"):  # "Back" tugmasi bosilsa
        await message.answer(text=get_text(lang, 'message_text', 'menu'), reply_markup=kb.menu(lang))
        await state.set_state(UserState.mainmenucheck)

    elif message.text in {"🇺🇸 eng", "🇺🇿 uz", "🇷🇺 ru"}:  # Yangi tilni tanladi
        new_lang = message.text
        await state.update_data(language=new_lang)

        file_path = "user_lang.json"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if str(user_id) in data['user_lang']:
                data['user_lang'][str(user_id)] = [new_lang.split(" ")[1]]
            else:
                data['user_lang'][str(user_id)] = [new_lang.split(" ")[1]]

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            await message.answer(text=get_text(new_lang, 'message_text', 'language_changed'))
            await message.answer(text=get_text(new_lang, 'message_text', 'menu'), reply_markup=kb.menu(new_lang))
            await state.set_state(UserState.mainmenucheck)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")





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
        return

    if message.text == get_text(lang, "buttons", "test_start"):
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
            reply_markup=ReplyKeyboardRemove()
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
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(UserState.questions)







