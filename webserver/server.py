#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
#from tkinter import INSERT
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, jsonify

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

import application.menu
import application.waiter
import application.chef
import application.reserve

import random

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://zg2410:6796@35.211.155.104/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ('uh oh, problem connecting to database')
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#


@app.route('/')
def welcome():
  return render_template("welcome.html")


@app.route('/customer')
def customer():
  return render_template('customer.html')


@app.route('/employee')
def employee():
  return render_template('employee.html')

@app.route('/menu/',methods=["POST", "GET"])
def menu():
  if "GET" == request.method:
    query = application.menu.fetch_menu()
    cursor = g.conn.execute(query)
    result = []
    for c in cursor:
      result.append(c)
    return render_template("menu.html", **dict(data = result))
  if "POST" == request.method:
    query = application.menu.add_dish(request.form)
    g.conn.execute(query)
    print('success')
    return redirect("/menu/")

@app.route('/menu_customer')
def menu_customer():
  query = application.menu.fetch_menu()
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(c)
  print(result)
  return render_template('menu-customer.html',**dict(data = result))

@app.route('/waiter/',methods=["POST", "GET"])
def waiter():
  if "GET" == request.method:
    return render_template("waiter.html")

  if "POST" == request.method:
    if 'view-all' in request.form and 'sensitive' not in request.form:
      query = application.waiter.fetch_waiter(request.form)
      cursor = g.conn.execute(query)
      print('success')
      result = []
      for c in cursor:
        result.append(c)
      return render_template("waiter.html", **dict(data = result))
    elif 'view-all' in request.form and 'sensitive' in request.form:
      query = application.waiter.fetch_all(request.form)
      cursor = g.conn.execute(query)
      print('success')
      result = []
      for c in cursor:
        result.append(c)
      return render_template("waiter.html", **dict(data = result))
    else:
      query = application.waiter.fetch(request.form)
      cursor = g.conn.execute(query)
      print('success')
      result = []
      for c in cursor:
        result.append(c)
      return render_template("waiter.html", **dict(data = result))


@app.route('/chef/',methods=["POST", "GET"])
def chef():
  if "GET" == request.method:
    return render_template("chef.html")
  if "POST" == request.method:
    if 'view-all' in request.form and 'sensitive' not in request.form:
      query = application.chef.fetch_chef(request.form)
      print(query)
      cursor = g.conn.execute(query)
      print('success')
      result = []
      for c in cursor:
        result.append(c)
      return render_template("chef.html", **dict(data = result))
    elif 'view-all' in request.form and 'sensitive' in request.form:
      query = application.chef.fetch_all(request.form)
      cursor = g.conn.execute(query)
      print('success')
      result = []
      for c in cursor:
        result.append(c)
      return render_template("chef.html", **dict(data = result))
    else:
      query = application.chef.fetch(request.form)
      cursor = g.conn.execute(query)
      print('success')
      result = []
      for c in cursor:
        result.append(c)
      return render_template("chef.html", **dict(data = result))


@app.route('/add_waiter/',methods=["POST", "GET"])
def add_waiter():
  if "GET" == request.method:
    return render_template("add_waiter.html")
  if "POST" == request.method:
    get = request.form
    id = random.randint(100,9999)
    query = '''
    INSERT INTO employee VALUES({employee_id},'{first}','{last}','{gender}',{age},'{email}',{phone},'{hire_date}',{working_years},'{salary}');
    '''

    query2 = '''
    INSERT INTO employee(employee_id,first_name,last_name,gender,email,phone_number,hire_date,working_years,salary)
    VALUES({employee_id},'{first}','{last}','{gender}','{email}',{phone},'{hire_date}',{working_years},'{salary}');
    '''

    if 'age' in request.form and len(request.form['age']) >0:
      age = int(request.form['age'])
      query = query.format(employee_id = id, first = get['first'], last = get['last'], gender = get['gender'], age = age, email = get['email'], phone = int(get['phone']), hire_date = get['hire'], working_years = float(get['work']), salary = get['salary'] )
      g.conn.execute(query)
    else:
      query2 = query2.format(employee_id = id, first = get['first'], last = get['last'], gender = get['gender'], email = get['email'], phone = int(get['phone']), hire_date = get['hire'], working_years = float(get['work']), salary = get['salary'] )
      g.conn.execute(query)

    query1 = '''
    INSERT INTO waiter VALUES({employee_id},'{shift}','{languages}');
    '''
    query1 = query1.format(employee_id = id, shift = get['shift'], languages = get['language'])
    g.conn.execute(query1)

    return redirect("/waiter/")

