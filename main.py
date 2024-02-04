import json
from datetime import datetime
from utilities import is_valid_date
from transaction_validator import check_transaction_dates
from transaction_analysis import calculate_rewards

# Function to load and update points history
def load_update_points_history(points_file, current_month, current_points):
    try:
        with open(points_file, 'r') as file:
            points_data = json.load(file)
    except FileNotFoundError:
        points_data = {"points_history": []} 

    points_history = points_data.get("points_history", [])

    # Update points for the current month
    points_history.append({"month": current_month, "points": current_points})

    # Keep only the last 6 months
    points_history = points_history[-6:]

    # Save updated points history
    points_data["points_history"] = points_history
    with open(points_file, 'w') as file:
        json.dump(points_data, file, indent=2)

# Function to add a new transaction
def add_transaction(transactions):
    # User input for whether to add a transaction
    add_new_transaction = input("Do you want to add a new transaction? (yes/no): ").lower()

    if add_new_transaction != 'yes':
        print("No new transaction added.")
        return

    # User input for the new transaction
    new_date = input("Enter the transaction date (YYYY-MM-DD): ")
    new_merchant_code = input("Enter the merchant code: ")
    new_amount_dollars = float(input("Enter the transaction amount in dollars: "))

    # Convert the amount to cents
    new_amount_cents = int(new_amount_dollars * 100)

    # Check if the new date matches the specified month and year
    new_year, new_month, _ = map(int, new_date.split('-'))
    if new_year != transactions['year'] or new_month != transactions['month']:
        print("Error: The entered date does not match the specified month and year.")
        return

    # Add the new transaction to the transactions dictionary
    new_transaction_id = f"T{len(transactions['transactions']) + 1}"
    new_transaction_info = {
        'date': new_date,
        'merchant_code': new_merchant_code,
        'amount_cents': new_amount_cents
    }

    transactions['transactions'][new_transaction_id] = new_transaction_info
    print(f"Transaction {new_transaction_id} added successfully.")

    # Update the transactions.json file
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file, indent=2)

# Function to remove a transaction
def remove_transaction(transactions):
    # Prompt the user to see if they want to remove a transaction
    remove_transaction_option = input("Do you want to remove a transaction? (yes/no): ").lower()

    if remove_transaction_option != 'yes':
        print("No transaction removed.")
        return

    # User input for removing a transaction
    remove_transaction_id = input("Enter the ID of the transaction you want to remove (e.g., T1): ")

    # Check if the provided transaction ID exists
    if remove_transaction_id not in transactions['transactions']:
        print(f"Transaction {remove_transaction_id} not found.")
        return

    # Remove the transaction
    removed_transaction = transactions['transactions'].pop(remove_transaction_id)
    print(f"Transaction {remove_transaction_id} removed successfully.")

    # Update the transactions.json file
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file, indent=2)

# Read input data from file
file_path = 'transactions.json'
with open(file_path, 'r') as file:
    input_data = json.load(file)

# Check transaction dates
incorrect_transactions = check_transaction_dates(input_data)

if not incorrect_transactions:
    print("All transactions have valid dates.")
else:
    print("Incorrect transactions:")
    for transaction in incorrect_transactions:
        print(f"Transaction {transaction['transaction_id']} with date {transaction['date']} has an {transaction['error_type']}.")

# Get the month and year from transactions.json
transactions_month = input_data.get("month")
transactions_year = input_data.get("year")

while True:
    # Prompt the user to add, remove, or perform analysis
    action = input("Do you want to add, remove, or perform analysis on transactions? (add/remove/analysis/done): ").lower()

    if action == 'add':
        # Prompt the user to add a new transaction
        add_transaction(input_data)
    elif action == 'remove':
        # Prompt the user to remove a transaction
        remove_transaction(input_data)
    elif action == 'analysis':
        # Perform analysis
        # Define the rules to apply
        selected_rules = [1, 2, 3, 4, 5, 6]

        # Call calculate_rewards with selected_rules
        total_rewards, transaction_rewards = calculate_rewards(file_path, selected_rules)

        # Load previous points history
        points_file = 'points_history.json'
        current_month = f"{transactions_year}-{transactions_month:02}"

        try:
            with open(points_file, 'r') as file:
                points_data = json.load(file)
        except FileNotFoundError:
            points_data = {"points_history": []}

        # Calculate average points earned in the last 6 months
        last_six_months_points = points_data.get("points_history", [])[-6:]
        average_last_six_months = sum(entry["points"] for entry in last_six_months_points) / max(len(last_six_months_points), 1)

        print(f"Total Maximum Reward Points for the Month: {total_rewards}")

        if last_six_months_points:
            # Calculate percentage above or below the average
            percentage_difference = ((total_rewards - average_last_six_months) / average_last_six_months) * 100
            print(f"Percentage difference from the average points earned in the last 6 months: {percentage_difference:.2f}%")
        else:
            print("No points history available for comparison.")

        print("Maximum Reward Points Applied for Each Transaction:")
        for transaction_id, reward in transaction_rewards.items():
            print(f"Transaction {transaction_id}: {reward} points")

        # Ask the user if they want to add this month's points to the history
        add_to_history = input("Do you want to add this month's points to the history? (yes/no): ").lower()
        if add_to_history == 'yes':
            load_update_points_history(points_file, current_month, total_rewards)
            print("Points added to history.")

    elif action == 'done':
        print("Exiting the program. Have a great day!")
        break
    else:
        print("Invalid action. Please choose 'add', 'remove', 'analysis', or 'done'.")

# Update the file with the modified transactions
with open(file_path, 'w') as file:
    json.dump(input_data, file, indent=2)
