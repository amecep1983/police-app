from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "ghana-police-123"

wanted_cars = {
    "AS 1010-10": {"reason": "Wanted by Ashawo", "owner": "Krobea asante"},
}
officers_users = {"admin": "1234"}
@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    result = None
    searched = None
    if request.method == "POST":
        searched = request.form.get("plate", "").strip().upper()
        if searched in wanted_cars:
            result = wanted_cars[searched]
    return render_template("index.html", result=result, searched=searched, user=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
        if request.method == "POST":
        u = request.form.get("username","").strip().lower()
        p = request.form.get("password","").strip()
        if u in officers_users and officers_users[u] == p:
            session["user"] = u
            return redirect(url_for("home"))
        return render_template("login.html", error="Wrong login. Try Admin / 1234")
    return render_template("login.html")

@app.route("/add", methods=["GET", "POST"])
def add_car():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        plate = request.form.get("plate", "").strip().upper()
        wanted_cars[plate] = {"reason": request.form.get("reason"), "owner": request.form.get("owner")}
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/list")
def view_list():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("list.html", wanted=wanted_cars)


@app.route("/add_officer", methods=["GET", "POST"])
@app.route("/officers", methods=["GET", "POST"])
def add_officer():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        new_user = request.form.get("username")
        new_pass = request.form.get("password")
        if new_user and new_pass:
            officers_users[new_user.strip().lower()] = new_pass.strip()
        return redirect(url_for("add_officer"))
    return render_template("officers.html", officers=list(officers_users.keys()))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
