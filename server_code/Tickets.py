import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Utils import *
from .utils import Validation
from . import Customers
from datetime import datetime, timedelta, date
from .utils import Validation
from . import Data

@authenticated_callable
@tables.in_transaction
def add_ticket(ticket_dict, text, customer):
  # If this customer already exists in the database, don't re-check for errors
  if app_tables.customers.has_row(customer):
    cust_validation_errors = None
  else:
    cust_validation_errors = Validation.get_customer_errors(customer)
  tick_validation_errors = Validation.get_ticket_errors(ticket_dict)
  if tick_validation_errors or cust_validation_errors:
    raise Exception('Something went wrong')
  else:
    if not app_tables.customers.has_row(customer):
      customer = Customers.add_customer(customer)
    current_ticket_row = app_tables.currentticketno.get()
    ticket = app_tables.tickets.add_row(
        customer=customer, 
        status=app_tables.status.get(name="Open"), 
        date=datetime.now(),
        number=current_ticket_row['number'],
        **ticket_dict
      )
    # Increment current ticket number
    current_ticket_row['number'] += 1
    app_tables.messages.add_row(
        date=datetime.now(),
        ticket=ticket,
        type=app_tables.types.get(name="INTERNAL_NOTE"),
        details=text,
        agent=anvil.users.get_user()
    )
    return ticket

@authenticated_callable
def get_customer_tickets(filters={}):
  tickets = app_tables.tickets.search(tables.order_by('date', ascending=False), **filters)
  tick_and_messages = []
  for t in tickets:
    messages = app_tables.messages.search(tables.order_by("date", ascending=False), ticket=t)
    first_message = messages[len(messages) - 1]
    data = {'ticket':t, 'message':first_message}
    tick_and_messages.append(data)
  return tick_and_messages

@authenticated_callable
def get_messages(ticket):
  return app_tables.messages.search(tables.order_by("date", ascending=False), ticket=ticket)

@authenticated_callable
def get_ticket(number):
  return app_tables.tickets.search(tables.order_by("date", ascending=False), number=number)
  
@authenticated_callable
def get_tickets(sort, filters={}, date_filter={}):
  if filters.get('owner') and filters['owner'] == Data.NO_AGENTS_SELECTED:
    filters['owner'] = None
  ascending = sort != 'date'
  closed_status = Data.CLOSED
  # Condition on date filters here then pass to filters if acceptable
  start = date_filter.get('start') or datetime(1900, 1, 1, 0, 0, 0)
  end = date_filter.get('end') or datetime.now()
  end += timedelta(days=1)
  filters['date'] = q.between(start, end)
  if filters.get('status') == Data.CLOSED:
    closed_start = date_filter.get('closed_start') or datetime(1900, 1, 1)
    closed_end = date_filter.get('closed_end') or datetime.now()
    closed_end += timedelta(days=1)
    filters['closed'] = q.between(closed_start, closed_end)
  return app_tables.tickets.search(tables.order_by(sort, ascending=ascending), **filters)
  

@anvil.email.handle_message()
def message_handler(msg):
  msg.reply(text="Thank you for your message. We aim to get back to you in 3 working days.")
  
  cust_row = app_tables.customers.get(email=msg.envelope.from_address)
  if not cust_row:
    names = msg.addressees.from_address.name.split(" ", 1)
    cust_row = app_tables.customers.add_row(
      email=msg.envelope.from_address,
      first_name=names[0],
      last_name=names[1],
      company="",
      title="",
      created=datetime.now()
    )
  current_ticket_row = app_tables.currentticketno.get()
  ticket_row = app_tables.tickets.add_row(
                title=msg.subject,
                category=Data.NEW_CATEGORY,
                priority=Data.NEW_PRIORITY,
                status=Data.OPEN,
                date=datetime.now(),
                customer=cust_row,
                due=date.today() + timedelta(days=3),
                owner=app_tables.users.get(email="demo@anvil.works"),
                number=current_ticket_row['number']
                )
  current_ticket_row['number'] += 1
  msg_row = app_tables.messages.add_row(
              details=msg.text,
              date=datetime.now(),
              ticket=ticket_row,
              type=Data.INCOMING
  )

@authenticated_callable
def add_message(message_dict, ticket):
  message_validation_errors = Validation.get_message_errors(message_dict)
  if message_validation_errors:
    raise Exception("Something went wrong")
  else:
    app_tables.messages.add_row(
        date=datetime.now(),
        ticket=ticket,
        agent=anvil.users.get_user(),
        **message_dict
    )
  if message_dict['type'] == Data.OUTGOING:
    anvil.email.send(
      to=ticket['customer']['email'],
      from_name="Anvil Support",
      subject=f"Re: {ticket['title']}",
      text=message_dict['details']
    )
  