@app.route('/add_chef/',methods=["POST", "GET"])
def add_chef():
  if "GET" == request.method:
    return render_template("add_chef.html")
  if "POST" == request.method:
    get = request.form
    id = random.randint(100,9999)
    query = '''
    INSERT INTO employee VALUES({employee_id},'{first}','{last}','{gender}',{age},'{email}',{phone},'{hire_date}',{working_years},'{salary}');
    '''
    query2 = '''
    INSERT INTO employee(employee_id,first_name,last_name,gender,email,phone_number,hire_date,working_years,salary)
    VALUES({employee_id},'{first}','{last}','{gender}','{email}',{phone},'{hire_date}',{working_years},'{salary}');
    '''
    if 'age' in request.form and len(request.form['age']) >0:
      age = int(request.form['age'])
      query = query.format(employee_id = id, first = get['first'], last = get['last'], gender = get['gender'], age = age, email = get['email'], phone = int(get['phone']), hire_date = get['hire'], working_years = float(get['work']), salary = get['salary'] )
      g.conn.execute(query)
    else:
      query2 = query2.format(employee_id = id, first = get['first'], last = get['last'], gender = get['gender'], email = get['email'], phone = int(get['phone']), hire_date = get['hire'], working_years = float(get['work']), salary = get['salary'] )
      g.conn.execute(query2)
    print(query)

    query1 = '''
    INSERT INTO chef VALUES({employee_id},'{specialization}',{year},'{honor}');
    '''
    if 'honor' in request.form:
      honor = request.form['honor']
    else:
      honor = ''
    query1 = query1.format(employee_id = id, specialization = get['cook'], year = float(get['year']), honor = honor)
    g.conn.execute(query1)

    return redirect("/chef/")

@app.route('/cook',methods = ["POST","GET"])
def cook():
  if "GET" == request.method:
    query = '''
    SELECT e.employee_id,e.first_name,e.last_name,c.cooking_specialization,cook.name,item.type
    FROM employee e, chef c, cook, item
    WHERE e.employee_id = c.employee_id AND cook.employee_id = e.employee_id AND item.name = cook.name
    ORDER BY e.employee_id
    '''
    cursor = g.conn.execute(query)
    result = []
    for c in cursor:
      result.append(c)

    query1 = '''
    SELECT item.name,item.type
    FROM item
    WHERE item.name NOT IN (SELECT cook.name FROM cook)
    ORDER BY item.type;
    '''
    cursor = g.conn.execute(query1)
    result1 = []
    for c in cursor:
      result1.append(c)

    query2 = '''
    SELECT chef.employee_id,e.first_name,chef.cooking_specialization
    FROM chef,employee e
    WHERE e.employee_id = chef.employee_id
    ORDER BY chef.cooking_specialization;
    '''
    cursor = g.conn.execute(query2)
    result2 = []
    for c in cursor:
      result2.append(c)

    query3 = '''
    SELECT chef.employee_id,e.first_name,chef.cooking_specialization
    FROM chef,employee e
    WHERE e.employee_id = chef.employee_id AND e.employee_id NOT IN (SELECT cook.employee_id FROM cook)
    ORDER BY chef.cooking_specialization;
    '''
    cursor = g.conn.execute(query3)
    result3 = []
    for c in cursor:
      result3.append(c)

    return render_template('cook.html',**dict(data = result),**dict(data1=result1), **dict(data2=result2),**dict(data3=result3))
  if "POST" == request.method:
    get = dict(request.form)
    print(get)
    query = '''INSERT INTO cook VALUES({employee_id},'{name}');
    '''
    query = query.format(employee_id = int(get['ID']), name = get['name'])
    print(query)
    cursor = g.conn.execute(query)
    return redirect("/cook")


