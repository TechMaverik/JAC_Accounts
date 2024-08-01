from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from display import menus
import mapper, service, settings
import json, os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["get", "post"])
def welcome():
    return render_template(
        "welcome.html",
        dashboard=menus.dashboard_menus,
    )


@app.route("/directory", methods=["get", "post"])
def index():
    dashboard = menus.dashboard_menus
    member_tab = menus.add_members_menu
    rows = mapper.view_members()
    return render_template(
        "index.html",
        dashboard=dashboard,
        rows=rows,
        member_tab=member_tab,
    )


@app.route("/add_members", methods=["get", "post"])
def add_members():
    dashboard = menus.dashboard_menus
    gender = menus.gender
    yes_no = menus.yes_no
    status = service.add_members()
    return render_template(
        "add_members.html",
        dashboard=dashboard,
        gender=gender,
        yes_no=yes_no,
        status=status,
    )


@app.route("/delete", methods=["get", "post"])
def delete():
    dashboard = menus.dashboard_menus
    return render_template("delete.html", dashboard=dashboard)


@app.route("/delete_member", methods=["get", "post"])
def delete_member():
    dashboard = menus.dashboard_menus
    member_tab = menus.add_members_menu
    rows = mapper.view_members()
    service.delete_member()
    return render_template(
        "index.html",
        dashboard=dashboard,
        member_tab=member_tab,
    )


@app.route("/create_ledger", methods=["get", "post"])
def create_ledger():
    service.create_ledger()
    company = mapper.get_company_details()
    rows = mapper.view_ledger_head()
    return render_template(
        "create_ledger.html",
        dashboard=menus.dashboard_menus,
        payment_type=menus.receipt_payment,
        ledger_list_table=menus.ledger_list_table,
        rows=rows,
        company=company,
    )


@app.route("/receipt", methods=["get", "post"])
def receipt():
    ledger_header = mapper.view_ledger_head()
    header = service.get_ledgerlist()
    service.generate_receipt()
    return render_template(
        "receipt.html",
        dashboard=menus.dashboard_menus,
        ledger_header=ledger_header,
        receipt_payment=menus.receipt_payment,
        payment_type=menus.payment_type,
        header=header,
    )


@app.route("/delete_ledgerhead", methods=["get", "post"])
def delete_ledgerhead():
    dashboard = menus.dashboard_menus
    service.delete_ledgerhead()
    return render_template(
        "delete_ledgerhead.html",
        dashboard=dashboard,
    )


@app.route("/view_ledger", methods=["get", "post"])
def view_ledger():
    dashboard = menus.dashboard_menus
    ledger_header = service.get_ledgerlist()

    if request.method == "POST":
        ledger, receipt_sum, voucher_sum, head = service.view_ledger()
        print(ledger)
        return render_template(
            "view_ledger.html",
            dashboard=dashboard,
            ledger_header=ledger_header,
            ledger_view_table_head=menus.ledger_view_table_head,
            ledger=ledger,
            head=head,
            receipt_sum=receipt_sum,
            voucher_sum=voucher_sum,
        )
    else:
        return render_template(
            "view_ledger.html",
            dashboard=dashboard,
            ledger_header=ledger_header,
            ledger_view_table_head=menus.ledger_view_table_head,
        )


@app.route("/cashbook", methods=["get", "post"])
def cashbook():
    try:

        dashboard = menus.dashboard_menus
        rows, receipt_amount, voucher_amount, opening_balance = service.cashbook()
        try:
            opening_balance_data = int(opening_balance[0][1])
        except:
            opening_balance_data = 0
        try:
            receipt_amount_data = int(receipt_amount[0][0])
        except:
            receipt_amount_data = 0
        try:
            voucher_amount_data = int(voucher_amount[0][0])
        except:
            voucher_amount_data = 0

        try:
            balance = (opening_balance_data + receipt_amount_data) - voucher_amount_data
        except:
            balance = 0

        return render_template(
            "cashbook.html",
            dashboard=dashboard,
            cash_table=menus.cashbook_table,
            rows=rows,
            receipt_amount=receipt_amount,
            voucher_amount=voucher_amount,
            balance=balance,
            opening_balance_data=opening_balance_data,
        )
    except:
        return render_template(
            "error.html",
            message="No Processed Cashbook Data to Display",
            dashboard=menus.dashboard_menus,
        )


@app.route("/add_opening_balance", methods=["get", "post"])
def add_opening_balance():
    service.add_opening_balance()
    dashboard = menus.dashboard_menus
    message = "Successfully Added Opening Cash"
    return render_template("error.html", message=message, dashboard=dashboard)


@app.route("/income_expense", methods=["get", "post"])
def income_expense():
    expenses_tables = menus.income_table
    try:
        incomes, expenses, receipt_total, voucher_total, comment, balance, colors = (
            service.income_expense()
        )

        dashboard = menus.dashboard_menus

        return render_template(
            "income_and_expense.html",
            expenses_tables=expenses_tables,
            expenses=expenses,
            incomes=incomes,
            dashboard=dashboard,
            receipt_total=receipt_total,
            voucher_total=voucher_total,
            comment=comment,
            balance=balance,
            colors=colors,
        )
    except:
        dashboard = menus.dashboard_menus
        message = "No Ledger data found to display Income and Expenditure"
        return render_template("error.html", message=message, dashboard=dashboard)


