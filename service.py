from flask import request
from models.add_members import AddMembers
from models.ledger import LedgerHead
import mapper
import random
import database


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
            id=lh_id,
            name=request.form["head"],
        )
        with open("static\ledger.txt", "a") as file:
            file.writelines(str(request.form["head"]))
            file.write("\n")
            file.close()
        mapper.create_ledger(ledgerHead)


def get_ledgerlist():
    clean_ledger_list = []
    with open("static\ledger.txt", "r") as file:
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

        with open("static\ledger.txt", "w") as file:
            ledgerList.remove(name)
            for data in ledgerList:
                file.writelines(str(data) + "\n")
            file.close()
        mapper.delete_ledgerhead(name)


def generate_receipt():
    if request.method == "POST":
        counter_file = open("static\cashbook_counter.txt", "r")
        data = int(counter_file.read())
        counter_file.close()
        ledger_head_list = get_ledgerlist()
        try:
            database.create_ledger_tables()
        except:
            pass

        for item in ledger_head_list:
            payment_type = request.form.get("payment_type")
            if payment_type == "Receipt":
                receipt = request.form.get(str(item))
                voucher = 0
            else:
                receipt = 0
                voucher = request.form.get(str(item))
            name = request.form.get("name")
            date = request.form.get("date")
            payment_method = request.form.get("payment_method")
            R_id = data
            print(
                R_id, name, date, receipt, voucher, payment_method, item, payment_type
            )

            mapper.generate_receipt(
                R_id,
                name,
                date,
                receipt,
                voucher,
                payment_method,
                item,
                payment_type,
            )
        counter_file = open("static\cashbook_counter.txt", "w")
        data = int(data) + 1
        counter_file.write(str(data))
        counter_file.close()


def view_ledger():
    if request.method == "POST":
        head = request.form.get("head")
        rows, receipt_sum, voucher_sum = mapper.view_ledger(head)
        return rows, receipt_sum, voucher_sum, head


def cashbook():
    headers = get_ledgerlist()
    rows, receipt_amount, voucher_amount = mapper.cashbook(header=headers)
    rct = receipt_amount[0][0]
    vchr = voucher_amount[0][0]
    balance = rct - vchr
    return rows, receipt_amount, voucher_amount, balance
