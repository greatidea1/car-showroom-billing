from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_pymongo import PyMongo
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Set up MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/rbcars"
mongo = PyMongo(app)

# Database collections
payments_collection = mongo.db.payments

# Home page to accept payments
@app.route("/", methods=["GET", "POST"])
def index():
    today_date = datetime.today().strftime('%Y-%m-%d')

    if request.method == "POST":
        branch_name = request.form.get("branch_name")
        branch_type = request.form.get("branch_type")
        product_service_name = request.form.get("product_service_name")
        payment_type = request.form.get("payment_type")
        payment_amount = float(request.form.get("payment_amount"))
        payment_date = request.form.get("payment_date") or today_date

        payment_data = {
            "branch_name": branch_name,
            "branch_type": branch_type,
            "product_service_name": product_service_name,
            "payment_type": payment_type,
            "payment_amount": payment_amount,
            "payment_date": payment_date
        }

        # Insert data into MongoDB
        payments_collection.insert_one(payment_data)
        flash("Payment recorded successfully!", "success")
        return redirect(url_for("index"))

    return render_template("index.html", today_date=today_date)

# Report page to generate date-wise report
@app.route("/report", methods=["GET"])
def report():
    date_filter = request.args.get('date')
    total_amount = 0

    if date_filter:
        payments = list(payments_collection.find({"payment_date": date_filter}))
        total_amount = sum(payment['payment_amount'] for payment in payments)
        return render_template("report.html", payments=payments, total_amount=total_amount, date=date_filter)
    
    return render_template("report.html", total_amount=total_amount)



# Main entry point to run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
