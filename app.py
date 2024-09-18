"""A parser to analyse credit card transactions from the bill."""

import os
import argparse
import sqlite3
from bank_hdfc import parse_hdfc
from bank_yesbank import parse_yes
from bank_axis import parse_axis

import csv


PARSE_FUNCTIONS = {
    "hdfc": parse_hdfc,
    "yes": parse_yes,
    "axis": parse_axis,
}

banklist = [keys for keys in PARSE_FUNCTIONS.keys()]


def export_csv(transactions: list[dict]):
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
        print(f"{len(vendors)} Vendors fetched successfully.")
        return vendors
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {
            "error": {
                "message": "An error occurred while fetching vendors from the database.",
                "type": "database_error",
            }
        }


def add_vendor(
    bank_name: str, short_name: str, category: str, name_source: str
) -> dict:
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
        conn.close()
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


def delete_vendor(bank_name: str) -> dict:
    """Delete a vendor from the database."""
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendors WHERE bank_name=?", (bank_name,))
        row = cursor.fetchone()
        if not row:
            return {
                "message": "Vendor does not exist in the database.",
                "type": "info",
            }
        # Delete the vendor from the database
        cursor.execute("DELETE FROM vendors WHERE bank_name=?", (bank_name,))
        conn.commit()
        conn.close()
        return {
            "message": f"Vendor {bank_name} deleted successfully.",
            "type": "success",
        }
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return {
            "error": {
                "message": "An error occurred while deleting the vendor from the database.",
                "type": "database_error",
            }
        }


def categorize_transaction(
    transactions: list[dict], vendors: dict, bank: str
) -> list[dict]:
    """Categorize the transaction based on the vendor."""
    for transaction in transactions:
        if transaction["vendor"] in vendors.keys():
            transaction["category"] = vendors[transaction["vendor"]]["category"]
            transaction["vendor"] = vendors[transaction["vendor"]]["short_name"]
        else:
            transaction["category"] = "Misc"
            add_vendor(
                transaction["vendor"], transaction["vendor"], "Misc", bank.lower()
            )
    return transactions


def main(file, bank):
    """Parse the credit card bill and print the transactions."""

    # Check if the file exists
    if not os.path.exists(file):
        print("File not found. Please check the file path and try again.")
        return {"error": "File not found. Please check the file path and try again."}

    print("Parsing the credit card bill...")
    print(f"Bank: {bank}")
    print(f"File {file} found.")
    vendors = get_vendors()

    if "error" in vendors:
        print(vendors["error"]["message"])
        return {"error": vendors["error"]["message"]}

    # Get the appropriate parsing function based on the bank
    parse_function = PARSE_FUNCTIONS.get(bank.lower())

    if not parse_function:
        print("Bank not supported.")
        print(f"Supported banks: {banklist}")
        return {"error": "Bank not supported."}

    try:
        transactions = parse_function(file)
        transactions = categorize_transaction(transactions, vendors, bank)
        print("Transactions parsed successfully.")
    except Exception as e:
        print(f"An error occurred while parsing the file: {e}")
        return {"error": f"An error occurred while parsing the file: {e}"}

    export_csv(transactions)
    return {"message": "Transactions parsed successfully."}


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
