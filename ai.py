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
            prompt = (
                f"""Foydalanuvchi quyidagi savolni berdi. Siz LingUp LC online o‘quv markazi haqida **faktlarga asoslangan va kerakli qismga yo‘naltirilgan javob** yozing.

            Javob quyidagi talablarga mos bo‘lsin:
            - Markdown (*, **) ishlatilmasin.
            - Emoji faqat zarur joylarda ishlatilishi kerak (masalan: 💻, 🎯, 📝).
            - Foydalanuvchining savoli qaysi bo‘limga taalluqli bo‘lsa, o‘sha bo‘limni alohida ta’kidlang.
            - Agar savol umumiy bo‘lsa, butun tuzilmani qisqacha tushuntiring.
            - Agar savol mavzuga aloqador bo‘lmasa, shunday deb yozing: “hozircha bu mavzuga oid ma’lumot topilmadi.”

            Savol: {message_text}

            Ma’lumotlar:
            LingUp LC — ingliz tilini o‘rganmoqchi bo‘lganlar uchun zamonaviy online o‘quv markazi.

            🌐 Darslar shakli:
               - Barcha mashg‘ulotlar 100% online tarzda olib boriladi 💻
               - Zoom, Google Meet, va LingUp platformasi 🎥


            📚 Kurslar:
               - Ingliz tili: Beginner'dan Advanced darajagacha 📈
               - IELTS tayyorlov kurslari 🎯
               - Speaking, Listening, Vocabulary darslari 🗣️

            👩‍🏫 O‘qituvchilar:
               - Tajribali va sertifikatlangan mutaxassislar 🏅
               - Har bir o‘quvchi uchun individual yondashuv 🤝

            🎉 Afzalliklar:
               - Moslashuvchan vaqt jadvali ⏰
               - Gamifikatsiyalangan darslar 🎮
               - Testlar va oraliq baholash 📝
               - Telegram yopiq guruhlar 👥
            """
            )


        elif lang.endswith("ru"):
            prompt = (
                f"""Пользователь задал следующий вопрос. Пожалуйста, дайте чёткий и точный ответ о современном онлайн-учебном центре **LingUp LC**, основываясь на приведённых фактах и строго по теме вопроса.

            Требования к ответу:
            - Не используйте markdown (например: *, **).
            - Эмодзи используйте только в уместных местах (например: 💻, 🎯, 📝), не перебарщивайте.
            - Если вопрос относится к конкретному разделу, выделите только его.
            - Если вопрос общий, дайте краткое описание всех разделов.
            - Если вопрос не относится к тематике, напишите: «на данный момент информация по этому вопросу недоступна».

            Вопрос: {message_text}

            Информация:
            LingUp LC — это современный онлайн-центр для изучения английского языка.

            🌐 Формат занятий:
               - Все уроки проходят в 100% онлайн-формате 💻
               - Используемые платформы: Zoom, Google Meet и собственная платформа LingUp 🎥


            📚 Курсы:
               - Английский язык: от уровня Beginner до Advanced 📈
               - Подготовка к IELTS 🎯
               - Отдельные уроки по Speaking, Listening и Vocabulary 🗣️

            👩‍🏫 Преподаватели:
               - Опытные и сертифицированные специалисты 🏅
               - Индивидуальный подход к каждому ученику 🤝

            🎉 Преимущества:
               - Гибкий график занятий ⏰
               - Интерактивные и игровые уроки 🎮
               - Регулярные тесты и промежуточная оценка 📝
               - Закрытые Telegram-группы для учеников 👥
            """
            )



        elif lang.endswith("en"):
            prompt = (
                f"""The user asked the following question. Please provide a clear and factual answer about **LingUp LC**, an online English learning center, based strictly on the user's question.

            Follow these response rules:
            - Do not use markdown formatting (such as *, **).
            - Use emojis only where appropriate (like 💻, 🎯, 📝), do not overuse them.
            - If the question is related to a specific section, focus only on that part.
            - If it's a general question, briefly describe all relevant sections.
            - If the question is unrelated to this topic, respond with: “no relevant information available at the moment.”

            Question: {message_text}

            Information:
            LingUp LC is a modern online education center for learning English.

            🌐 Lesson format:
               - All classes are 100% online 💻
               - Platforms used: Zoom, Google Meet, and LingUp's own platform 🎥


            📚 Courses:
               - English: from Beginner to Advanced 📈
               - IELTS preparation 🎯
               - Special lessons for Speaking, Listening, and Vocabulary 🗣️

            👩‍🏫 Teachers:
               - Conducted by experienced and certified professionals 🏅
               - Individual approach for every student 🤝

            🎉 Advantages:
               - Flexible schedule ⏰
               - Interactive and gamified lessons 🎮
               - Regular tests and progress assessments 📝
               - Private Telegram groups for students 👥
            """
            )



        else:
            prompt = (
                "Foydalanuvchi savoliga chiroyli, toza, emoji bilan boyitilgan va tushunarli javob yozing. Markdown ishlatilmasin.\n"
                f"Savol: {message_text}"
            )

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print("Xatolik:", e)
        return "Kechirasiz, javobni olishda xatolik yuz berdi."




