from flask import Flask, render_template, request, redirect, flash
import requests
import csv


def create_app():
    app = Flask(__name__)
    app.config[
        "SECRET_KEY"
    ] = "eh2WGSwY@HwO$!S!j32EM*9$36zKJCyvrvu#fRVV3rgs$3@H&whPGXwknMyW#qypW%E#D8yhTPDq$m##Ho6wUkNdIeuWozI8dZM"
    return app


app = create_app()


def zdobycie_i_zapisanie_walut():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    rates = data[0].get("rates")
    with open("data_file.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["code", "currency", "ask", "bid"], delimiter=";"
        )
        writer.writeheader()
        writer.writerows(rates)
    return rates


@app.route("/nbp/", methods=["GET", "POST"])
def nbp():
    rates = zdobycie_i_zapisanie_walut()
    codes = []

    for data in rates:
        codes.append(data.get("code"))
    if request.method == "POST":
        code = request.form.get("currency")
        ile = int(request.form.get("howmuch"))

        for data in rates:
            if data.get("code") == code:
                ask = data.get("ask")
        ile = ile
        elo = ask * ile
        flash(
            f"Koszt operacji w przypadku waluty {code} to: {elo:.2f}zł",
            category="success",
        )
    return render_template("zad9.2.html", codes=codes, rates=rates)


if __name__ == "__main__":
    app.run(debug=True)
