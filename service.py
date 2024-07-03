from flask import request
from models.add_members import AddMembers
from models.ledger import LedgerHead
import mapper
import random


def add_members():
    if request.method == "POST":
        new_members = AddMembers(
            name=request.form["name"],
            address=request.form["address"],
            gender=request.form["gender"],
            dob=request.form["dob"],
            voting_power=request.form["voting_power"],
            married=request.form["married"],
            contact_no=request.form["contact_no"],
            whatsapp_no=request.form["whatsapp_no"],
            dom=request.form["dom"],
            spouse_name=request.form["spouse_name"],
            nos_children=request.form["nos_children"],
            subscription=request.form["subscription"],
        )
        status = mapper.add_members(new_members)
        return status


def delete_member():
    if request.method == "POST":
        id = request.form.get("id")
        mapper.delete_member(id)


def create_ledger():
    if request.method == "POST":
        lh_id = "LH" + str(random.randint(1, 100))
        ledgerHead = LedgerHead(
            id=lh_id, name=request.form["head"], company=request.form["company"]
        )
        with open("static/ledger.txt", "a") as file:
            file.writelines(str(request.form["head"]))
            file.write("\n")
            file.close()
        mapper.create_ledger(ledgerHead)


def get_ledgerlist():
    clean_ledger_list = []
    with open("static/ledger.txt", "r") as file:
        ledger_list = file.readlines()
        file.close()
    for unclean_data in ledger_list:
        data = unclean_data.replace("\n", "")
        clean_ledger_list.append(data)
    return clean_ledger_list


def delete_ledgerhead():
    if request.method == "POST":
        name = request.form.get("name")
        ledgerList = get_ledgerlist()

        with open("static/ledger.txt", "w") as file:
            ledgerList.remove(name)
            for data in ledgerList:
                file.writelines(str(data) + "\n")
            file.close()
        mapper.delete_ledgerhead(name)


def generate_receipt():
    if request.method == "POST":
        counter_file = open("static/receipt_counter.txt", "r")
        receipt_index = int(counter_file.read())
        counter_file.close()
        counter_file = open("static/voucher_counter.txt", "r")
        voucher_index = int(counter_file.read())
        counter_file.close()

        ID = random.randint(0, 1000)
        name = request.form.get("name")
        payment_type = request.form.get("payment_type")
        payment_method = request.form.get("payment_method")
        ledger_head = request.form.get("ledger_head")
        date = request.form.get("date")
        amount = request.form.get("amount")

        if payment_type == "Income":
            mapper.generate_receipt(
                ID,
                name,
                payment_type,
                payment_method,
                ledger_head,
                date,
                amount,
                receipt_index,
            )
            counter_file = open("static/receipt_counter.txt", "w")
            data = int(receipt_index) + 1
            counter_file.write(str(data))
            counter_file.close()

        elif payment_type == "Expense":
            mapper.generate_receipt(
                ID,
                name,
                payment_type,
                payment_method,
                ledger_head,
                date,
                amount,
                voucher_index,
            )
            counter_file = open("static/voucher_counter.txt", "w")
            data = int(voucher_index) + 1
            counter_file.write(str(data))
            counter_file.close()


def view_ledger():
    if request.method == "POST":
        head = request.form.get("head")
        rows, receipt_sum, voucher_sum = mapper.view_ledger(head)
        return rows, receipt_sum, voucher_sum, head


def cashbook():
    headers = get_ledgerlist()
    opening_balance = mapper.get_opening_balance()
    rows, receipt_amount, voucher_amount = mapper.cashbook(header=headers)
    return (rows, receipt_amount, voucher_amount, opening_balance)


def add_opening_balance():
    if request.method == "POST":
        id = random.randint(0, 2)
        amount = request.form.get("opening_balance")
        mapper.add_opening_balance(id, amount)


def income_expense():
    headers = get_ledgerlist()
    income_row, expense_row, receipt_total, voucher_total = mapper.income_expense(
        headers
    )
    balance = receipt_total[0][0] - voucher_total[0][0]
    if balance < 0:
        comment = "Expenditure over Income"
        color = "red"
    else:
        comment = "Income over Expenditure"
        color = "blueviolet"
    return (
        income_row,
        expense_row,
        receipt_total,
        voucher_total,
        comment,
        balance,
        color,
    )


def create_company():
    if request.method == "POST":
        id = random.randint(1, 10)
        company = request.form["name"]
        gst = request.form["gst"]
        address = request.form["address"]
        status = mapper.create_company(id, company, gst, address)
        return status
