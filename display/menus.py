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
    "Settings": "",
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
