# theater.py
#
# The owner of a monopolistic movie theater in a small town has
# complete freedom in setting ticket prices.  The more he charges, the
# fewer people can afford tickets.  The less he charges, the more it
# costs to run a show because attendance goes up.  In a recent
# experiment the owner determined a relationship between the price of
# a ticket and average attendance.
#
# At a price of $5.00/ticket, 120 people attend a performance.  For
# each 10-cent change in the ticket price, the average attendance
# changes by 15 people.  That is, if the owner charges $5.10, some 105
# people attend on the average; if the price goes down to $4.90,
# average attendance increases to 135.
#
# Unfortunately, the increased attendance also comes at an increased
# cost.  Every performance comes at a fixed cost of $180 to the owner
# plus a variable cost of $0.04 per attendee.
#
# The owner would like to know the exact relationship between profit
# and ticket price in order to maximize the profit.
#
# Write a program to figure out the best ticket price (to the nearest
# 10 cents) that maximizes profit.
#
# Credit: This problem comes from "How to Design Programs", 2nd Ed.

# "wishful thinking" coding. Focus on the actual problem being solved
#  a function (or object) that directly address that


from decimal import Decimal
Number = Decimal
LOW_PRICE = Number('1.0')

# Problem parameters (abstraction)
LOW_PRICE  = 1.0
HIGH_PRICE = 10.0
INCREMENT  = 0.1
"""
FIXED_COST
VARIABLE_COST
BASE_PRICE
"""


# start the problem 
def best_ticket_price(low_price, high_price, increment):
    #... 
    #return max()
    price = low_price
    best_price = price
    best_profit = compute_profit(price)
    while price <= high_price:
        price += increment
        profit = compute_profit(price)
        if profit > best_profit:
            best_profit = profit
            best_price = price

    return best_price

# more general function that allows any profit function to be supplied 
# # could be reuse in other applications 
def best_price(low_price, high_price, increment, profit_func):
    #... 
    #return max()
    price = low_price
    best_price = price
    best_profit = profit_func(price)
    while price <= high_price:
        price += increment
        profit = profit_func(price)
        if profit > best_profit:
            best_profit = profit
            best_price = price

    return best_price


def compute_profit(price):
    attendees = expected_attendees(price)
    revenue = expected_revenue(attendees, price)
    #revenue = attendees * price
    #revenue = expected_revenue()
    cost = expected_cost(attendees)
    return revenue - cost

def expected_revenue(attendees, price):
    return attendees * price

def expected_cost(attendees):
    return 180 + 0.04 * attendees

def expected_attendees(price):
    return 120 - (price - 5.0) * (15/0.10)

# **search** for the best price over some range
best_price = best_price(1.0, 10.0, 0.10, compute_profit)
print("Best price:", best_price)



