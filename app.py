from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        return redirect(url_for("market"))

    return render_template("signin.html")

@app.route("/market")
def market():
    return render_template("market.html")
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    return redirect(url_for("market"))

@app.route("/register")
def register():
    name= request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    return redirect(url_for("market"))
if __name__ == "__main__":
   app.run(debug=True)
