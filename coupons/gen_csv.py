import random

safe_alphabet = "AEFHJKQRUXY23456789"


def generate_id():
    return "".join(
        [safe_alphabet[random.randint(0, len(safe_alphabet) - 1)] for _ in range(5)]
    )


coupons = {}

coupon_list = [
    (10, "5 euros de remise", 5, "Campagne Facebook"),
    (10, "Une crêpe offerte pour une crêpe achetée", 0, "Iot.bzh"),
]

for quantity, description, discount_amount, origin in coupon_list:
    for i in range(quantity):
        while True:
            id = generate_id()
            if id not in coupons:
                break
        coupons[id] = (description, discount_amount, origin)

for id, (description, discount_amount, origin) in coupons.items():
    print(",".join([id, description, str(discount_amount), origin]))
