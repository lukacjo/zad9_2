from flask import Flask, render_template, request, redirect, flash
import requests
import csv
import time

"""
Najlepsze czasy
Wersja pierwsza:
zdobycie: 0.0016s
nbp 0.052s

Wersja druga (z set):
zdobycie: 0.0005s
nbp: 0.040s
"""


def create_app():
    app = Flask(__name__)
    app.config[
        "SECRET_KEY"
    ] = "eh2WGSwY@HwO$!S!j32EM*9$36zKJCyvrvu#fRVV3rgs$3@H&whPGXwknMyW#qypW%E#D8yhTPDq$m##Ho6wUkNdIeuWozI8dZM"
    return app


app = create_app()


def fetch_and_save_currencies():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    start_time = time.time()
    rates = {currency["code"]: currency for currency in data[0].get("rates")}
    with open("data_file.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["code", "currency", "ask", "bid"], delimiter=";"
        )
        writer.writeheader()
        writer.writerows(rates.values())
    end_time = time.time()
    real_time = end_time - start_time
    print(f"Czas fetch_and_save to: {real_time}s")
    return rates


fetch_and_save_currencies()


@app.route("/nbp/", methods=["GET", "POST"])
def nbp():
    start_time = time.time()
    rates = fetch_and_save_currencies()
    codes = set(rates.keys())

    if request.method == "POST":
        code = request.form.get("currency")
        ile = int(request.form.get("howmuch"))

        currency_info = rates[code]
        ask = currency_info["ask"]
        elo = ask * ile
        flash(
            f"Koszt zakupu {ile} {code} to: {elo:.2f}zł",
            category="success",
        )
        end_time = time.time()
        real_time = end_time - start_time
        print(f"Czas nbp to: {real_time}s")

    return render_template("zad9.2.html", codes=codes, rates=rates.values())


if __name__ == "__main__":
    app.run(debug=True)
