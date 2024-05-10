"menus.py"
add_members_menu = [
    "#",
    "Name",
    "Address",
    "Date of birth",
    "Contact No",
    "Married",
    "Subscription",
    "Action",
]

dashboard_menus = {
    "ActiveMembers": "/",
    "AddMembers": "/add_members",
    "CreateLedger": "/create_ledger",
    "ViewLedger": "/view_ledger",
    "CashBook": "/cashbook",
    "BankAccounts": "",
    "Receipts&Payments": "",
    "Income&Expenditure": "",
    "BalanceSheet": "",
    "Administration": "",
    "Office": "",
    "Settings": "",
}

gender = ["-", "Male", "Female"]
yes_no = ["-", "Yes", "No"]
payment_type = ["Receipt", "Payment"]
ledger_list_table = ["#", "Ledger Head", "Type", "Action"]
ledger_view_table_head = ["Date", "Receipt No", "Description", "Amount (INR)"]
cashbook_table = [
    "Date",
    "Receipt",
    "Party Details",
    "Amount",
]
