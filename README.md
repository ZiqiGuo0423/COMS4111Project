# restaurant management system

# team members:
Ziqi Guo: zg2410
Xinglu Zhou: xz3065

#db account: zg2410

#url: http://35.229.113.181:8111/

#In part1, we mentioned to implement following part:
For customers:
a.book appointment
b.Have access to menu
c.Being able to do special requests (add peers and input the accessibility requirements of peers)
d.view bills

We implemented all of them and also
a.customer can order dishes and view their order details (including dish name, quantity, total quantity, total amount need to pay)
b.customer can cancel their upcoming reservation (all related stuff will be deleted from related tables as well)
c.customer can reschedule their upcoming reservation (update the date)
d.customer can see all of history reservation details he/she made

For waiters:
In part1 we mentioned:
A. Being able to see number of customers, their assigned table, their special request and orders
b. Having access to menu and can update order (order status) to the system
C, being able to cancel orders (which we did not implement since it make no sense for the waiter to cancel the order)
d. View payment bills
e.see table details when making reservation

We implemented above parts plus:
a.all employees (including waiters and chef) can input new dishes into menu
b.all employees (including waiters and chef) can see dish-assignment-to-chef and also get the information about dishes without assignment, chef without any assignment, available chef and according to this information to assign dish to chef.
C.can search waiter information based on first name and/or email address and/or working years above #years. Besides, can choose whether to display all information(including sensitive info like age, salary, etc) or to just display normal information. Also, can choose whether to display in the order of employee id.
d.can view all waiters info (also can choose the way to display)
e.can insert new waiters
f.see waiter-assignment-to-reservation and also get the information about reservation without assignment(which will never happen since when customer make a new reservation, it will automatically choose one waiter to assigned to that reservation. Implemented in server.py), waiter without any assignment, available waiters.
g.view all reservation detail and based on order number to see order details (including dish name, quantity, total quantity, total amount need to pay).

For chef:
In part1 we mentioned:
a. Have access to menu
b. Query all orders.

We implement all we mentioned plus:
a.can search chef information based on first name and/or email address and/or Years of Cooking Experience over # years and/or cooking specialization. Besides, can choose whether to display all information(including sensitive info like age, salary, etc) or to just display normal information. Also, can choose whether to display in the order of employee id.
b.can view all chef info (also can choose the way to display)
c. can insert new waiters
d.view all reservation detail and based on order number to see order details (including dish name, quantity, total quantity, total amount need to pay).
e. Can update order status

# two interesting webpages:
A. view_reservation.html
In this page, a customer can search for his/her history reservation info based on his/her phone number. This include a join of reserve table, reservation table, customer table and orders table. And also to display peer info, it uses peer table. Search order details based on order number using orders table join contain table. 
In this page, a customer can also cancel his/her upcoming reservation based on their phone number used to make reservation. This include select operation into reservation table to retrieve reservation id and delete operation with customer table to delete customer info and cascade peer info in peer table and cascade reserve info in reserve table, delete operation with reservation table to delete reservation and cascade order info in orders table and contain info in contain table.
In this page, a customer can update his/her upcoming reservation date based on phone number input and new date input. This include update operation with reservation table.
It is interesting because it's the most complicated part in this design, which correlated many tables and use select, delete, update operations. Customer is discretionary to cancel or reschedule the reservation.

B. order.html
In this page, a customer can order dishes by input phone number used for reservation and the name of the dish. The menu will be displayed for user to scan (this include select * operation with item table). When customer clicks the add button, first, a select operation will be performed with reserve table to retrieve the order number related to this phone number. Second, an insert operation will be performed to insert new row into contain table. Third, a select operation is performed to retrieve the number of items info from orders table based on the phone number. Fourth, a update operation will be performed with orders table to add one to the number of items field to update the order info.
It is interesting because it is similar to a real-world scenario and includes select, insert, update operations.



