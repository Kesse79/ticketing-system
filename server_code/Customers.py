import anvil.tables as tables
from anvil.tables import app_tables
from .Utils import *
from datetime import datetime
from .utils import Validation

@authenticated_callable
def add_customer(cust_dict):
  cust_dict['created'] = datetime.now()
  return app_tables.customers.add_row(**cust_dict)

@authenticated_callable
def get_customers(filters={}):
  return app_tables.customers.search(tables.order_by('last_name', ascending=True), **filters)

@authenticated_callable
def update_customer(customer, customer_dict):
  if app_tables.customers.has_row(customer):
    cust_validation_errors = Validation.get_customer_errors(customer_dict)
    if cust_validation_errors:
      raise Exception('Something went wrong')
    else:
      customer.update(**customer_dict)  

@authenticated_callable
@tables.in_transaction
def delete_customers(customers):
  for c in customers:
    tickets = app_tables.tickets.search(customer=c)
    for t in tickets:
      messages = app_tables.messages.search(ticket=t)
      for m in messages:
        if app_tables.messages.has_row(m):
          m.delete()
      if app_tables.tickets.has_row(t):
        t.delete()
    if app_tables.customers.has_row(c):
      c.delete()