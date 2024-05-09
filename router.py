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
        payment_type=menus.payment_type,
        ledger_list_table=menus.ledger_list_table,
        rows=rows,
    )


@app.route("/receipt", methods=["get", "post"])
def receipt():
    ledger_header = mapper.view_ledger_head()
    service.generate_receipt()
    return render_template(
        "receipt.html",
        dashboard=menus.dashboard_menus,
        ledger_header=ledger_header,
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

    return render_template(
        "view_ledger.html",
        dashboard=dashboard,
        ledger_header=ledger_header,
        ledger_view_table_head=menus.ledger_view_table_head,
    )


if __name__ == "__main__":
    app.run("localhost", 5000, debug=True)
