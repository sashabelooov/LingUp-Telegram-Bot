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
                "Foydalanuvchiga quyidagi tartibda aniq, tushunarli, chiroyli va emoji bilan boyitilgan javob yozing.\n"
                "Markdown belgilaridan (*, **) foydalanmang. Javob quyidagi shaklda bo‘lishi kerak:\n"
                "\n"
                "Salom! 👋 Aim Academy (Act In Maximum) o‘quv markazi haqida ma’lumot:\n"
                "\n"
                "📍 Joylashuv:\n"
                "   - Asosiy filial: Qorasuv-3 massivi, 14-uy 🏡\n"
                "   - Ikkinchi filial: Qorasuv-1 massivi, 23-uy 🏫\n"
                "\n"
                "📞 Telefon: +998 33 7000224 ☎️\n"
                "✉️ Email: aimacademy224@gmail.com 📧\n"
                "\n"
                "📚 Kurslar:\n"
                "   - Ingliz tili kurslari zamonaviy metodikalar 🚀 asosida o‘tiladi\n"
                "   - Malakali o‘qituvchilar tomonidan darslar olib boriladi 👩‍🏫\n"
                "\n"
                "🎯 Qo‘shimcha:\n"
                "   - Interaktiv darslar 💡\n"
                "   - Amaliy mashg‘ulotlar ✍️ orqali o‘quvchilar tilni tez va samarali o‘zlashtiradi\n"
                "   - Yuksak natijalarga erishishga yordam beradi 🏆\n"
                "\n"
                "Agar bu ma’lumotga aloqador savol bo‘lmasa, «hozircha ma’lumot topilmadi» deb yozing.\n"
                f"Savol: {message_text}"
            )

        elif lang.endswith("ru"):
            prompt = (
                "Ответьте пользователю чётко, понятно, красиво, с эмодзи и без использования markdown. Структурируйте текст так:\n"
                "\n"
                "Привет! 👋 Вот информация об учебном центре Aim Academy (Act In Maximum):\n"
                "\n"
                "📍 Адрес:\n"
                "   - Главный филиал: массив Карасу-3, дом 14 🏡\n"
                "   - Второй филиал: массив Карасу-1, дом 23 🏫\n"
                "\n"
                "📞 Телефон: +998 33 7000224 ☎️\n"
                "✉️ Почта: aimacademy224@gmail.com 📧\n"
                "\n"
                "📚 Курсы:\n"
                "   - Курсы английского языка с современными методиками 🚀\n"
                "   - Преподаватели — опытные и квалифицированные 👩‍🏫\n"
                "\n"
                "🎯 Дополнительно:\n"
                "   - Интерактивные занятия 💡\n"
                "   - Практические упражнения ✍️ помогают быстро освоить язык\n"
                "   - Достижение высоких результатов 🏆\n"
                "\n"
                "Если вопрос не связан с этим, напишите: «информация в настоящее время недоступна».\n"
                f"Вопрос: {message_text}"
            )

        elif lang.endswith("en"):
            prompt = (
                "Reply clearly, beautifully, and understandably. Do not use markdown. Use emojis only where appropriate. Format the response like this:\n"
                "\n"
                "Hello! 👋 Here's information about Aim Academy (Act In Maximum):\n"
                "\n"
                "📍 Location:\n"
                "   - Main branch: Qorasuv-3 district, House 14 🏡\n"
                "   - Second branch: Qorasuv-1 district, House 23 🏫\n"
                "\n"
                "📞 Phone: +998 33 7000224 ☎️\n"
                "✉️ Email: aimacademy224@gmail.com 📧\n"
                "\n"
                "📚 Courses:\n"
                "   - English language classes with modern methods 🚀\n"
                "   - Taught by qualified and experienced teachers 👩‍🏫\n"
                "\n"
                "🎯 Additional Info:\n"
                "   - Interactive lessons 💡\n"
                "   - Practical exercises ✍️ for fast and effective learning\n"
                "   - Helps students achieve excellent results 🏆\n"
                "\n"
                "If the user's question is unrelated, just reply with: “no information available at this time.”\n"
                f"Question: {message_text}"
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





async def ai(lang: str):
    try:
        api_key = config('GEMINI_API_KEY')
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash")

        if lang.endswith("uz"):
            prompt = (
                "Kurs narxini foydalanuvchiga chiroyli, aniq va ishonchli tarzda yoz. "
                "Faqat bitta aniq javob yozing. Markdown yoki belgilarsiz yozing (masalan: *, ** ishlatma). "
                "Kurs narxi: 499 000 so'm. Oddiy va professional uslubda yoz."
            )
        elif lang.endswith("ru"):
            prompt = (
                "Напиши информацию о цене курса красиво, понятно и дружелюбно. "
                "Ответ должен быть точным и без каких-либо символов разметки (без *, ** и т.п.). "
                "Цена курса: 499 000 сум. Используй простой и профессиональный стиль."
            )
        elif lang.endswith("eng"):
            prompt = (
                "Write a clear and friendly message about the course price. "
                "Only return one clean sentence. Do not use any markdown or formatting symbols like * or **. "
                "The price is 499,000 UZS. Use simple and professional language."
            )
        else:
            prompt = "Kurs narxi: 499 000 so'm. Oddiy matn formatida yoz."

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(e)