import random



def view_table():
    query = '''
    SELECT * FROM table_sit 
    ORDER BY table_number
    '''
    return (query)

def book():
    query = '''
    INSERT INTO reservation VALUES ('{id}',{number},'{date}')
    '''
    return (query)


def select_waiter():
    query = '''
    SELECT employee_id FROM waiter;
    '''
    return(query)

def add_reserve():
    query = '''
    INSERT INTO reserve VALUES({phone},'{table}',{waiter},'{order}','{id}')
    '''
    return (query)
    

def add_cus(args):
    query = '''
    INSERT INTO customer VALUES ({phone},'{first}','{last}')
    '''
    query = query.format(phone = int(args['phone']), first = args['first'], last = args['last'])
    return (query)

def order():
    query = '''
    INSERT INTO orders VALUES ('{order}', 0, 'unfinish','{rid}')
    '''
    return (query)
