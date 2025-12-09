import os
import logging
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail  # <--- NEW: Import Mail
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
mail = Mail()  # <--- NEW: Initialize Mail

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# --- EMAIL CONFIGURATION (GMAIL) ---
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'ashishbhandari0408@gmail.com')  # <-- default to admin email

# --- STARTUP VALIDATION (helpful logs if creds missing on Render) ---
if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    app.logger.warning("Mail credentials are missing. Set MAIL_USERNAME and MAIL_PASSWORD (Render environment). "
                       "Gmail typically requires an App Password or OAuth2 - do not use a regular account password.")

db.init_app(app)
mail.init_app(app)  # <--- NEW: Connect Mail to App

# --- ASYNC EMAIL SENDER AND UTILITIES ---
import threading
from flask import current_app, render_template, request, jsonify  # <-- add request & jsonify
from flask_mail import Message

def _send_async_mail(app_obj, msg):
    with app_obj.app_context():
        try:
            mail.send(msg)
            app_obj.logger.info("Email sent to %s subject=%s", msg.recipients, msg.subject)
        except Exception as exc:
            app_obj.logger.exception("Failed to send email to %s: %s", msg.recipients, exc)

def send_email(to, subject, html=None, body=None, sender=None):
    """
    Sends an email asynchronously.
    - to: string or list of emails
    - subject: string
    - html: html body (preferred)
    - body: text body (optional)
    - sender: optional from address, defaults to MAIL_DEFAULT_SENDER
    Returns: threading.Thread object for the send operation.
    """
    if isinstance(to, str):
        recipients = [to]
    else:
        recipients = to

    sender = sender or app.config.get('MAIL_DEFAULT_SENDER')
    msg = Message(subject=subject, recipients=recipients, html=html, body=body, sender=sender)
    thread = threading.Thread(target=_send_async_mail, args=(app, msg), daemon=True)
    thread.start()
    return thread

def send_order_status_email(order=None, user_email=None, action='updated'):
    """
    Send an order status update email.
    - order: optional object that can have .id and .status (if provided, used to populate template)
    - user_email: required if order/user isn't available from DB
    - action: textual action e.g., 'accepted', 'cancelled'
    """
    # Determine recipient
    recipient = None
    order_data = {}
    try:
        # If a model Order object is passed, extract email
        if order is not None:
            order_id = getattr(order, "id", None)
            order_status = getattr(order, "status", action)
            order_data = {"id": order_id, "status": order_status}
            # try to read user email from order.user.email if exists
            user = getattr(order, "user", None)
            if user:
                recipient = getattr(user, "email", None)
    except Exception:
        recipient = None

    # Fallback to explicit param
    if not recipient:
        recipient = user_email

    if not recipient:
        current_app.logger.error("No recipient email found for order status email (order=%r)", order)
        return None

    subject = f"[Feast-Fleet] Order #{order_data.get('id','?')} {action.capitalize()}"
    # try rendering template; fallback to text
    try:
        html = render_template("emails/order_status.html", order=order_data, action=action)
    except Exception:
        html = None
    body = f"Your order #{order_data.get('id','?')} has been {action}."

    # Use existing send_email (async)
    return send_email(recipient, subject, html=html, body=body)

# --- CLI command to test email sending from Render environment ---
import click

@app.cli.command("send-test-email")
@click.argument("recipient")
def send_test_email(recipient):
    """Usage: flask send-test-email you@example.com   (run from app directory)"""
    subject = "[Feast-Fleet] Test email from app"
    body = "This is a test message from the Feast-Fleet app."
    html = "<p>This is a <strong>test</strong> message from the Feast-Fleet app.</p>"
    send_email(recipient, subject, html=html, body=body)
    app.logger.info("Triggered test email to %s", recipient)
    click.echo(f"Triggered test email to {recipient}. Check logs for confirmation.")

# --- ADMIN ROUTES (safe and minimal) ---
# Note: protect these routes using your existing admin/authentication in production.
@app.route("/admin/order/<int:order_id>/status", methods=["POST"])
def admin_update_order_status(order_id):
    """
    Update order status and notify user.
    Expected JSON body: {"action": "accepted"|"cancelled", "email": "user@example.com" (optional)}
    If you have a models.Order with relation to user, the endpoint will use that user's email automatically.
    """
    payload = request.get_json(silent=True) or {}
    action = (payload.get("action") or "").lower()
    explicit_email = payload.get("email")

    if action not in ("accepted", "cancelled", "completed", "pending", "rejected"):
        return jsonify({"error": "invalid action"}), 400

    order = None
    # Try to fetch order from models.Order if available
    try:
        import models  # noqa: F401
        Order = getattr(models, "Order", None)
        if Order:
            order = Order.query.get(order_id)
            if order:
                # update status on the order model if field exists
                if hasattr(order, "status"):
                    order.status = action
                    db.session.add(order)
                    db.session.commit()
    except Exception as exc:
        current_app.logger.debug("Order DB update skipped/failed: %s", exc)

    # If order exists but didn't provide user email, send_order_status_email will attempt to read user email
    recipient = explicit_email or None
    thread = send_order_status_email(order=order, user_email=recipient, action=action)
    return jsonify({
        "status": "queued",
        "action": action,
        "order_id": order_id,
        "email": explicit_email if explicit_email else (getattr(getattr(order, 'user', None), 'email', None) if order else None)
    }), 202

# Debug helper route (only active if explicitly enabled)
if os.environ.get("ALLOW_DEBUG_EMAIL_ROUTE", "False").lower() in ("true", "1", "yes"):
    from flask import jsonify
    @app.route("/_debug/test-email/<email_addr>")
    def _debug_test_email(email_addr):
        send_email(email_addr, "[Feast-Fleet] Debug test", html="<p>Debug test</p>", body="Debug test")
        return jsonify({"status": "queued", "to": email_addr})

with app.app_context():
    import models  # noqa: F401
    db.create_all()

# USAGE: call this from your admin accept/cancel order handlers:
# from app import send_email
# subject = f"Your order #{order.id} has been {order.status}"
# html = render_template("emails/order_status.html", order=order)  # build template in templates/emails
# send_email(order.user.email, subject, html=html)