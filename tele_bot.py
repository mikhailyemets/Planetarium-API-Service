import logging
import requests

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

THEMES_URL = 'http://127.0.0.1:8000/api/planetarium/themes/'
SESSIONS_URL = 'http://127.0.0.1:8000/api/planetarium/show_sessions/'
ASTRO_SHOWS_URL = 'http://127.0.0.1:8000/api/planetarium/shows/'
TICKETS_URL = 'http://127.0.0.1:8000/api/planetarium/tickets/'
DOMES_URL = 'http://127.0.0.1:8000/api/planetarium/domes/'

def build_menu():
    return [
        [
            InlineKeyboardButton("Список Сеансов", callback_data='list_sessions'),
        ],
        [
            InlineKeyboardButton("Astronomy Shows", callback_data='list_astronomy_shows'),
            InlineKeyboardButton("Planetarium Domes", callback_data='list_domes'),
        ],
        [
            InlineKeyboardButton("Список Тем", callback_data='list_themes'),
            InlineKeyboardButton("Список Билетов", callback_data='list_tickets'),
        ]
    ]

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = build_menu()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    message = ''
    if query.data == 'list_sessions':
        try:
            response = requests.get(SESSIONS_URL)
            response.raise_for_status()
            sessions = response.json()

            if isinstance(sessions, list):
                session_list = ''
                for session in sessions:
                    session_list += (
                        f"Сеанс ID: {session['id']}\n"
                        f"Шоу ID: {session['show']}\n"
                        f"Дата и время: {session['date_time']}\n\n"
                    )

                message = f"Список доступных сеансов:\n{session_list}" if session_list else "Сеансы не найдены"
            else:
                message = "Ответ от API не является списком сеансов"
        except requests.exceptions.RequestException as e:
            message = f'Ошибка при подключении к API: {e}'

    elif query.data == 'list_astronomy_shows':
        try:
            response = requests.get(ASTRO_SHOWS_URL)
            response.raise_for_status()
            shows = response.json()

            if isinstance(shows, list):
                show_list = ''
                for show in shows:
                    themes = ', '.join(show['theme'])
                    show_list += (
                        f"Шоу ID: {show['id']}\n"
                        f"Название: {show['title']}\n"
                        f"Описание: {show['description']}\n"
                        f"Темы: {themes}\n\n"
                    )

                message = f"Список доступных шоу:\n{show_list}" if show_list else "Шоу не найдены"
            else:
                message = "Ответ от API не является списком шоу"
        except requests.exceptions.RequestException as e:
            message = f'Ошибка при подключении к API: {e}'

    elif query.data == 'list_themes':
        try:
            response = requests.get(THEMES_URL)
            response.raise_for_status()
            themes = response.json()

            if isinstance(themes, list):
                theme_list = ''
                for theme in themes:
                    theme_list += f"Тема ID: {theme['id']}, Название: {theme['name']}\n"

                message = f"Список доступных тем:\n{theme_list}" if theme_list else "Темы не найдены"
            else:
                message = "Ответ от API не является списком тем"
        except requests.exceptions.RequestException as e:
            message = f'Ошибка при подключении к API: {e}'

    elif query.data == 'list_tickets':
        telegram_username = update.effective_user.username
        logger.info(f'Запрос билетов для пользователя: {telegram_username}')
        if telegram_username:
            await show_tickets(update, context, telegram_username)
            return
        else:
            message = "Ошибка: не удалось определить ваше имя пользователя в Telegram."

    elif query.data == 'list_domes':  # Новая обработка для списка домов
        try:
            response = requests.get(DOMES_URL)
            response.raise_for_status()
            domes = response.json()

            if isinstance(domes, list):
                dome_list = ''
                for dome in domes:
                    dome_list += f"**Дом ID:** {dome['id']}, Название: {dome['name']}\n"

                message = f"Список доступных домов:\n{dome_list}" if dome_list else "Дома не найдены"
            else:
                message = "Ответ от API не является списком домов"
        except requests.exceptions.RequestException as e:
            message = f'Ошибка при подключении к API: {e}'

    keyboard = build_menu()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(message, reply_markup=reply_markup, parse_mode='MarkdownV2')

async def show_tickets(update: Update, context: ContextTypes.DEFAULT_TYPE, telegram_username: str) -> None:
    try:
        response = requests.get(TICKETS_URL, params={'telegram_username': telegram_username})
        response.raise_for_status()
        tickets = response.json()

        if isinstance(tickets, list) and tickets:
            ticket_list = ''
            for ticket in tickets:
                reservation_info = ticket.get('reservation_info', {})
                ticket_list += (
                    f"Билет ID: {ticket['id']}\n"
                    f"Ряд: {ticket['row']}\n"
                    f"Место: {ticket['seat']}\n"
                    f"Show Session: {ticket['show_session_info']}\n"
                    f"Reservation Created At: {reservation_info.get('created_at', 'N/A')}\n"
                    f"---\n"
                )
            message = f"Ваши билеты:\n{ticket_list}" if ticket_list else "У вас нет купленных билетов"
        else:
            message = "У вас нет купленных билетов"
    except requests.exceptions.RequestException as e:
        message = f'Ошибка при подключении к API: {e}'

    keyboard = build_menu()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(message, reply_markup=reply_markup)


def main() -> None:
    TG_BOT_TOKEN = '7069982548:AAH1wLBjwMY5GuCLk4Ckox2b-LO4TfmxGrA'

    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == '__main__':
    main()
