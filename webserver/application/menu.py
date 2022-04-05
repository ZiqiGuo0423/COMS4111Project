import logging

FETCH_MENU = """
    select * from item;
"""

INSERT = """INSERT INTO item VALUES('{name}', {price}, '{description}', '{type}');"""


def fetch_menu():
    query = FETCH_MENU
    return query

def add_dish(args):
    add_dish = INSERT
    add_dish = add_dish.format(name = args['name'], price = args['price'], description = args['description'], type = args['type'])
    print(add_dish)
    return add_dish