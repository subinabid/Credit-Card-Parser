# Credit Card Transaction Parser

Parses the text from a credit card bill to extract the date, category, amount and vendor for each transaction and exports a csv summary.

## Setup / Installation

- Clone the repo
- Run the db.py module ```python3 db.py```

A `database.db` file is created in the root folder. While parsing each file, the new vendors found in the bill are added to the `vendors` table. The 2 fields `short_name` and `category` may be modified to suit your requirement for each case, if required,

## Usage

Copy the transaction text from the Credit card bill to a text file in the root folder and run the command ```python3 app.py filename.txt bankname``` 

eg: ```python3 app.py txn.txt hdfc```

Run ```python3 app.py -h``` for help.
