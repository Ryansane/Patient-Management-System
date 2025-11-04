Ryan Level 5 Hospital - Patient Management System

Run locally:
1. python3 -m venv venv
2. source venv/bin/activate   (or venv\Scripts\activate on Windows)
3. pip install -r requirements.txt
4. flask run   (or python app.py)

Render:
- Create a web service pointing to this repo.
- Build command: pip install -r requirements.txt
- Start command: gunicorn app:app

The project includes session-based notifications (Bootstrap alert banners) and a dynamic greeting.