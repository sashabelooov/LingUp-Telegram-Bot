from google import generativeai as genai
from decouple import config



async def ai_response(lang: str, message_text: str):
    try:
        api_key = config('GEMINI_API_KEY')
        genai.configure(api_key=api_key)

        # Modelni chaqirish
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Tilga mos aniq prompt
        if lang.endswith("uz"):
            prompt = (
                "Quyidagi savolga faqat bitta aniq, tushunarli va foydalanuvchiga mos javob yoz. "
                "Javob qisqa, samimiy va markdown belgilari (*, **) bo‘lmagan holda bo‘lsin. "
                f"Savol: {message_text}"
            )
        elif lang.endswith("ru"):
            prompt = (
                "Дай только один точный, понятный и дружелюбный ответ на следующий вопрос. "
                "Ответ должен быть коротким и без форматирования (без *, **). "
                f"Вопрос: {message_text}"
            )
        elif lang.endswith("en"):
            prompt = (
                "Give only one clear, short, and friendly answer to the following question. "
                "Avoid markdown or formatting characters (*, **). "
                f"Question: {message_text}"
            )
        else:
            prompt = (
                "Berilgan savolga faqat bitta aniq va qisqa javob yoz. Formatlash belgilarisiz yoz. "
                f"Savol: {message_text}"
            )

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("Xatolik:", e)