async def ai_test(lang: str):
    try:
        api_key = config('GEMINI_API_KEY')
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")

        if lang.endswith("uz"):
            prompt = (
                "Iltimos, menga ingliz tili bo‘yicha test shaklida 10 ta savol va ularning to‘g‘ri javoblarini tuzib bering. Har bir savol variantli bo‘lsin. Format quyidagicha bo‘lsin:\n\n"
                "1. Savol matni\n"
                "   A) variant A\n"
                "   B) variant B\n"
                "   C) variant C\n"
                "   D) variant D\n"
                "   To‘g‘ri javob: B\n\n"
                "Darajalar quyidagicha bo‘lsin:\n"
                "- Beginner (2 ta savol)\n"
                "- Elementary (2 ta savol)\n"
                "- Pre-Intermediate (2 ta savol)\n"
                "- Intermediate (2 ta savol)\n"
                "- Upper-Intermediate (2 ta savol)\n\n"
                "Savollar grammatika, so‘z boyligi yoki tushunishga oid bo‘lishi mumkin.\n"
                "Savollar va javoblar faqat ingliz tilida bo‘lsin."
            )

        elif lang.endswith("ru"):
            prompt = (
                "Пожалуйста, составь 10 тестовых вопросов по английскому языку с вариантами ответов и укажи правильный вариант. Формат:\n\n"
                "1. Вопрос\n"
                "   A) Вариант A\n"
                "   B) Вариант B\n"
                "   C) Вариант C\n"
                "   D) Вариант D\n"
                "   Правильный ответ: C\n\n"
                "Уровни сложности:\n"
                "- Beginner (2 вопроса)\n"
                "- Elementary (2 вопроса)\n"
                "- Pre-Intermediate (2 вопроса)\n"
                "- Intermediate (2 вопроса)\n"
                "- Upper-Intermediate (2 вопроса)\n\n"
                "Темы могут быть связаны с грамматикой, лексикой или пониманием текста.\n"
                "Все вопросы и ответы должны быть написаны только на английском языке."
            )

        elif lang.endswith("eng"):
            prompt = (
                    "Please create 10 multiple-choice English test questions, with answers included. Use this format:\n\n"
                    "1. Question text\n"
                    "   A) Option A\n"
                    "   B) Option B\n"
                    "   C) Option C\n"
                    "   D) Option D\n"
                    "   Correct answer: A\n\n"
                    "Levels:\n"
                    "- Beginner (2 questions)\n"
                    "Elementary (2 questions)\n"
                  "- Pre-Intermediate (2 questions)\n"
                  "- Intermediate (2 questions)\n"
                  "- Upper-Intermediate (2 questions)\n\n"
                  "The questions can be about grammar, vocabulary, or reading comprehension.\n"
                  "All content must be in English."
            )

        else:
            prompt = "Iltimos, menga ingliz tili bo‘yicha test shaklida 10 ta savol va ularning to‘g‘ri javoblarini tuzib bering. Har bir savol variantli bo‘lsin. Format quyidagicha bo‘lsin:\n\n"


        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(e)



# async def ai(lang: str):
#     try:
#         api_key = config('GEMINI_API_KEY')
#         genai.configure(api_key=api_key)
#
#         model = genai.GenerativeModel("gemini-2.5-flash")
#
#         if lang.endswith("uz"):
#             prompt = (
#                 "Kurs narxini foydalanuvchiga chiroyli, aniq va ishonchli tarzda yoz. "
#                 "Faqat bitta aniq javob yozing. Markdown yoki belgilarsiz yozing (masalan: *, ** ishlatma). "
#                 "Kurs narxi: 499 000 so'm. Oddiy va professional uslubda yoz."
#             )
#         elif lang.endswith("ru"):
#             prompt = (
#                 "Напиши информацию о цене курса красиво, понятно и дружелюбно. "
#                 "Ответ должен быть точным и без каких-либо символов разметки (без *, ** и т.п.). "
#                 "Цена курса: 499 000 сум. Используй простой и профессиональный стиль."
#             )
#         elif lang.endswith("eng"):
#             prompt = (
#                 "Write a clear and friendly message about the course price. "
#                 "Only return one clean sentence. Do not use any markdown or formatting symbols like * or **. "
#                 "The price is 499,000 UZS. Use simple and professional language."
#             )
#         else:
#             prompt = "Kurs narxi: 499 000 so'm. Oddiy matn formatida yoz."
#
#         response = model.generate_content(prompt)
#         return response.text.strip()
#     except Exception as e:
#         print(e)