@app.route('/reservation',methods = ["POST","GET"])
def reservation():

  query = '''
  
  SELECT r.reservation_id, r.phone_number,c.last_name,c.first_name,re.number_of_people,re.date,r.table_number,r.order_number,o.order_status,r.employee_id
  FROM reserve r, reservation re, customer c, orders o
  WHERE r.reservation_id = re.reservation_id AND r.phone_number = c.phone_number AND o.order_number = r.order_number
  ORDER BY re.date;
  '''
  cursor = g.conn.execute(query)
  result = []
  for c in cursor:
    result.append(c)
  
  if 'POST' == request.method and 'id' in request.form and 'update' not in request.form:
    query = '''
    SELECT o.order_number,c.name, c.quantity, i.price, cook.employee_id
    FROM orders o, item i, contain c, cook
    WHERE o.order_number = '{order}' AND c.order_number = '{order}' AND c.name = i.name AND cook.name = c.name;
    '''
    query = query.format(order = request.form['id'])
    cursor = g.conn.execute(query)
    result1 = []
    for c in cursor:
      result1.append(c)

    query1 = '''
    SELECT o.number_of_items,  
    (select sum(i.price) from item i, contain c where c.name = i.name and c.order_number = '{order}')
    FROM orders o 
    WHERE o.order_number = '{order}';
    '''
    query1 = query1.format(order = request.form['id'])
    cursor = g.conn.execute(query1)
    result2 = []
    for c in cursor:
      result2.append(c)
    return render_template('reservation.html',**dict(data=result),**dict(data1 = result1),**dict(data2 = result2))
  if 'POST' == request.method and 'update' in request.form and 'id' in request.form and request.form['id']:
    print(request.form)
    query = '''
    UPDATE orders set order_status = '{status}' where order_number = '{order}';
    '''
    query = query.format(status = request.form['status'], order = request.form['id'])
    g.conn.execute(query)
    return redirect('/reservation')
  return render_template('reservation.html',**dict(data=result))


@app.route('/waiter_assign',methods = ["POST","GET"])
def waiter_assign():
  if "GET" == request.method:
    query = '''
    SELECT r.employee_id,e.first_name,e.last_name,r.reservation_id,re.date,r.order_number,r.table_number,r.phone_number
    FROM reserve r, reservation re, employee e
    WHERE r.reservation_id = re.reservation_id AND r.employee_id = e.employee_id
    ORDER BY re.date
    '''
    cursor = g.conn.execute(query)
    result = []
    for c in cursor:
      result.append(c)
    
    query1 = '''
    SELECT re.reservation_id,re.date,re.number_of_people
    FROM reservation re
    WHERE re.reservation_id NOT IN (SELECT r.reservation_id from reserve r)
    ORDER BY re.date
    '''
    cursor = g.conn.execute(query1)
    result1 = []
    for c in cursor:
      result1.append(c)

    query2 = '''
    SELECT e.employee_id,e.first_name,w.shift
    FROM employee e, waiter w
    WHERE e.employee_id NOT IN (SELECT r.employee_id FROM reserve r) AND e.employee_id = w.employee_id
    ORDER BY e.employee_id
    '''
    cursor = g.conn.execute(query2)
    result2 = []
    for c in cursor:
      result2.append(c)
    
    query3 = '''
    SELECT e.employee_id,e.first_name,w.shift
    FROM employee e, waiter w
    WHERE e.employee_id = w.employee_id
    ORDER BY e.employee_id
    '''
    cursor = g.conn.execute(query3)
    result3 = []
    for c in cursor:
      result3.append(c)
    print(result3)
    return render_template('waiter-assign.html',**dict(data = result),**dict(data1 = result1),**dict(data2 = result2),**dict(data3 = result3))
  # if  'POST' == request.method:
  #   get = request.form
  #   print(get)
  #   return redirect('/reserve')