@app.route("/settings", methods=["get", "post"])
def settings_page():
    return render_template(
        "settings.html",
        dashboard=menus.dashboard_menus,
        months=menus.months,
    )


@app.route("/erase_all_data", methods=["get", "post"])
def erase_all_data():
    status = settings.erase_all_data()
    return render_template(
        "welcome.html",
        dashboard=menus.dashboard_menus,
        status=status,
    )


@app.route("/create_company", methods=["get", "post"])
def create_company():
    service.create_company()
    company_details = mapper.get_company_details()
    try:
        x = company_details[0][0]
    except:
        company_details = ""
    return render_template(
        "create_company.html",
        dashboard=menus.dashboard_menus,
        company_tables=menus.company_details,
        company_details=company_details,
    )


@app.route("/plot_expense", methods=["get", "post"])
def get_expense_plotting_data():

    (
        hospital_expense_amt,
        car_loan_amt,
        emi_amt,
        electricity_bill,
        food_amt,
        groceries_amt,
        house_rent_amt,
        infotainment_amt,
        others_amt,
        steam_amt,
    ) = mapper.get_expense_plotting_data()

    try:
        hospital_expense_amt = hospital_expense_amt[0][0]
    except:
        hospital_expense_amt = 0
    try:
        car_loan_amt = car_loan_amt[0][0]
    except:
        car_loan_amt = 0
    try:
        emi_amt = emi_amt[0][0]
    except:
        emi_amt = 0
    try:
        electricity_bill = electricity_bill[0][0]
    except:
        electricity_bill = 0
    try:
        food_amt = food_amt[0][0]
    except:
        food_amt = 0
    try:
        groceries_amt = groceries_amt[0][0]
    except:
        groceries_amt = 0
    try:
        house_rent_amt = house_rent_amt[0][0]
    except:
        house_rent_amt = 0
    try:
        infotainment_amt = infotainment_amt[0][0]
    except:
        infotainment_amt = 0
    try:
        others_amt = others_amt[0][0]
    except:
        others_amt = 0
    try:
        steam_amt = steam_amt[0][0]
    except:
        steam_amt = 0

    data = {
        "hospital_expense_amt": hospital_expense_amt,
        "car_loan_amt": car_loan_amt,
        "emi_amt": emi_amt,
        "electricity_bill": electricity_bill,
        "food_amt": food_amt,
        "groceries_amt": groceries_amt,
        "house_rent_amt": house_rent_amt,
        "infotainment_amt": infotainment_amt,
        "others_amt": others_amt,
        "steam_amt": steam_amt,
    }
    return data


@app.route("/export_json", methods=["get", "post"])
def export_to_json():

    (
        hospital_expense_amt,
        car_loan_amt,
        emi_amt,
        electricity_bill,
        food_amt,
        groceries_amt,
        house_rent_amt,
        infotainment_amt,
        others_amt,
        steam_amt,
    ) = mapper.get_expense_plotting_data()

    try:
        hospital_expense_amt = hospital_expense_amt[0][0]
    except:
        hospital_expense_amt = 0
    try:
        car_loan_amt = car_loan_amt[0][0]
    except:
        car_loan_amt = 0
    try:
        emi_amt = emi_amt[0][0]
    except:
        emi_amt = 0
    try:
        electricity_bill = electricity_bill[0][0]
    except:
        electricity_bill = 0
    try:
        food_amt = food_amt[0][0]
    except:
        food_amt = 0
    try:
        groceries_amt = groceries_amt[0][0]
    except:
        groceries_amt = 0
    try:
        house_rent_amt = house_rent_amt[0][0]
    except:
        house_rent_amt = 0
    try:
        infotainment_amt = infotainment_amt[0][0]
    except:
        infotainment_amt = 0
    try:
        others_amt = others_amt[0][0]
    except:
        others_amt = 0
    try:
        steam_amt = steam_amt[0][0]
    except:
        steam_amt = 0

    data = {
        "hospital_expense_amt": hospital_expense_amt,
        "car_loan_amt": car_loan_amt,
        "emi_amt": emi_amt,
        "electricity_bill": electricity_bill,
        "food_amt": food_amt,
        "groceries_amt": groceries_amt,
        "house_rent_amt": house_rent_amt,
        "infotainment_amt": infotainment_amt,
        "others_amt": others_amt,
        "steam_amt": steam_amt,
    }
    try:
        os.mkdir("exports")
    except:
        pass
    if request.method == "POST":
        month = request.form.get("month")
    with open("exports/" + month + ".json", "w") as file:
        json.dump(data, file, indent=6)
        file.close()
    return render_template(
        "settings.html",
        dashboard=menus.dashboard_menus,
        months=menus.months,
    )


@app.route("/delete_all_table_contents", methods=["get", "post"])
def delete_all_table_contents():
    service.delete_all_table_contents()
    return render_template(
        "settings.html",
        dashboard=menus.dashboard_menus,
        months=menus.months,
    )


@app.route("/plotting", methods=["get", "post"])
def plotting():
    return redirect("http://192.168.1.13:1880/ui")


if __name__ == "__main__":
    app.run("localhost", 5000, debug=False)