async def ai_response_course_info(lang: str, message_text: str):
    try:
        api_key = config('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        if lang.endswith("uz"):
            prompt = f"""Foydalanuvchi quyidagi savolni berdi. LingUp LC onlayn o‘quv markazi haqida aniq va faktlarga asoslangan javob bering, foydalanuvchining savoliga tegishli bo‘limga e’tibor qaratgan holda.

Javob quyidagi talablarga mos bo‘lsin:
- Markdown belgilari (*, **) ishlatilmasin.
- Emoji-lar faqat zarur joylarda qo‘llansin (masalan: 💻, 🎯, 📝) va ortiqcha ishlatilmasin.
- Agar savol ma’lum bir bo‘limga tegishli bo‘lsa, faqat o‘sha bo‘limga oid ma’lumotlarni yozing (boshqa bo‘limlarni kiritmang).
- Agar savol umumiy xarakterga ega bo‘lsa, barcha bo‘limlar haqida qisqacha ma’lumot bering.
- Agar savol mavzuga aloqador bo‘lmasa, javobda "hozircha bu mavzuga oid ma’lumot topilmadi." deb yozing.
- Javob juda qisqa ham, juda uzun ham bo‘lmasin; o‘rtacha hajmda, lo‘nda va ravon bo‘lsin.

Savol: {message_text}

Ma’lumot:
LingUp LC — ingliz tilini o‘rganmoqchi bo‘lganlar uchun zamonaviy onlayn o‘quv markazi.

🌐 Darslar shakli:
- Barcha mashg‘ulotlar 100% onlayn tarzda o‘tkaziladi 💻
- Mashg‘ulotlar Zoom, Google Meet va LingUp’ning o‘z platformasida olib boriladi 🎥

📚 Kurslar:
- Ingliz tili kurslari: boshlang‘ich (Beginner) darajadan to Advanced darajagacha 📈
- IELTS imtihoniga tayyorlov kurslari 🎯
- Speaking, Listening, Vocabulary bo‘yicha maxsus darslar 🗣️

👩‍🏫 O‘qituvchilar:
- Darslarni tajribali va sertifikatlangan mutaxassislar olib boradi 🏅
- Har bir o‘quvchiga individual yondashuv ta’minlanadi 🤝

🎉 Afzalliklar:
- Moslashuvchan dars jadvali ⏰
- Interaktiv va o‘yinlashtirilgan darslar 🎮
- Muntazam testlar va oraliq baholash 📝
- O‘quvchilar uchun yopiq Telegram guruhlari 👥
"""
        elif lang.endswith("ru"):
            prompt = f"""Пользователь задал следующий вопрос. Пожалуйста, дайте чёткий, точный и релевантный ответ о LingUp LC (современном онлайн-центре для изучения английского языка), строго по теме вопроса и используя только приведённую ниже информацию.

Требования к ответу:
- Не используйте форматирование Markdown (символы *, **).
- Эмодзи используйте только там, где это уместно (например: 💻, 🎯, 📝), и не чрезмерно.
- Если вопрос касается определённого раздела, ответьте только по этому разделу (не упоминайте другие).
- Если вопрос носит общий характер, дайте краткое описание всех соответствующих разделов.
- Если вопрос не относится к этой теме, ответ должен быть: "на данный момент информация по этому вопросу недоступна".
- Ответ должен быть умеренной длины: не слишком коротким, но и не слишком длинным; информативным и по делу.

Вопрос: {message_text}

Информация:
LingUp LC — современный онлайн-центр для изучения английского языка.

🌐 Формат занятий:
- Все уроки проходят в 100% онлайн-формате 💻
- Используются платформы: Zoom, Google Meet и собственная платформа LingUp 🎥

📚 Курсы:
- Курсы английского языка: от начального (Beginner) до продвинутого (Advanced) уровня 📈
- Подготовка к экзамену IELTS 🎯
- Отдельные уроки по Speaking, Listening и Vocabulary для улучшения навыков 🗣️

👩‍🏫 Преподаватели:
- Занятия ведут опытные и сертифицированные специалисты 🏅
- К каждому ученику применяется индивидуальный подход 🤝

🎉 Преимущества:
- Гибкий график занятий ⏰
- Интерактивные и игровые уроки 🎮
- Регулярные тесты и промежуточная оценка прогресса 📝
- Закрытые группы в Telegram для учеников 👥
"""
        elif lang.endswith("en"):
            prompt = f"""The user asked the following question. Please provide a clear, factual, and relevant answer about LingUp LC (a modern online English learning center), focusing strictly on the user's question and using only the information provided below.

Follow these guidelines for your answer:
- Do not use any Markdown formatting (e.g., *, **).
- Use emojis only where appropriate (e.g., 💻, 🎯, 📝) and do not overuse them.
- If the question pertains to a specific section, answer using only that section’s information (do not include details from other sections).
- If the question is general, provide a brief overview of all relevant sections.
- If the question is unrelated to this topic, respond with: "no relevant information available at the moment."
- Keep the answer moderately sized — not too short and not too long — and make it concise and to the point.

Question: {message_text}

Information:
LingUp LC is a modern online center for learning English.

🌐 Lesson format:
- All classes are conducted 100% online 💻
- Platforms used include Zoom, Google Meet, and LingUp’s own platform 🎥

📚 Courses:
- English courses from Beginner to Advanced levels 📈
- IELTS exam preparation courses 🎯
- Special lessons focusing on Speaking, Listening, and Vocabulary skills 🗣️

👩‍🏫 Teachers:
- Classes are led by experienced and certified professionals 🏅
- An individual approach is provided for each student 🤝

🎉 Advantages:
- Flexible class schedule ⏰
- Interactive, gamified lessons 🎮
- Regular tests and progress assessments 📝
- Private Telegram groups for students 👥
"""
        else:
            prompt = f"""The user asked: {message_text}

You are an assistant for LingUp LC (an online English learning center). Provide a clear, factual, and relevant answer based on the LingUp LC information. The answer should be in the same language as the question, well-written, and include appropriate emojis where relevant. Do not use any Markdown formatting.

Information:
LingUp LC is a modern online center for learning English.
🌐 Lesson format: 100% online classes via Zoom, Google Meet, and LingUp’s platform 💻🎥
📚 Courses: English courses (Beginner to Advanced), IELTS preparation, Speaking/Listening/Vocabulary lessons 📈🎯🗣️
👩‍🏫 Teachers: Experienced, certified professionals; individual approach for each student 🏅🤝
🎉 Advantages: Flexible schedule, interactive gamified lessons, regular tests/progress checks, private Telegram groups ⏰🎮📝👥
"""
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("Xatolik:", e)
        return "Kechirasiz, javobni olishda xatolik yuz berdi."





# async def ai_response_course_info(lang: str, message_text: str):
#     try:
#         api_key = config('GEMINI_API_KEY')
#         genai.configure(api_key=api_key)
#
#         model = genai.GenerativeModel("gemini-2.5-flash")
#
#         if lang.endswith("uz"):
#             prompt = (
#                 f"""Foydalanuvchi quyidagi savolni berdi. Siz LingUp LC online o‘quv markazi haqida **faktlarga asoslangan va kerakli qismga yo‘naltirilgan javob** yozing.
#
#             Javob quyidagi talablarga mos bo‘lsin:
#             - Markdown (*, **) ishlatilmasin.
#             - Emoji faqat zarur joylarda ishlatilishi kerak (masalan: 💻, 🎯, 📝).
#             - Foydalanuvchining savoli qaysi bo‘limga taalluqli bo‘lsa, o‘sha bo‘limni alohida ta’kidlang.
#             - Agar savol umumiy bo‘lsa, butun tuzilmani qisqacha tushuntiring.
#             - Agar savol mavzuga aloqador bo‘lmasa, shunday deb yozing: “hozircha bu mavzuga oid ma’lumot topilmadi.”
#
#             Savol: {message_text}
#
#             Ma’lumotlar:
#             LingUp LC — ingliz tilini o‘rganmoqchi bo‘lganlar uchun zamonaviy online o‘quv markazi.
#
#             🌐 Darslar shakli:
#                - Barcha mashg‘ulotlar 100% online tarzda olib boriladi 💻
#                - Zoom, Google Meet, va LingUp platformasi 🎥
#
#
#             📚 Kurslar:
#                - Ingliz tili: Beginner'dan Advanced darajagacha 📈
#                - IELTS tayyorlov kurslari 🎯
#                - Speaking, Listening, Vocabulary darslari 🗣️
#
#             👩‍🏫 O‘qituvchilar:
#                - Tajribali va sertifikatlangan mutaxassislar 🏅
#                - Har bir o‘quvchi uchun individual yondashuv 🤝
#
#             🎉 Afzalliklar:
#                - Moslashuvchan vaqt jadvali ⏰
#                - Gamifikatsiyalangan darslar 🎮
#                - Testlar va oraliq baholash 📝
#                - Telegram yopiq guruhlar 👥
#             """
#             )
#
#
#         elif lang.endswith("ru"):
#             prompt = (
#                 f"""Пользователь задал следующий вопрос. Пожалуйста, дайте чёткий и точный ответ о современном онлайн-учебном центре **LingUp LC**, основываясь на приведённых фактах и строго по теме вопроса.
#
#             Требования к ответу:
#             - Не используйте markdown (например: *, **).
#             - Эмодзи используйте только в уместных местах (например: 💻, 🎯, 📝), не перебарщивайте.
#             - Если вопрос относится к конкретному разделу, выделите только его.
#             - Если вопрос общий, дайте краткое описание всех разделов.
#             - Если вопрос не относится к тематике, напишите: «на данный момент информация по этому вопросу недоступна».
#
#             Вопрос: {message_text}
#
#             Информация:
#             LingUp LC — это современный онлайн-центр для изучения английского языка.
#
#             🌐 Формат занятий:
#                - Все уроки проходят в 100% онлайн-формате 💻
#                - Используемые платформы: Zoom, Google Meet и собственная платформа LingUp 🎥
#
#
#             📚 Курсы:
#                - Английский язык: от уровня Beginner до Advanced 📈
#                - Подготовка к IELTS 🎯
#                - Отдельные уроки по Speaking, Listening и Vocabulary 🗣️
#
#             👩‍🏫 Преподаватели:
#                - Опытные и сертифицированные специалисты 🏅
#                - Индивидуальный подход к каждому ученику 🤝
#
#             🎉 Преимущества:
#                - Гибкий график занятий ⏰
#                - Интерактивные и игровые уроки 🎮
#                - Регулярные тесты и промежуточная оценка 📝
#                - Закрытые Telegram-группы для учеников 👥
#             """
#             )
#
#
#
#         elif lang.endswith("en"):
#             prompt = (
#                 f"""The user asked the following question. Please provide a clear and factual answer about **LingUp LC**, an online English learning center, based strictly on the user's question.
#
#             Follow these response rules:
#             - Do not use markdown formatting (such as *, **).
#             - Use emojis only where appropriate (like 💻, 🎯, 📝), do not overuse them.
#             - If the question is related to a specific section, focus only on that part.
#             - If it's a general question, briefly describe all relevant sections.
#             - If the question is unrelated to this topic, respond with: “no relevant information available at the moment.”
#
#             Question: {message_text}
#
#             Information:
#             LingUp LC is a modern online education center for learning English.
#
#             🌐 Lesson format:
#                - All classes are 100% online 💻
#                - Platforms used: Zoom, Google Meet, and LingUp's own platform 🎥
#
#
#             📚 Courses:
#                - English: from Beginner to Advanced 📈
#                - IELTS preparation 🎯
#                - Special lessons for Speaking, Listening, and Vocabulary 🗣️
#
#             👩‍🏫 Teachers:
#                - Conducted by experienced and certified professionals 🏅
#                - Individual approach for every student 🤝
#
#             🎉 Advantages:
#                - Flexible schedule ⏰
#                - Interactive and gamified lessons 🎮
#                - Regular tests and progress assessments 📝
#                - Private Telegram groups for students 👥
#             """
#             )
#
#
#
#         else:
#             prompt = (
#                 "Foydalanuvchi savoliga chiroyli, toza, emoji bilan boyitilgan va tushunarli javob yozing. Markdown ishlatilmasin.\n"
#                 f"Savol: {message_text}"
#             )
#
#         response = model.generate_content(prompt)
#         return response.text.strip()
#
#     except Exception as e:
#         print("Xatolik:", e)
#         return "Kechirasiz, javobni olishda xatolik yuz berdi."
#
#
