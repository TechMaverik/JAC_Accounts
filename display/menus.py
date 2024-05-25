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
    "Active Members": "/",
    "Add Members": "/add_members",
    "Create Ledger": "/create_ledger",
    "View Ledger": "/view_ledger",
    "Cash Book": "/cashbook",
    "Income and Expense": "/income_expense",
    "Settings": "/settings",
}

gender = ["-", "Male", "Female"]
yes_no = ["-", "Yes", "No"]
receipt_payment = ["Receipt", "Voucher"]
ledger_list_table = ["#", "Ledger Head", "Action"]
ledger_view_table_head = [
    "Date",
    "No",
    "Receipt/Voucher",
    "Party Details",
    "Amount (INR)",
]
cashbook_table = [
    "Date",
    "No",
    "Receipt/Voucher",
    "Party Details",
    "Amount(INR)",
]
payment_type = ["Cash", "Cheque"]
income_table = [
    "Date",
    "No",
    "Receipt",
    "Party Details",
    "Amount(INR)",
]
