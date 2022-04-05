import logging
from sqlalchemy import text

FULL_FETCH = """
SELECT
	e.employee_id,
	e.first_name,
	e.last_name,
	e.email,
	e.phone_number,
    e.working_years,
    w.languages,
	e.gender,
	e.age,
	e.hire_date,
	e.salary_per_week,
    w.shift
FROM
	employee e,
	waiter w
WHERE
	e.employee_id = w.employee_id
"""

STD_FETCH = """
SELECT
	e.employee_id,
	e.first_name,
	e.last_name,
	e.email,
	e.phone_number,
    e.working_years,
    w.languages
FROM
	employee e,
	waiter w
WHERE
	e.employee_id = w.employee_id
"""

queryMap = {
    'first_name': " AND e.first_name LIKE '%%{}%%'",
    'email': " AND e.email LIKE '%%{}%%'",
    'year': "AND e.working_years >= {}",
    'sort': " ORDER BY e.employee_id"
}

def fetch(args):
    query = FULL_FETCH if 'sensitive' in args else STD_FETCH
    print(str(args))
    if 'name' in args and args['name']:
        query += queryMap['first_name'].format(args['name']) 
    if 'email' in args and args['email']:
        query += queryMap['email'].format(args['email']) 
    if 'year' in args and args['year']:
        year = float(args['year'])
        query += queryMap['year'].format(year)
    query += queryMap['sort'] if 'sort' in args else ""
    print(str(query))
    return query

def fetch_waiter(args):
    query = '''
        SELECT
            e.employee_id,
            e.first_name,
            e.last_name,
            e.email,
            e.phone_number,
            e.working_years,
            w.languages
        FROM
            employee e,
            waiter w
        WHERE
            e.employee_id = w.employee_id
    '''
    query += queryMap['sort'] if 'sort' in args else ""
    return(query)

def fetch_all(args):
    query = '''
        SELECT
            e.employee_id,
            e.first_name,
            e.last_name,
            e.email,
            e.phone_number,
            e.working_years,
            w.languages,
            e.gender,
            e.age,
            e.hire_date,
            e.salary_per_week,
            w.shift
        FROM
            employee e,
            waiter w
        WHERE
            e.employee_id = w.employee_id
    '''
    query += queryMap['sort'] if 'sort' in args else ""
    return(query)