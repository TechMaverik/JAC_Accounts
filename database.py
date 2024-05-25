import sqlite3
import logging
import service

logger = logging.getLogger(__name__)
logging.basicConfig(filename="jac_accounts.log", encoding="utf-8", level=logging.DEBUG)


def create_members():
    """Create members table"""
    con = sqlite3.connect("jac_accounts.db")
    con.execute(
        "Create table Members(id VARCHAR,name VARCHAR,address VARCHAR,gender VARCHAR,dob VARCHAR,voting_power VARCHAR,married VARCHAR,contact_no VARCHAR,whatsapp_no VARCHAR,dom VARCHAR,spouse_name VARCHAR,nos_children VARCHAR,subscription VARCHAR)"
    )
    con.close()
    logging.info(msg="Members Table Created")


def create_ledger():
    con = sqlite3.connect("jac_accounts.db")
    con.execute("Create table LedgerHeads(id VARCHAR, name VARCHAR)")
    con.close()
    logging.info(msg="Ledger Table Created")


def create_ledger_tables():
    ledger_header_list = service.get_ledgerlist()
    con = sqlite3.connect("jac_accounts.db")

    for head in ledger_header_list:
        try:
            con.execute(
                "Create table "
                + head
                + "(id VARCHAR, name VARCHAR, dynamic_id VARCHAR, amount VARCHAR, date VARCHAR, cash_cheque VARCHAR, payment_type VARCHAR)"
            )
            logging.info(msg=head + " Table Created")
            con.close()
            print("Created custom ledger head table in DB --->" + head)
        except:
            print("Cant create custom ledger head tables in DB ---> " + head)


def create_opening_balance():
    con = sqlite3.connect("jac_accounts.db")
    con.execute("Create table OpeningBalance(amount VARCHAR DEFAULT 0 NOT NULL)")
    con.close()
    logging.info(msg="Ledger Table Created")
