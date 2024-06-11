# Planetarium API service
This is the Planetarium Management API. This project provides a comprehensive set of endpoints to manage the entire theatre ecosystem.
 
## Features
- JWT token authentication.
- Swagger documentation.
- Throttling for Anon, Auth users.
- Telegram bot with ability to get informations about shows/tickets etc.
- Image uploading.
- Planetarium API has such endpoints api/theatre: themes, astronomy shows, planetarium dome, reservations, tickets, reservations, show sessions.
- User API has multiple useful endpoints you can check them at swagger documentation page.
- Use endpoints to buy tickets, check reservation history any many more.
- For endpoints you can check the swagger documentation api/schema/swagger/.
 
 
## Common installation
 
1. **Clone the repository:**
 
   ```sh
   git https://github.com/mikhailyemets/Planetarium-API-Service.git (After develop branch merged with main)
   cd api
   ```
 
2. Create and activate **venv** (bash):
   ```sh
   python -m venv venv
   source venv/Scripts/activate
   ```
   Windows (Command Prompt)
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
   Mac / Linux (Unix like systems)
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
 
3. Create an `.env` file in the root of the project directory. You can use the `.env.example` file as a template (just change DJANGO_SECRET_KEY):
    ```sh
    cp .env.example .env
    ```
 
### Local installation:
1. Install **requirements.txt** to your **venv**:
   ```sh
   pip install -r requirements.txt
   ```
 
2. Create apply migrations:
   ```sh
   python manage.py migrate
   ```
 
3. (Optional) use my sample of prefilled DB:
   ```sh
   python manage.py loaddata planetarium.json
   python manage.py loaddata user.json
   ```
 
4. Start the server:
   ```sh
   python manage.py runserver
   ```
 
### Docker local installation:
1. Create app image and start it:
   ```sh
   docker-compose build
   docker-compose up
   ```
 
### If you used prefilled database from .json:
   - **admin_user**. email: admin@mail.com, password: 123123
   - **auth_user**. email: user@mail.com, password: 123123
