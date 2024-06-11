import logging
import requests
from decouple import config

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

# setting for tg_bot/docker

HOST = 'http://127.0.0.1:8000'
DOCKER_HOST = 'http://planetarium:8000'

THEMES_URL = f'{DOCKER_HOST}/api/planetarium/themes/'
SESSIONS_URL = f'{DOCKER_HOST}/api/planetarium/show_sessions/'
ASTRO_SHOWS_URL = f'{DOCKER_HOST}/api/planetarium/shows/'
TICKETS_URL = f'{DOCKER_HOST}/api/planetarium/tickets/'
DOMES_URL = f'{DOCKER_HOST}/api/planetarium/domes/'

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
                        f"Session ID: {session['id']}\n"
                        f"Show ID: {session['show']}\n"
                        f"Date and Time: {session['date_time']}\n\n"
                    )

                message = f"List of available sessions:\n{session_list}" if session_list else "Sessions not found"
            else:
                message = "Response from API is not a list of sessions"
        except requests.exceptions.RequestException as e:
            message = f'Error connecting to API: {e}'

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
                        f"Show ID: {show['id']}\n"
                        f"Title: {show['title']}\n"
                        f"Description: {show['description']}\n"
                        f"Themes: {themes}\n\n"
                    )

                message = f"List of available shows:\n{show_list}" if show_list else "Shows not found"
            else:
                message = "Response from API is not a list of shows"
        except requests.exceptions.RequestException as e:
            message = f'Error connecting to API: {e}'

    elif query.data == 'list_themes':
        try:
            response = requests.get(THEMES_URL)
            response.raise_for_status()
            themes = response.json()

            if isinstance(themes, list):
                theme_list = ''
                for theme in themes:
                    theme_list += f"Theme ID: {theme['id']}, Name: {theme['name']}\n"

                message = f"List of available themes:\n{theme_list}" if theme_list else "Themes not found"
            else:
                message = "Response from API is not a list of themes"
        except requests.exceptions.RequestException as e:
            message = f'Error connecting to API: {e}'

    elif query.data == 'list_tickets':
        telegram_username = update.effective_user.username
        logger.info(f'Requesting tickets for user: {telegram_username}')
        if telegram_username:
            await show_tickets(update, context, telegram_username)
            return
        else:
            message = "Error: Could not determine your Telegram username."

    elif query.data == 'list_domes':
        try:
            response = requests.get(DOMES_URL)
            response.raise_for_status()
            domes = response.json()

            if isinstance(domes, list):
                dome_list = ''
                for dome in domes:
                    dome_list += f"**Dome ID:** {dome['id']}, Name: {dome['name']}\n"

                message = f"List of available domes:\n{dome_list}" if dome_list else "Domes not found"
            else:
                message = "Response from API is not a list of domes"
        except requests.exceptions.RequestException as e:
            message = f'Error connecting to API: {e}'

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
                    f"Ticket ID: {ticket['id']}\n"
                    f"Row: {ticket['row']}\n"
                    f"Seat: {ticket['seat']}\n"
                    f"Show Session: {ticket['show_session_info']}\n"
                    f"Reservation Created At: {reservation_info.get('created_at', 'N/A')}\n"
                    f"---\n"
                )
            message = f"Your tickets:\n{ticket_list}" if ticket_list else "You have no purchased tickets"
        else:
            message = "You have no purchased tickets"
    except requests.exceptions.RequestException as e:
        message = f'Error connecting to API: {e}'

    keyboard = build_menu()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(message, reply_markup=reply_markup)


def main() -> None:
    TG_BOT_TOKEN = config("TG_TOKEN")

    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == '__main__':
    main()
