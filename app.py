"""A parser to analyse credit card transactions from the bill."""

import os
import argparse
import sqlite3
from bank_hdfc import parse_hdfc
import csv


class Bank:
    """Class to define the supported banks."""

    HDFC = "hdfc"
    ICICI = "icici"
    SBI = "sbi"
    YESBANK = "yesbank"
    CITI = "citi"


banklist = [Bank.HDFC, Bank.ICICI, Bank.SBI, Bank.YESBANK, Bank.CITI]


def export_csv(transactions):
    """Export the transactions to a CSV file."""
    csv_filename = "transactions.csv"
    fieldnames = [
        "date",
        "category",
        "amount",
        "source",
        "vendor",
    ]

    # Open the CSV file in write mode
    with open(csv_filename, "w", newline="") as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the transactions data
        for transaction in transactions:
            transaction.pop("time", None)
            transaction.pop("credit", None)
            transaction["date"] = transaction["date"].strftime("%d/%m/%Y")
            writer.writerow(transaction)

    print(f"Transactions exported to {csv_filename} successfully.")


def get_vendors() -> dict[str, dict]:
    """Get the list of vendors from the database."""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendors")
        rows = cursor.fetchall()
        vendors = {}
        for row in rows:
            vendors[row[0]] = {
                "short_name": row[1],
                "category": row[2],
            }
        return vendors
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {
            "error": {
                "message": "An error occurred while fetching vendors from the database.",
                "type": "database_error",
            }
        }


def add_vendor(bank_name, short_name, category, name_source):
    """Add a new vendor to the database."""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendors WHERE bank_name=?", (bank_name,))
        row = cursor.fetchone()
        if row:
            return {
                "message": "Vendor already exists in the database.",
                "type": "info",
            }
        # Add the vendor to the database if not already present
        cursor.execute(
            "INSERT INTO vendors VALUES (?, ?, ?, ?)",
            (bank_name, short_name, category, name_source),
        )
        conn.commit()
        return {
            "message": f"Vendor {bank_name} added successfully.",
            "type": "success",
        }
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {
            "error": {
                "message": "An error occurred while adding the vendor to the database.",
                "type": "database_error",
            }
        }


def main(file, bank):
    """Parse the credit card bill and print the transactions."""

    # Check if the file exists
    if not os.path.exists(file):
        print("File not found. Please check the file path and try again.")
        return

    # Check if the bank is supported
    if bank.lower() not in banklist:
        print("Bank not supported.")
        print(f"Supported banks: {banklist}")
        return

    vendors = get_vendors()

    if bank.lower() == Bank.HDFC:
        transactions = parse_hdfc(file)

    for transaction in transactions:
        if transaction["vendor"] in vendors.keys():
            transaction["category"] = vendors[transaction["vendor"]]["category"]
            transaction["vendor"] = vendors[transaction["vendor"]]["short_name"]
        else:
            transaction["category"] = "Misc"
            add_vendor(
                transaction["vendor"], transaction["vendor"], "Misc", bank.lower()
            )

    export_csv(transactions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Credit Card Bill Parser",
        description="Parse the credit card bill and print the transactions.",
        epilog="Happy parsing :)",
    )
    parser.add_argument("file", help="The credit card bill txt file to parse")
    parser.add_argument("bank", help="The issuing bank", type=str)
    args = parser.parse_args()

    main(args.file, args.bank)
