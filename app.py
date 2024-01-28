import os
import humanize

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Some of this was taken from the finance app - app config, login, register, apology


# Configure application
# Configure session to use filesystem (instead of signed cookies)
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///twitterclone.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def process_tweets(tweets):
    """Process tweets for display"""
    for tweet in tweets:
        tweet["likes"] = db.execute("SELECT count(*) as likes FROM likes WHERE tweet_id = ?", tweet["id"])
        tweet["userlikes"] = db.execute("SELECT * FROM likes WHERE user_id = ? AND tweet_id = ?", session["user_id"], tweet["id"]) if session else False
        tweet_time = datetime.strptime(tweet["date"], "%Y-%m-%d %H:%M:%S")
        tweet["friendlydate"] = humanize.naturaltime(tweet_time - datetime.now())
    return tweets

@app.route("/")
def index():
    """Show all tweets"""
    tweets = db.execute("SELECT *, username FROM tweets, users WHERE tweets.user_id = users.id ORDER BY date DESC")
    tweets = process_tweets(tweets)
    return render_template("index.html", tweets=tweets)

@app.route("/user")
def user():
    """Show user's tweets"""
    username = db.execute("SELECT username FROM users WHERE id = ?", request.args.get('user'))
    tweets = db.execute("SELECT *, username FROM tweets, users WHERE tweets.user_id = users.id AND tweets.user_id = ? ORDER BY date DESC", request.args.get('user'))
    tweets = process_tweets(tweets)
    return render_template("user.html", tweets=tweets, username=username[0]["username"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username is unique
        if len(rows) != 0:
            return apology("username already exists", 403)

        # Insert user into database
        db.execute("INSERT INTO users (username, password) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/tweet", methods=["POST"])
@login_required
def tweet():
    """Tweet"""
    if not request.form.get("contents"):
        return apology("You must provide a tweet")
    if len(request.form.get("contents")) > 255:
        return apology("Tweet must be less than 255 characters")
    db.execute("INSERT INTO tweets (user_id, contents) VALUES(?, ?)", session["user_id"], request.form.get("contents"))
    return redirect("/")


@app.route("/like", methods=["POST"])
@login_required
def like():
    """Like a tweet"""
    try:
        data = request.get_json()
        if not data.get("tweet"):
            return jsonify({"error": "You must provide a tweet"}), 400
        if data.get("action") == "dislike":
            db.execute("DELETE FROM likes WHERE user_id = ? AND tweet_id = ?", session["user_id"], data.get("tweet"))
        else:
            db.execute("INSERT INTO likes (user_id, tweet_id) VALUES(?, ?)", session["user_id"], data.get("tweet"))
        likes = db.execute("SELECT count(*) as likes FROM likes WHERE tweet_id = ?", data.get("tweet"))
        return jsonify({"status": "success", "likes": likes[0]['likes']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400