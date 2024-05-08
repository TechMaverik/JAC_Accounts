import sqlite3
import logging

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
    con.execute("Create table LedgerHeads(id VARCHAR, name VARCHAR, type VARCHAR)")
    con.close()
    logging.info(msg="Ledger Table Created")


def create_receipt():
    con = sqlite3.connect("jac_accounts.db")
    con.execute(
        "Create table Receipt(id VARCHAR, name VARCHAR, date  VARCHAR,item VARCHAR, head VARCHAR)"
    )
    con.close()
    logging.info(msg="Receipt Table Created")


create_members()
create_ledger()
create_receipt()
