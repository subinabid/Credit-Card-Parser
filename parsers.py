"""Parser for Credit card bills"""

from datetime import datetime


def parse_axis(file):
    """Parse Axis credit card bill and return the transactions."""
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


def parse_hdfc(file):
    """Parse HDFC credit card bill and return the transactions."""
    transactions = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue

            try:
                test_string1 = line[12:19]
                tx_time = datetime.strptime(test_string1, "%H:%M:%S")
                tx_date = line[0:19]
                tx_date = datetime.strptime(tx_date, "%d/%m/%Y %H:%M:%S")
                line = line[20:]
            except ValueError:
                # test_string1 is not a valid time
                tx_time = None
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
            amount = line[last_space:]
            amount = amount.replace(",", "")
            amount = float(amount)
            amount = amount * -1 if credit else amount

            transaction = {}
            transaction["date"] = tx_date
            transaction["time"] = True if tx_time else None
            transaction["vendor"] = vendor
            transaction["amount"] = amount
            transaction["credit"] = credit
            transaction["source"] = "HDFC"

            transactions.append(transaction)
    return transactions


def parse_icici(file):
    """Parse ICICI credit card bill and return the transactions."""
    transactions = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue

            tx_date = line[0:10]
            tx_date = datetime.strptime(tx_date, "%d/%m/%Y")
            line = line[22:]

            credit = False

            if line[-2:].lower() == "cr":
                credit = True
                line = line[0:-3]

            spaces = [i for i, char in enumerate(line) if char == " "]
            last_space = spaces[-1]
            amount = line[last_space:]
            amount = amount.replace(",", "")
            amount = float(amount)
            amount = amount * -1 if credit else amount
            vendor = line[: spaces[-2]]

            transaction = {}
            transaction["date"] = tx_date
            transaction["vendor"] = vendor
            transaction["amount"] = amount
            transaction["credit"] = credit
            transaction["source"] = "ICICI"

            transactions.append(transaction)

    return transactions


def parse_yes(file):
    """Parse Yesbank credit card bill and return the transactions."""
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
            vendor_space = spaces[-2]
            vendor = line[:vendor_space]
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
