from flask import Flask, render_template, request, url_for,redirect,flash
import requests

app = Flask(__name__)
app.secret_key = "foreignCurrencyKey"

#edit api_key
api_key = "your key"
access_url = "http://data.fixer.io/api/latest?access_key=" + api_key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #form value
        firstCurrency = request.form.get("firstCurrency")
        secondCurrency = request.form.get("secondCurrency")
        amount = request.form.get("amount")
        try:
            response = requests.get(access_url)
            if response.status_code == 200:
                # terminal info
                # app.logger.info(response)

                infos = response.json()
                # terminal info
                # app.logger.info(infos)

                if infos["success"] == True:
                    firstValue = infos["rates"][firstCurrency]
                    secondValue = infos["rates"][secondCurrency]
                    result = (secondValue / firstValue) * float(amount)
                    currencyInfo = dict()

                    currencyInfo["firstCurrency"] = firstCurrency
                    currencyInfo["secondCurrency"] = secondCurrency
                    currencyInfo["amount"] = amount
                    currencyInfo["result"] = result

                else:
                    flash("İstek başarısız Key'i kontrol et!", "warning")
                    return redirect(url_for("index"))
                flash("Başarılı !", "success")
                return render_template("index.html", info=currencyInfo)

            flash("İstek başarısız URL 200 OK cevabı vermedi !", "warning")
            return redirect(url_for("index"))

        except:
            flash("İstek başarısız URL hatalı olabilir http:// eklemeyi dene !", "warning")
            return redirect(url_for("index"))

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)