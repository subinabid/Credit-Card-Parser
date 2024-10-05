# Credit Card Transaction Parser

Parses the text from a credit card bill to extract the date, category, amount and vendor for each transaction and exports a csv summary.

## Setup / Installation

- Clone the repo
- The project uses [uv](https://docs.astral.sh/uv/) for package and project management
- Python version is `3.12`
- Activate with `uv init`
- Initiate the database with  ```uv run db.py```

A `database.db` file is created in the root folder. While parsing each file, the new vendors found in the bill are added to the `vendors` table. The 2 fields `short_name` and `category` may be modified to suit your requirement for each case, if required,

## Usage

Copy the transaction text from the Credit card bill to a text file in the root folder and run the command ```uv run app.py filename.txt bankname```

eg: ```uv run app.py txn.txt hdfc```

Run ```uv run app.py -h``` for help.
