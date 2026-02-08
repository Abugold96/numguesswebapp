from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
# Required for session to store random number and guesses
app.secret_key = "supersecretkey"


@app.route("/", methods=["GET", "POST"])
def index():
    # Initialize random number and guesses
    if "random_number" not in session:
        session["random_number"] = random.randint(1, 100)  # default top range
        session["guesses"] = 0

    message = ""
    top_range = session.get("top_range", 100)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "set_range":
            user_range = request.form.get("top_of_range")
            if user_range.isdigit() and int(user_range) > 0:
                top_range = int(user_range)
                session["top_range"] = top_range
                session["random_number"] = random.randint(1, top_range)
                session["guesses"] = 0
                message = f"Range set! Guess a number between 1 and {top_range}."
            else:
                message = "Please enter a valid number larger than 0."

        elif action == "guess":
            user_guess = request.form.get("user_guess")
            session["guesses"] += 1

            if not user_guess.isdigit():
                message = "Please enter a valid number."
            else:
                user_guess = int(user_guess)
                if user_guess == session["random_number"]:
                    message = f"You got it in {session['guesses']} guesses! 🎉"
                    # Reset game
                    session.pop("random_number")
                    session.pop("guesses")
                    session.pop("top_range")
                elif user_guess > session["random_number"]:
                    message = "You were above the number!"
                else:
                    message = "You were below the number!"

    return render_template("index.html", message=message, top_range=top_range)


if __name__ == "__main__":
    app.run(debug=True)