@authenticated_callable
def update_ticket(ticket, ticket_dict):
  tick_validation_errors = Validation.get_ticket_settings_errors(ticket_dict)
  if tick_validation_errors:
    raise Exception("Something went wrong")
  else:
    if app_tables.tickets.has_row(ticket):
      # If ticket is newly closed
      if ticket_dict['status'] == Data.CLOSED and not ticket['status'] == Data.CLOSED:
        ticket_dict['closed'] = datetime.now()
      ticket.update(**ticket_dict)  
    
@authenticated_callable
def update_ticket_priority(ticket, priority):
  if app_tables.tickets.has_row(ticket):
    ticket.update(priority=priority)  
    
@authenticated_callable
@tables.in_transaction
def close_tickets(tickets):
  for t in tickets:
    t_dict = {
      'title': t['title'],
      'category': t['category'],
      'priority': t['priority'],
      'owner': t['owner'],
      'due': t['due'],
    }
    t_dict['status'] = Data.CLOSED
    update_ticket(t, t_dict)

@authenticated_callable
def get_dashboard_data(date_filters={}, dash_filters={}):
  resolved_tickets, new_tickets = get_ticket_data(date_filters, dash_filters)
  headline_stats = get_headline_dash_stats()
  progress_dash_stats = get_progess_data(resolved_tickets, new_tickets, date_filters, dash_filters)
  resolution_data = get_resolution_data(resolved_tickets, new_tickets, date_filters, dash_filters)
  return headline_stats, progress_dash_stats, resolution_data

def get_ticket_data(date_filters, dash_filters):
  resolved_tickets = app_tables.tickets.search(
    closed=q.between(date_filters['start'], date_filters['end'], max_inclusive=True),
    status=Data.CLOSED,
    **dash_filters
  )
  new_tickets = app_tables.tickets.search(
    date=q.between(date_filters['start'], date_filters['end'], max_inclusive=True), 
    **dash_filters
  )
  return resolved_tickets, new_tickets

def get_headline_dash_stats():
  today = datetime.now()
  seven_days_ago = date.today() - timedelta(days=6)
  last_start = seven_days_ago - timedelta(days=8)
  
  tickets_opened_in_range = app_tables.tickets.search(date=q.between(seven_days_ago, today))
  tickets_opened_in_previous = app_tables.tickets.search(date=q.between(last_start, seven_days_ago))
  new_ticket = len(tickets_opened_in_range)
  previous_new_ticket = len(tickets_opened_in_previous)
  
  tickets_closed_in_range = app_tables.tickets.search(closed=q.between(seven_days_ago, today), status=Data.CLOSED) #incase it was reopened
  tickets_closed_in_previous = app_tables.tickets.search(closed=q.between(last_start, seven_days_ago), status=Data.CLOSED) 
  closed_tickets = len(tickets_closed_in_range)
  previous_closed_tickets = len(tickets_closed_in_previous)
  
  all_open_tickets = app_tables.tickets.search(status=Data.OPEN)
  all_open = len(all_open_tickets)
  
  return {
    'new_tickets': {'number': new_ticket, 'delta': new_ticket - previous_new_ticket},
    'closed_tickets': {'number': closed_tickets, 'delta': closed_tickets - previous_closed_tickets},
    'all_open': {'number': all_open, 'delta': None}
  }

@authenticated_callable
def get_progess_data(resolved_tickets, new_tickets, date_filters, dash_filters):
  # Get the type of an outgoing email from Support
  # Tickets closed on first reply are those that are both closed AND have only one reply to the customer from internal
  closed_on_first = [t for t in resolved_tickets if len(app_tables.messages.search(ticket=t, type=Data.OUTGOING)) == 1]
  # This returns ALL new customers over the period. Need to then apply dashboard filters to only return new_customers with tickets that match the filters

  returning_customers = list(set())
  new_customers = list(set())
  for ticket in new_tickets:
    open_date = ticket['date']
    customer = ticket['customer']
    customer_tickets = get_tickets(sort = 'date', filters= {'customer': customer})
    if len([t for t in customer_tickets if t['date'] < open_date]): #not the first ticket. This is a returning customer. If this customer is already in the new customer list do nothing. else add him to the returning customer. in case they made multiple tickets in this span of time, however their first was still in this range
      if customer not in new_customers:
        returning_customers.append(customer)
    else:
      new_customers.append(customer)
      
  return {
    'resolved': {
      'total_resolved': len(resolved_tickets), 'closed_on_first':len(closed_on_first)
     }, 
    'customers':{
      'new_customers':len(new_customers), 'returning_customers':len(returning_customers)
     }
  }

@authenticated_callable
def get_resolution_data(resolved_tickets, new_tickets, date_filters, dash_filters):
  dates = []
  res = []
  unres = []
  for day in (date_filters['start'] + timedelta(days=n) for n in range(date_filters['time_period'])):
    dates.append(day.strftime('%A, %d'))
    r = len([x for x in resolved_tickets if x['closed'].date() == day])
    res.append(r)
    u = len([x for x in new_tickets if not x['closed'] and x['date'].date() == day])
    unres.append(u)
  data = {'resolved':res, 'unresolved':unres}
  return {'dates':dates, 'data':data}
