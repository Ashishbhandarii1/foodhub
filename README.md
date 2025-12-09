Feast-Fleet — Flask app

Quick setup:
1. Create a virtualenv, install deps:
   python -m venv .venv
   .venv\Scripts\activate      (Windows)
   pip install -r requirements.txt

2. Local run:
   set DATABASE_URL=sqlite:///dev.db
   set MAIL_USERNAME=your@gmail.com
   set MAIL_PASSWORD=your_app_password
   flask run

Push to GitHub (option A: manual)
1. git init
2. git add .
3. git commit -m "Initial commit"
4. Create remote repo on GitHub and push (or use gh CLI):
   gh repo create Feast-Fleet --public --source=. --remote=origin --push

Option B: use scripts/create_github_repo.sh (requires gh CLI)

Render / Production:
- On Render set env vars: DATABASE_URL, SESSION_SECRET, MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER (optional).
- For Gmail, use an App Password or a transactional mail provider (SendGrid/Mailgun) and set credentials in Render.