@app.route('/reserve',methods = ["POST","GET"])
def reserve():
  if 'GET' == request.method:
    query = application.reserve.view_table()
    cursor = g.conn.execute(query)
    result = []
    for c in cursor:
      result.append(c)
    
    # query1 = application.menu.fetch_menu()
    # cursor = g.conn.execute(query1)
    # result1 = []
    # for c in cursor:
    #   result1.append(c)  
    return render_template('reserve.html',**dict(data = result))
  if 'POST' == request.method:
    if 'reserve' in request.form:
      print (request.form)
      query = application.reserve.book()
      rand = random.randint(10000,99999)
      rid = 'r' + str(rand)
      query = query.format(id = rid, number = int(request.form['number']), date = request.form['date'])
      print(query)
      g.conn.execute(query)

      #randomly assigned a waiter
      query = application.reserve.select_waiter()
      cursor = g.conn.execute(query)
      result = []
      for c in cursor:
        result.append(c)
      print(result)
      id = random.choice(result)
      print(id)

      #insert into order table
      order = 'O'+str(random.randint(100,999))
      query = application.reserve.order()
      query = query.format(order = order, rid = rid)
      print(query)
      g.conn.execute(query)

      # #insert into contain table
      # query = application.reserve.contain()
      # query = query.format(name = request.form['dish'], order = order )
      # print(query)
      # g.conn.execute(query)

      #insert into customer table
      query = application.reserve.add_cus(request.form)
      print(query)
      g.conn.execute(query)

      #insert into reserve table
      query = application.reserve.add_reserve()
      query = query.format(phone = int(request.form['phone']), table = request.form['table'], waiter = int(id[0]), order = order, id = rid)
      print(query)
      g.conn.execute(query)

      

    return redirect('/reserve')

@app.route('/view_reservation',methods = ["POST","GET"])
def view():
  if 'GET' == request.method:

    return render_template('view_reservation.html')

  if 'POST' == request.method:
    if 'search' in request.form:
      query = '''SELECT r.reservation_id, r.phone_number,c.last_name,c.first_name,re.number_of_people,re.date,r.table_number,r.order_number,o.order_status,r.employee_id
      FROM reserve r, reservation re, customer c, orders o
      WHERE r.reservation_id = re.reservation_id AND r.phone_number = c.phone_number AND o.order_number = r.order_number AND r.phone_number = {phone}
      ORDER BY re.date;'''
      query = query.format(phone = int(request.form['id']))
      print(query)
      cursor = g.conn.execute(query)
      result = []
      for c in cursor:
        result.append(c)
      query2 = '''
      SELECT p.name, p.phone_number_peer,p.assistance_or_not
      FROM peer p
      WHERE p.phone_number = {phone};
      '''
      query2 = query2.format(phone = int(request.form['id']))
      print(query2)
      cursor = g.conn.execute(query2)
      result1 = []
      for c in cursor:
        result1.append(c)
      return render_template('view_reservation.html',**dict(data = result),**dict(data1 = result1))
    
    if 'order' in request.form:
      query = '''
      SELECT o.order_number,c.name, c.quantity, i.price, cook.employee_id
      FROM orders o, item i, contain c, cook
      WHERE o.order_number = '{order}' AND c.order_number = '{order}' AND c.name = i.name AND cook.name = c.name;
      '''
      query = query.format(order = request.form['id'])
      cursor = g.conn.execute(query)
      result2 = []
      for c in cursor:
        result2.append(c)

      query1 = '''
      SELECT o.number_of_items,  
      (select sum(i.price) from item i, contain c where c.name = i.name and c.order_number = '{order}')
      FROM orders o 
      WHERE o.order_number = '{order}';
      '''
      query1 = query1.format(order = request.form['id'])
      cursor = g.conn.execute(query1)
      result3 = []
      for c in cursor:
        result3.append(c)
      return render_template('view_reservation.html',**dict(data2 = result2),**dict(data3 = result3))
      


