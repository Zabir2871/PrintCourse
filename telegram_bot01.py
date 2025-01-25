import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

courses = [
    {"short_name": "act", "course_code": "ACT 202", "course_name": "Financial Accounting II", "course_teacher": "Palash Saha"},
    {"short_name": "stat", "course_code": "BUS 207", "course_name": "Business Statistics II", "course_teacher": "Md. Alamgir Hossen"},
    {"short_name": "eco", "course_code": "BUS 209", "course_name": "Macroeconomics", "course_teacher": "Prof. Chowdhury Golam Kibria"},
    {"short_name": "fin", "course_code": "FIN 201", "course_name": "Introduction to Finance", "course_teacher": "Prof. Mohammad Nazmul Islam"},
    {"short_name": "ob", "course_code": "MGT 202", "course_name": "Organization Behavior", "course_teacher": "Prof. Kamrul Arefin"},
    {"short_name": "mkt", "course_code": "MKT 201", "course_name": "Introduction to Marketing", "course_teacher": "Ratul Kumar Saha"}
]

times = [
    {"cls_serial": "1", "class_time": "08:50 AM - 10:10 AM"},
    {"cls_serial": "2", "class_time": "10:15 AM - 11:35 AM"},
    {"cls_serial": "3", "class_time": "11:40 AM - 01:00 PM"},
    {"cls_serial": "4", "class_time": "01:50 PM - 03:10 PM"},
    {"cls_serial": "5", "class_time": "03:20 PM - 04:40 PM"}
]

def get_course_info(short_name):
    for course in courses:
        if course["short_name"] == short_name:
            return course
    return None

def get_class_time(cls_serial):
    for time in times:
        if time["cls_serial"] == cls_serial:
            return time["class_time"]
    return None

def get_full_date(date_str):
    current_year = datetime.datetime.now().year
    date_obj = datetime.datetime.strptime(f"{date_str} {current_year}", "%d %b %Y")
    return date_obj.strftime("%A, %B %d, %Y")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Enter the date (dd mmm), number of classes, and course short names with class serials (e.g., "25 jan, 2, act 1, stat 2"): ')

async def handle_message(update: Update, context: CallbackContext) -> None:
    try:
        input_data = update.message.text
        data_parts = input_data.split(',')

        # Extract and process the input data
        date_input = data_parts[0].strip()
        full_date = get_full_date(date_input)

        number_of_classes = int(data_parts[1].strip())
        selected_courses = []

        for i in range(2, 2 + number_of_classes):
            short_name, cls_serial = data_parts[i].strip().split()
            course_info = get_course_info(short_name)
            class_time = get_class_time(cls_serial)
            if course_info and class_time:
                selected_courses.append((class_time, course_info))
            else:
                await update.message.reply_text(f"Course with short name {short_name} or class serial {cls_serial} not found.")

        # Split the full date into parts
        day_of_week, month_day, year = full_date.split(', ')
        month_name, day = month_day.split(' ')

        response = f"\nTomorrow’s classes\n{day_of_week}\n{month_name},{day}, {year}\n"
        for class_time, course in selected_courses:
            response += f"\n{class_time}\n{course['course_code']}\n{course['course_name']}\n{course['course_teacher']}\n"

        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    application = Application.builder().token("7644001243:AAF5i1gOcvYvNvbwlZ-rJ9qx1kBJ7a_xI-A").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()