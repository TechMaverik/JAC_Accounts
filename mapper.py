import sqlite3
import database
import service


def add_members(model):
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


def view_members():
    try:
        database.create_members()
        database.create_ledger()
        database.create_cashbook()
    except:
        pass
    with sqlite3.connect("jac_accounts.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * from Members")
        rows = cur.fetchall()
    conn.close
    return rows


def delete_member(id):
    with sqlite3.connect("jac_accounts.db") as conn:
        cur = conn.cursor()
        cur.execute("DELETE from Members where id=?", (id,))
        conn.commit()
    conn.close()


def create_ledger(model):
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


def view_ledger_head():
    with sqlite3.connect("jac_accounts.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * from LedgerHeads")
        rows = cur.fetchall()
    conn.close()
    return rows


def delete_ledgerhead(name):
    with sqlite3.connect("jac_accounts.db") as conn:
        cur = conn.cursor()
        cur.execute("DELETE from LedgerHeads where name=?", (name,))
        conn.commit()
    conn.close()


def generate_receipt(
    R_id,
    name,
    date,
    receipt,
    voucher,
    payment_method,
    item,
    payment_type,
):
    with sqlite3.connect("jac_accounts.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT into "
            + item
            + "(id , name , date  , receipt_amount , voucher_amount , payment_method, payment_type ) Values(?,?,?,?,?,?,?)",
            (R_id, name, date, receipt, voucher, payment_method, payment_type),
        )
        conn.commit()
    conn.close()


def view_ledger(header):
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("Select * from " + header)
        rows = cursor.fetchall()
    conn.close()

    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("Select SUM(receipt_amount) FROM " + header)
        receipt_sum = cursor.fetchall()
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("Select SUM(voucher_amount) FROM " + header)
        voucher_sum = cursor.fetchall()
    conn.close()

    return rows, receipt_sum, voucher_sum


def generate_cashbook_query(x):
    UNION = " UNION "
    SELECT_QUERY = "SELECT * FROM "
    queryList = []
    for head in x:
        query = SELECT_QUERY + head + UNION
        queryList.append(query)
    listToStr = " ".join([str(elem) for elem in queryList])
    query = listToStr[: listToStr.rfind("UNION")]
    return query


def cashbook(header):
    query = generate_cashbook_query(header)
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    conn.close()
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "Select SUM(receipt_amount) AS Total_Amount FROM " + "(" + query + ")"
        )
        receipt_amount = cursor.fetchall()
    conn.close()
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "Select SUM(voucher_amount) AS Total_Amount FROM " + "(" + query + ")"
        )
        voucher_amount = cursor.fetchall()
    conn.close()
    return rows, receipt_amount, voucher_amount