@app.route('/add_com',methods = ["POST","GET"])
def add():
  if 'GET' == request.method:
    return render_template('add.html')
  if 'POST' == request.method:
    query = '''
    INSERT INTO peer VALUES('{name}','{phone}','{assis}','{p}')
    '''

    query2 = '''
    INSERT INTO peer(name,assistance_or_not,phone_number) VALUES('{name}','{assis}','{p}')
    '''
    print(len(request.form['phone']))
    if len(request.form['phone']) > 0:
      phone = int(request.form['phone'])
      query = query.format(name = request.form['name'], phone = phone, assis = request.form['assistance'], p = int(request.form['p']))
      g.conn.execute(query)
    else:
      query2 = query2.format(name = request.form['name'], assis = request.form['assistance'], p = int(request.form['p']))
      g.conn.execute(query2)
    return redirect('/add_com')



@app.route('/order',methods = ["POST","GET"])
def order():
  if 'GET' == request.method:
    query = application.menu.fetch_menu()
    cursor = g.conn.execute(query)
    result = []
    for c in cursor:
      result.append(c)
    print(result)
    return render_template('order.html',**dict(data = result))
  if 'POST' == request.method:
    # retrieve the order number related to that phone
    query = '''
    SELECT r.order_number FROM reserve r
    WHERE r.phone_number = {phone};
    '''
    query = query.format(phone = int(request.form['p']))
    print(query)
    cursor = g.conn.execute(query)
    result1 = []
    for c in cursor:
      result1.append(c)
    print(result1)
    
    result = result1[0][0]
    print(result)

    query1 = '''
    INSERT INTO contain VALUES(1,'{name}','{order}');
    '''
    query1 = query1.format(name = request.form['name'], order = result)
    cursor = g.conn.execute(query1)

    #update the order table
    query2 = '''
    SELECT number_of_items FROM orders WHERE order_number = '{order}';
    '''
    query2 = query2.format(order = result)
    cursor = g.conn.execute(query2)
    result1 = []
    for c in cursor:
      result1.append(c)
    print(result1)
    
    result2 = result1[0][0]
    result2 = int(result2) + 1
    print(result2)
    
    query3 = '''
    UPDATE orders SET number_of_items = {number} WHERE order_number = '{order}';
    '''
    query3 = query3.format(number = result2, order = result)
    g.conn.execute(query3)
    
    return redirect('/order')


# @app.route('/')
# def index():
#   """
#   request is a special object that Flask provides to access web request information:

#   request.method:   "GET" or "POST"
#   request.form:     if the browser submitted a form, this contains the data in the form
#   request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

#   See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
#   """

#   # DEBUG: this is debugging code to see what request looks like
#   print (request.args)


#   #
#   # example of a database query
#   #
#   cursor = g.conn.execute("SELECT name FROM test")
#   names = []
#   for result in cursor:
#     names.append(result['name'])  # can also be accessed using result[0]
#   cursor.close()

#   #
#   # Flask uses Jinja templates, which is an extension to HTML where you can
#   # pass data to a template and dynamically generate HTML based on the data
#   # (you can think of it as simple PHP)
#   # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
#   #
#   # You can see an example template in templates/index.html
#   #
#   # context are the variables that are passed to the template.
#   # for example, "data" key in the context variable defined below will be 
#   # accessible as a variable in index.html:
#   #
#   #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
#   #     <div>{{data}}</div>
#   #     
#   #     # creates a <div> tag for each element in data
#   #     # will print: 
#   #     #
#   #     #   <div>grace hopper</div>
#   #     #   <div>alan turing</div>
#   #     #   <div>ada lovelace</div>
#   #     #
#   #     {% for n in data %}
#   #     <div>{{n}}</div>
#   #     {% endfor %}
#   #
#   context = dict(data = names)


#   #
#   # render_template looks in the templates/ folder for files.
#   # for example, the below file reads template/index.html
#   #
#   return render_template("index.html", **context)

# #
# # This is an example of a different path.  You can see it at:
# # 
# #     localhost:8111/another
# #
# # Notice that the function name is another() rather than index()
# # The functions for each app.route need to have different names
# #
# @app.route('/another')
# def another():
#   return render_template("another.html")


# # Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#   name = request.form['name']
#   g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
#   return redirect('/')



if __name__ == "__main__":
  app.run(debug = True)
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
