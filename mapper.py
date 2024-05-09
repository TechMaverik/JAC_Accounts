import sqlite3
import database


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
            "INSERT into LedgerHeads(id,name,type)Values(?,?,?)",
            (
                model.id,
                model.name,
                model.type,
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


def generate_receipt(R_id, name, date, amount, item):
    with sqlite3.connect("jac_accounts.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT into " + item + "(id , name , date  , amount ) Values(?,?,?,?)",
            (
                R_id,
                name,
                date,
                amount,
            ),
        )
        conn.commit()
    conn.close()


def view_ledger():
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("Select * from Receipt")
        rows = cursor.fetchall()
    conn.close()
    return rows
