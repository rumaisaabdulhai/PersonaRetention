"""
This script generates buyer strategies with random budgets, preferred brands, and preferred features.
"""

from convo_prompts import BUYER_STRATEGIES, BUDGET, PREFERRED_BRAND, PREFERRED_FEATURES
import random
import json

NUM_STRATEGIES = 3
NUM_FEATURES = 3

def main():
    buyer_strategies = []
    for _ in range(NUM_STRATEGIES):
        buyer_strategy = random.choice(BUYER_STRATEGIES)
        budget = random.choice(BUDGET)
        preferred_brand = random.choice(PREFERRED_BRAND)
        preferred_features = random.sample(PREFERRED_FEATURES, NUM_FEATURES)
        buyer_background = f"Buyer background: {buyer_strategy}\nBudget: {budget}\nPreferred Brand: {preferred_brand}\nPreferred Features: {', '.join(preferred_features)}"
        buyer_strategies.append(buyer_background)

    # save to a json
    with open("buyer_strategies.json", "w") as f:
        json.dump(buyer_strategies, f, indent=4)


if __name__ == "__main__":
    main()