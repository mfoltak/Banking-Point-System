import json
from utilities import is_valid_date

def check_transaction_dates(transactions):
    month = transactions['month']
    year = transactions['year']
    transaction_data = transactions['transactions']

    incorrect_transactions = []

    for transaction_id, transaction_info in transaction_data.items():
        transaction_date = transaction_info['date']

        # Check if the date is in the correct format and valid
        if not is_valid_date(transaction_date):
            incorrect_info = {
                'transaction_id': transaction_id,
                'date': transaction_date,
                'error_type': 'invalid date format'
            }
            incorrect_transactions.append(incorrect_info)
            continue

        transaction_year, transaction_month, _ = map(int, transaction_date.split('-'))

        # Check if the year and month match the specified values
        if transaction_year != year or transaction_month != month:
            error_type = ''
            if transaction_year != year:
                error_type += 'incorrect year'
            if transaction_month != month:
                error_type += ' and ' if error_type else ''
                error_type += 'incorrect month'

            incorrect_info = {
                'transaction_id': transaction_id,
                'date': transaction_date,
                'error_type': error_type
            }
            incorrect_transactions.append(incorrect_info)

    return incorrect_transactions
