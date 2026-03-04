import re
import sqlite3
import logging
import time
from flask import Flask, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

# -----------------------
# Logging Configuration
# -----------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------
# Database Initialization
# -----------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -----------------------
# Brute Force Protection
# -----------------------

login_attempts = {}

MAX_ATTEMPTS = 5
LOCKOUT_TIME = 300  # seconds (5 minutes)

def is_locked_out(ip):

    if ip in login_attempts:

        attempts, last_attempt = login_attempts[ip]

        if attempts >= MAX_ATTEMPTS:
            if time.time() - last_attempt < LOCKOUT_TIME:
                return True
            else:
                login_attempts[ip] = [0, time.time()]

    return False


def record_failed_attempt(ip):

    if ip not in login_attempts:
        login_attempts[ip] = [1, time.time()]
    else:
        login_attempts[ip][0] += 1
        login_attempts[ip][1] = time.time()


def reset_attempts(ip):

    if ip in login_attempts:
        del login_attempts[ip]

# -----------------------
# Input Validation
# -----------------------

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return len(password) >= 8

# -----------------------
# Security Headers
# -----------------------

@app.after_request
def set_security_headers(response):

    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    return response

# -----------------------
# Routes
# -----------------------

@app.route("/")
def home():

    if "user" in session:
        return f"""
        <h2>Welcome {session['user']}</h2>
        <a href='/logout'>Logout</a>
        """

    return """
    <h2>Secure SDLC Demo App</h2>
    <a href='/register'>Register</a><br>
    <a href='/login'>Login</a>
    """

# -----------------------
# Register
# -----------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not is_valid_email(email):
            return "Invalid email format"

        if not is_valid_password(password):
            return "Password must be at least 8 characters"

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, hashed_password)
            )

            conn.commit()
            conn.close()

            logging.info(f"User registered: {email}")

            return redirect("/login")

        except sqlite3.IntegrityError:

            logging.warning(f"Duplicate registration attempt: {email}")

            return "User already exists"

    return """
    <h2>Register</h2>
    <form method="POST">
    Email:<br>
    <input type="text" name="email"><br><br>

    Password:<br>
    <input type="password" name="password"><br><br>

    <input type="submit" value="Register">
    </form>
    """

# -----------------------
# Login
# -----------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    ip = request.remote_addr

    if is_locked_out(ip):
        logging.warning(f"Blocked login attempt from {ip} (too many attempts)")
        return "Too many failed login attempts. Try again in 5 minutes."

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[0], password):

            session["user"] = email

            reset_attempts(ip)

            logging.info(f"Successful login: {email}")

            return redirect("/")

        else:

            record_failed_attempt(ip)

            logging.warning(f"Failed login attempt for {email} from {ip}")

            return "Invalid credentials"

    return """
    <h2>Login</h2>
    <form method="POST">
    Email:<br>
    <input type="text" name="email"><br><br>

    Password:<br>
    <input type="password" name="password"><br><br>

    <input type="submit" value="Login">
    </form>
    """

# -----------------------
# Logout
# -----------------------

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")

# -----------------------
# Run with HTTPS
# -----------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        ssl_context=("cert.pem", "key.pem")
    )