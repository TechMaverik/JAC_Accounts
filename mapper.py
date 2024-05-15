import sqlite3
import database
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="jac_accounts.log", encoding="utf-8", level=logging.DEBUG)


def add_members(model):
    try:
        counter_file = open("static\counter.txt", "r")
        data = int(counter_file.read())
        counter_file.close()

        with sqlite3.connect("jac_accounts.db") as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT into Members (id ,name ,address ,gender ,dob ,voting_power ,married ,contact_no ,whatsapp_no ,dom ,spouse_name ,nos_children ,subscription) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    data,
                    model.name,
                    model.address,
                    model.gender,
                    model.dob,
                    model.voting_power,
                    model.married,
                    model.contact_no,
                    model.whatsapp_no,
                    model.dom,
                    model.spouse_name,
                    model.nos_children,
                    model.subscription,
                ),
            )
            conn.commit()
            counter_file = open("static\counter.txt", "w")
            data = int(data) + 1
            counter_file.write(str(data))
            counter_file.close()
        conn.close()
        return True
    except:
        logging.error(msg="Cannot Insert to Members")


def create_database():
    try:
        database.create_members()
        database.create_ledger()
    except:
        pass


def view_members():
    create_database()
    try:
        with sqlite3.connect("jac_accounts.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * from Members")
            rows = cur.fetchall()
        conn.close
        return rows
    except:
        logging.error(msg="Cannot Select from Members")


def delete_member(id):
    try:
        with sqlite3.connect("jac_accounts.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE from Members where id=?", (id,))
            conn.commit()
        conn.close()
    except:
        logging.error(msg="Cannot Delete Members")


def create_ledger(model):
    try:
        with sqlite3.connect("jac_accounts.db") as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT into LedgerHeads(id,name)Values(?,?)",
                (
                    model.id,
                    model.name,
                ),
            )
            conn.commit()
        conn.close()
    except:
        logging.error(msg="Cannot Insert to LedgerHeads")


def view_ledger_head():
    try:
        with sqlite3.connect("jac_accounts.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * from LedgerHeads")
            rows = cur.fetchall()
        conn.close()
        return rows
    except:
        logging.error(msg="Cannot Select LedgerHeads")


def delete_ledgerhead(name):
    try:
        with sqlite3.connect("jac_accounts.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE from LedgerHeads where name=?", (name,))
            conn.commit()
        conn.close()
    except:
        logging.error(msg="Cannot Delete LedgerHeads")


def generate_receipt(
    ID,
    name,
    payment_type,
    payment_method,
    ledger_head,
    date,
    amount,
    dynamic_id,
):
    try:
        with sqlite3.connect("jac_accounts.db") as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT into "
                + ledger_head
                + "(id , name , dynamic_id , amount , date , cash_cheque , payment_type ) Values(?,?,?,?,?,?,?)",
                (
                    ID,
                    name,
                    dynamic_id,
                    amount,
                    date,
                    payment_method,
                    payment_type,
                ),
            )
            conn.commit()
        conn.close()
    except:
        logging.error(msg="Cannot Insert to custom ledger head")


def view_ledger(header):
    try:
        with sqlite3.connect("jac_accounts.db") as conn:
            cursor = conn.cursor()
            cursor.execute("Select * from " + header)
            rows = cursor.fetchall()
        conn.close()
    except:
        logging.error(msg="Cannot Select from custom ledger head")

    try:
        with sqlite3.connect("jac_accounts.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "Select SUM(amount) FROM " + header + " WHERE payment_type='Receipt'"
            )
            receipt_sum = cursor.fetchall()
    except:
        logging.error(msg="Cannot get sum of amount from header " + header)
    with sqlite3.connect("jac_accounts.db") as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "Select SUM(amount) FROM " + header + " WHERE payment_type='Voucher'"
            )
            voucher_sum = cursor.fetchall()
        except:
            logging.error(msg="Cannot get sum of amount from header " + header)
    conn.close()

    return rows, receipt_sum, voucher_sum


def generate_cashbook_query(header_list):
    UNION = " UNION "
    SELECT_QUERY = "SELECT * FROM "
    queryList = []
    for head in header_list:
        query = SELECT_QUERY + head + UNION
        queryList.append(query)
    listToStr = " ".join([str(elem) for elem in queryList])
    query = listToStr[: listToStr.rfind("UNION")]
    return query


def cashbook(header):
    try:
        query = generate_cashbook_query(header)
        with sqlite3.connect("jac_accounts.db") as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            # + "WHERE receipt_amount AND voucher_amount != 0"
            rows = cursor.fetchall()
        conn.close()
        with sqlite3.connect("jac_accounts.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "Select SUM(amount) AS Total_Amount FROM "
                + "("
                + query
                + ")"
                + "WHERE payment_type='Receipt'"
            )
            receipt_amount = cursor.fetchall()
        conn.close()
        with sqlite3.connect("jac_accounts.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "Select SUM(amount) AS Total_Amount FROM "
                + "("
                + query
                + ")"
                + "WHERE payment_type='Voucher'"
            )
            voucher_amount = cursor.fetchall()
        conn.close()
        return rows, receipt_amount, voucher_amount
    except:
        logging.error(msg="Cannot Load Cashbook")
