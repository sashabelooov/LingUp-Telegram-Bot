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
            prompt = f"""
            Foydalanuvchi quyidagi savolni berdi. Iltimos, aniq, faktlarga asoslangan va foydalanuvchining savoliga to'g'ri javob bering. Faol va aniq bo'ling. Emoji-lar faqat zarur joylarda ishlatilishi kerak (misol: 💻, 🎯, 📝). Keraksiz belgilar ishlatilmasin.

            Savol: {message_text}

            Ma’lumot:
            LingUp LC — ingliz tilini o‘rganmoqchi bo‘lganlar uchun zamonaviy onlayn o‘quv markazi.

            Darslar shakli:
            - Barcha mashg‘ulotlar 100% onlayn tarzda o‘tkaziladi.
            - Zoom, Google Meet va LingUp’ning o‘z platformasida olib boriladi.

            Kurslar:
            - Ingliz tili kurslari: boshlang‘ich (Beginner) darajadan to Advanced darajagacha.
            - IELTS imtihoniga tayyorlov kurslari.
            - Speaking, Listening, Vocabulary bo‘yicha maxsus darslar.

            O‘qituvchilar:
            - Darslarni tajribali va sertifikatlangan mutaxassislar olib boradi.
            - Har bir o‘quvchiga individual yondashuv ta’minlanadi.

            Afzalliklar:
            - Moslashuvchan dars jadvali.
            - Interaktiv va o‘yinlashtirilgan darslar.
            - Muntazam testlar va oraliq baholash.
            - O‘quvchilar uchun yopiq Telegram guruhlari.
            """

        elif lang.endswith("ru"):
            prompt = f"""
            Пользователь задал следующий вопрос. Пожалуйста, дайте чёткий, точный и релевантный ответ, основываясь только на предоставленной информации. Используйте эмодзи только там, где это необходимо (например: 💻, 🎯, 📝). Не добавляйте ненужные символы.

            Вопрос: {message_text}

            Информация:
            LingUp LC — современный онлайн-центр для изучения английского языка.

            Формат занятий:
            - Все уроки проходят в 100% онлайн-формате.
            - Платформы: Zoom, Google Meet и собственная платформа LingUp.

            Курсы:
            - Курсы английского языка: от начального (Beginner) до продвинутого (Advanced) уровня.
            - Подготовка к экзамену IELTS.
            - Отдельные уроки по Speaking, Listening и Vocabulary для улучшения навыков.

            Преподаватели:
            - Занятия ведут опытные и сертифицированные специалисты.
            - К каждому ученику применяется индивидуальный подход.

            Преимущества:
            - Гибкий график занятий.
            - Интерактивные и игровые уроки.
            - Регулярные тесты и промежуточная оценка прогресса.
            - Закрытые группы в Telegram для учеников.
            """

        elif lang.endswith("en"):
            prompt = f"""
            The user asked the following question. Please provide a clear, factual, and relevant answer based on the LingUp LC information, with no unnecessary symbols or emojis, only using them where appropriate (e.g., 💻, 🎯, 📝).

            Question: {message_text}

            Information:
            LingUp LC is a modern online center for learning English.

            Lesson format:
            - All classes are conducted 100% online.
            - Platforms used include Zoom, Google Meet, and LingUp’s own platform.

            Courses:
            - English courses from Beginner to Advanced levels.
            - IELTS exam preparation courses.
            - Special lessons focusing on Speaking, Listening, and Vocabulary skills.

            Teachers:
            - Classes are led by experienced and certified professionals.
            - An individual approach is provided for each student.

            Advantages:
            - Flexible class schedule.
            - Interactive, gamified lessons.
            - Regular tests and progress assessments.
            - Private Telegram groups for students.
            """

        else:
            prompt = f"""
            The user asked: {message_text}

            You are an assistant for LingUp LC (an online English learning center). Provide a clear, factual, and relevant answer based on the LingUp LC information, strictly following the user's language and using appropriate emojis where relevant. Do not use any Markdown formatting.

            Information:
            LingUp LC is a modern online center for learning English.
            Lesson format: 100% online classes via Zoom, Google Meet, and LingUp’s platform.
            Courses: English courses (Beginner to Advanced), IELTS preparation, Speaking/Listening/Vocabulary lessons.
            Teachers: Experienced, certified professionals; individual approach for each student.
            Advantages: Flexible schedule, interactive gamified lessons, regular tests/progress checks, private Telegram groups.
            """

        response = model.generate_content(prompt)
        
        cleaned_response = re.sub(r'[^\w\s,().!?&]', '', response.text.strip())
        
        return cleaned_response

    except Exception as e:
        print("Xatolik:", e)
        return "Kechirasiz, javobni olishda xatolik yuz berdi."





