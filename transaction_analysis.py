import json
from itertools import combinations
import math

def calculate_transaction_rewards(transaction_info, selected_rules):
    merchant_code = transaction_info['merchant_code']
    amount_cents = transaction_info['amount_cents'] / 100

    max_transaction_points = 0

    sport_check_amount = 0
    tim_hortons_amount = 0
    subway_amount = 0
    other_amount = 0

    if merchant_code == 'sportcheck':
        sport_check_amount = amount_cents
    elif merchant_code == 'tim_hortons':
        tim_hortons_amount = amount_cents
    elif merchant_code == 'subway':
        subway_amount = amount_cents
    else:
        other_amount = amount_cents

    for rule in selected_rules:
        rule_points = 0

        if rule == 1 and sport_check_amount >= 75 and tim_hortons_amount >= 25 and subway_amount >= 25:
            rule_points += 500
            sport_check_amount -= 75
            tim_hortons_amount -= 25
            subway_amount -= 25

        elif rule == 2 and sport_check_amount >= 75 and tim_hortons_amount >= 25:
            rule_points += 300
            sport_check_amount -= 75
            tim_hortons_amount -= 25

        elif rule == 4 and sport_check_amount >= 25 and tim_hortons_amount >= 10 and subway_amount >= 10:
            rule_points += 150
            sport_check_amount -= 25
            tim_hortons_amount -= 10
            subway_amount -= 10

        elif rule == 5 and sport_check_amount >= 25 and tim_hortons_amount >= 10:
            rule_points += 75
            sport_check_amount -= 25
            tim_hortons_amount -= 10

        elif rule == 3 and sport_check_amount >= 75:
            rule_points += 200
            sport_check_amount -= 75

        elif rule == 6 and sport_check_amount >= 20:
            rule_points += 75
            sport_check_amount -= 20

    # Rule 7: 1 point for every $1 spend for all other purchases (including leftover amount)
    rule_points += sport_check_amount + subway_amount + tim_hortons_amount + other_amount
    max_transaction_points = max(max_transaction_points, math.floor(rule_points))

    return max_transaction_points

def calculate_rewards(file_path, selected_rules):
    with open(file_path, 'r') as file:
        transactions = json.load(file)['transactions']

    total_rewards = 0
    transaction_rewards = {}

    for transaction_id, transaction_info in transactions.items():
        max_points = calculate_transaction_rewards(transaction_info, selected_rules)
        transaction_rewards[transaction_id] = max_points
        total_rewards += max_points

    return total_rewards, transaction_rewards

# Read input data from file
file_path = 'transactions.json'

# Define all possible rules (1 to 6)
all_rules = [1, 2, 3, 4, 5, 6]

# Find the combination of rules that yields the maximum reward points
max_reward = 0
best_combination = []

for r in range(1, len(all_rules) + 1):
    rule_combinations = list(combinations(all_rules, r))
    for rules_combination in rule_combinations:
        total_rewards, transaction_rewards = calculate_rewards(file_path, rules_combination)
        if total_rewards > max_reward:
            max_reward = total_rewards
            best_combination = rules_combination

# Print or use the calculated rewards and best combination as needed
print(f"Total Maximum Reward Points for the Month: {max_reward} points")
print("Maximum Reward Points Applied for Each Transaction:")
for transaction_id, reward in transaction_rewards.items():
    print(f"Transaction {transaction_id}: {reward} points")
