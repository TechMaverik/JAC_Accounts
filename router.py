from flask import Flask, render_template, request
from display import menus
import mapper
import service

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"


@app.route("/", methods=["get", "post"])
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
    rows = mapper.view_ledger_head()
    return render_template(
        "create_ledger.html",
        dashboard=menus.dashboard_menus,
        payment_type=menus.receipt_payment,
        ledger_list_table=menus.ledger_list_table,
        rows=rows,
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
        rows, receipt_amount, voucher_amount = service.cashbook()
        balance = receipt_amount[0][0] - voucher_amount[0][0]

        return render_template(
            "cashbook.html",
            dashboard=dashboard,
            cash_table=menus.cashbook_table,
            rows=rows,
            receipt_amount=receipt_amount,
            voucher_amount=voucher_amount,
            balance=balance,
        )
    except:
        dashboard = menus.dashboard_menus
        message = "NO LEDGERS FOUND TO DISPLAY CASHBOOK"
        return render_template("error.html", message=message, dashboard=dashboard)


if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)
