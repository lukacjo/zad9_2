from flask import Flask, render_template, request
import requests
import csv

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0].get('rates')
with open('data_file.csv', 'w', encoding='UTF8', newline='') as f :
    writer = csv.DictWriter(f, fieldnames=['code', 'currency', 'ask', 'bid'],delimiter=';')
    writer.writeheader()
    writer.writerows(rates)


@app.route("/nbp/", methods=["GET", "POST"])
def nbp():
    codes = []
    result = []
    for data in rates:
        codes.append(data.get('code'))
    if request.method == "POST":
        code=request.form.get("currency")
        ile=request.form.get("howmuch")
        for data in rates:
            if data.get('code') == code:
                ask = data.get('ask')
        ile=int(ile)
        elo=ask*ile
        return f"Koszt operacji to:{elo}zł ", result
    return render_template("zad9.2.html",codes=codes,rates=rates)




















if __name__ == '__main__':
    app.run(debug=True)