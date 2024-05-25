import sqlite3
import service
import database


def erase_all_data():
    ledger_header_list = service.get_ledgerlist()
    table_list = [
        "Members",
        "LedgerHeads",
        "OpeningBalance",
    ]

    ledger_cache_path = "static/ledger.txt"
    cache_file_path = [
        "static/receipt_counter.txt",
        "static/voucher_counter.txt",
        "static/counter.txt",
    ]

    with sqlite3.connect("jac_accounts.db") as conn:

        for table in table_list:
            try:
                query = "DROP Table " + table
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
            except:
                print("Cannot find " + table)

        for table in ledger_header_list:
            try:
                query = "DROP Table " + table
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
            except:
                print("Cannot find " + table)

        with open(ledger_cache_path, "w") as file:
            file.write("")
            file.close()

        for path in cache_file_path:
            with open(path, "w") as file:
                file.write("1")
            file.close()

    conn.close()
    database.create_members()
    database.create_ledger()
    database.create_opening_balance()
    return True
