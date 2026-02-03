import json
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove


def letter_to_index(letter: str) -> int:
    letter = (letter or "").strip().upper()
    return ord(letter) - ord("A")


def safe_poll_option(text: str, limit: int = 100) -> str:
    text = (text or "").strip().replace("\n", " ")
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


with open("cefr_grammar_test_50_lingupuz.cleaned.json", "r", encoding="utf-8") as f:
    TEST_DATA = json.load(f)

tests = TEST_DATA["tests"]
score_levels = TEST_DATA.get("meta", {}).get("score_levels", [])


def get_cefr_level(score: int) -> str:
    for rule in score_levels:
        if rule["min"] <= score <= rule["max"]:
            return rule["level"]
    return "Unknown"


async def send_next_question(bot, state: FSMContext, chat_id: int, limit: int = 50) -> bool:
    data = await state.get_data()

    level = data["level"]
    q_keys = data["q_keys"]
    q_index = int(data.get("q_index", 0))
    total = int(data.get("total_questions", 0))

    if total >= limit or q_index >= len(q_keys):
        return False

    qnum = q_keys[q_index]
    qobj = tests[level]["questions"][qnum]

    question_text = (qobj["question"] or "").strip()
    options = [safe_poll_option(x) for x in list(qobj["options"])]

    correct_letter = tests[level]["answers"][qnum]
    correct_index = letter_to_index(correct_letter)

    if not (0 <= correct_index < len(options)):
        raise ValueError(
            f"Bad test data: question_num={qnum}, answer={correct_letter}, options={len(options)}"
        )

    await state.update_data(
        correct_answer=int(correct_index),
        q_index=q_index + 1,
        total_questions=total + 1,
    )

    await bot.send_poll(
        chat_id=chat_id,
        question=question_text,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=False,
        reply_markup=ReplyKeyboardRemove(),
    )
    return True