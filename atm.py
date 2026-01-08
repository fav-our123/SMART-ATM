from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "atm_secret_key"  # Needed for session management

# -------------------------------
# Simulated User Database
# -------------------------------
users = {
    "1234567890": {"pin": "1234", "balance": 50000},
    "9876543210": {"pin": "5678", "balance": 75000}
}

# -------------------------------
# ROUTES
# -------------------------------

# 1. Welcome Page
@app.route("/")
def index():
    session.clear()  # Clear previous session
    return render_template("index.html")

# 2. Biometrics Verification (simulated)
@app.route("/biometric", methods=["GET", "POST"])
def biometric():
    if request.method == "POST":
        # For simulation, always pass biometric
        biometric_passed = request.form.get("biometric_passed", "true") == "true"
        if not biometric_passed:
            return render_template("index.html", error="Biometric verification failed. Please try again.")
        return redirect("/card")
    return render_template("biometric.html")

# 3. Card Entry
@app.route("/card", methods=["GET", "POST"])
def card():
    if request.method == "POST":
        card_number = request.form.get("card_number")
        if card_number in users:
            session["card"] = card_number
            return redirect("/pin")
        else:
            return render_template("card.html", error="Invalid card. Please try again.")
    return render_template("card.html")

# 4. PIN Authentication
@app.route("/pin", methods=["GET", "POST"])
def pin():
    card = session.get("card")
    if not card:
        return redirect("/card")

    if request.method == "POST":
        pin = request.form.get("pin")
        if users[card]["pin"] == pin:
            return redirect("/menu")
        else:
            return render_template("pin.html", error="Incorrect PIN. Please try again.")
    return render_template("pin.html")

# 5. Main Menu
@app.route("/menu", methods=["GET", "POST"])
def menu():
    card = session.get("card")
    if not card:
        return redirect("/card")

    if request.method == "POST":
        choice = request.form.get("choice")
        if choice == "1":
            return redirect("/balance")
        elif choice == "2":
            return redirect("/withdraw")
        elif choice == "3":
            return redirect("/exit")
        else:
            return render_template("menu.html", error="Invalid choice. Please select 1, 2, or 3.")
    return render_template("menu.html")

# 6A. Balance Inquiry
@app.route("/balance")
def balance():
    card = session.get("card")
    if not card:
        return redirect("/card")
    balance = users[card]["balance"]
    return render_template("balance.html", balance=balance)

# 6B. Withdraw Cash
@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    card = session.get("card")
    if not card:
        return redirect("/card")

    if request.method == "POST":
        try:
            amount = int(request.form.get("amount"))
        except (ValueError, TypeError):
            message = "Invalid amount entered."
            return render_template("withdraw.html", message=message, balance=users[card]["balance"])

        if amount <= 0:
            message = "Amount must be greater than zero."
        elif amount > users[card]["balance"]:
            message = "Insufficient funds. Please enter a lower amount."
        else:
            users[card]["balance"] -= amount
            message = f"Transaction successful. You withdrew {amount} naira."

        return render_template("withdraw.html", message=message, balance=users[card]["balance"])

    return render_template("withdraw.html", balance=users[card]["balance"])

# 7. Exit Page
@app.route("/exit")
def exit():
    session.clear()
    return render_template("exit.html")

# -------------------------------
# Run the App Locally
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
