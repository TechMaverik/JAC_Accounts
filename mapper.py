import sqlite3
import database

try:
    database.create_members()
except:
    pass
try:
    database.create_ledger()
except:
    pass
try:
    database.create_company()
except:
    pass
try:
    database.create_opening_balance()
except:
    pass


def add_members(model):
    counter_file = open("static/counter.txt", "r")
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
        counter_file = open("static/counter.txt", "w")
        data = int(data) + 1
        counter_file.write(str(data))
        counter_file.close()
    conn.close()
    return True


def view_members():
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
            "INSERT into LedgerHeads(id,name,company)Values(?,?,?)",
            (
                model.id,
                model.name,
                model.company,
            ),
        )
        conn.commit()
    conn.close()
    try:
        database.create_ledger_tables()
    except:
        print("Cant create tables")


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
    ID,
    name,
    payment_type,
    payment_method,
    ledger_head,
    date,
    amount,
    dynamic_id,
):
    with sqlite3.connect("jac_accounts.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT into "
            + ledger_head
            + "(id , name , dynamic_id , amount , date , cash_cheque , payment_type, header ) Values(?,?,?,?,?,?,?,?)",
            (
                ID,
                name,
                dynamic_id,
                amount,
                date,
                payment_method,
                payment_type,
                ledger_head,
            ),
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
        cursor.execute(
            "Select SUM(amount) FROM " + header + " WHERE payment_type='Income'"
        )
        receipt_sum = cursor.fetchall()
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "Select SUM(amount) FROM " + header + " WHERE payment_type='Expense'"
        )
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
    # query = query + " OpeningBalance"
    return query


def cashbook(header):
    query = generate_cashbook_query(header)
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query + " ORDER BY date DESC")
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
            + "WHERE payment_type='Income'"
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
            + "WHERE payment_type='Expense'"
        )
        voucher_amount = cursor.fetchall()
    conn.close()
    return rows, receipt_amount, voucher_amount


def add_opening_balance(id, amount):
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "Insert into OpeningBalance(id,amount) Values(?,?)",
            (
                id,
                amount,
            ),
        )
        conn.commit()
    conn.close()


def get_opening_balance():
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM OpeningBalance")
        rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows


def generate_income_expense_query(headers_list, receipt_payment):
    UNION = " UNION "
    SELECT_QUERY = "SELECT * FROM "
    queryList = []
    for head in headers_list:
        query = (
            SELECT_QUERY
            + head
            + " WHERE payment_type='"
            + receipt_payment
            + "'"
            + UNION
        )
        queryList.append(query)
    listToStr = " ".join([str(elem) for elem in queryList])
    query = listToStr[: listToStr.rfind("UNION")]
    return query


def income_expense(headers):
    query = generate_income_expense_query(headers, "Income")
    print(query)
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query + " ORDER BY date DESC")
        income_row = cursor.fetchall()

    conn.close()
    query = generate_income_expense_query(headers, "Expense")
    print(query)
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query + " ORDER BY date DESC")
        expense_row = cursor.fetchall()
    conn.close()

    with sqlite3.connect("jac_accounts.db") as conn:
        query = generate_cashbook_query(headers)
        cursor = conn.cursor()
        cursor.execute(
            "Select SUM(amount) AS Total_Amount FROM "
            + "("
            + query
            + ")"
            + "WHERE payment_type='Income'"
        )
        receipt_total = cursor.fetchall()

    with sqlite3.connect("jac_accounts.db") as conn:
        query = generate_cashbook_query(headers)
        cursor = conn.cursor()
        cursor.execute(
            "Select SUM(amount) AS Total_Amount FROM "
            + "("
            + query
            + ")"
            + "WHERE payment_type='Expense'"
        )
        voucher_total = cursor.fetchall()

    conn.close()

    return (income_row, expense_row, receipt_total, voucher_total)


def create_company(id, name, gst, address):
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT into Company(id , company , gst , address ) VALUES(?,?,?,?)",
            (
                id,
                name,
                gst,
                address,
            ),
        )
        conn.commit()
    conn.close()
    return True


def get_company_details():
    with sqlite3.connect("jac_accounts.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Company")
        rows = cursor.fetchall()
    conn.close()
    return rows


def get_expense_plotting_data():
    with sqlite3.connect("jac_accounts.db") as conn:

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS HospitalExpense FROM HospitalExpense")
        hospital_expense_amt = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS CarLoan FROM CarLoan")
        car_loan_amt = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) FROM EMI")
        emi_amt = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS Electricity_bill FROM Electricity_bill")
        electricity_bill = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS Food FROM Food")
        food_amt = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS Groceries FROM Groceries")
        groceries_amt = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS HouseRent FROM HouseRent")
        house_rent_amt = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS Infotainment FROM Infotainment")
        infotainment_amt = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS Others FROM Others")
        others_amt = cursor.fetchall()

        cursor = conn.cursor()
        cursor.execute("Select SUM(amount) AS Steam FROM Steam")
        steam_amt = cursor.fetchall()

    conn.close()
    return (
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
    )


def delete_all_table_contents(ledger_heads):
    with sqlite3.connect("jac_accounts.db") as conn:
        cur = conn.cursor()
        for head in ledger_heads:
            cur.execute("DELETE from " + str(head))
            conn.commit()
    conn.close()
    counter_file = open("static/receipt_counter.txt", "w")
    counter_file.write(str(1))
    counter_file.close()
    counter_file = open("static/voucher_counter.txt", "w")
    counter_file.write(str(1))
    counter_file.close()
    counter_file = open("static/opening_balance.txt", "w")
    counter_file.write(str(1))
    counter_file.close()
