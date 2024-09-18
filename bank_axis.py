"""Parser for HDFC bank"""

from datetime import datetime


def parse_axis(file):
    """Parse the credit card bill and return the transactions."""
    transactions = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue

            tx_date = line[0:10]
            tx_date = datetime.strptime(tx_date, "%d/%m/%Y")
            line = line[11:]

            credit = False

            if line[-2:] == "Cr":
                credit = True

            line = line[0:-3]
            spaces = [i for i, char in enumerate(line) if char == " "]
            last_space = spaces[-1]
            vendor = line[:last_space]
            vendor = vendor[: vendor.find(" - Ref No:")]
            amount = line[last_space:]
            amount = amount.replace(",", "")
            amount = float(amount)
            amount = amount * -1 if credit else amount

            transaction = {}
            transaction["date"] = tx_date
            transaction["vendor"] = vendor
            transaction["amount"] = amount
            transaction["credit"] = credit
            transaction["source"] = "Yes Bank"

            transactions.append(transaction)
    return transactions
