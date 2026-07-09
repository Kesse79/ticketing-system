from anvil import open_form
from . import emitter

nav_dic = {
  'login': {
    'active': None,
    'form_name': 'Pages.Login' } ,
  'dashboard': {
    'active': 'dashboard',
    'form_name': 'Pages.Dashboard' } ,
  'customers': {
    'active': 'customers',
    'form_name': 'Pages.Customers' } ,
  'tickets': {
    'active': 'tickets',
    'form_name': 'Pages.Tickets.Tickets' } ,
  'new_ticket': {
    'active': 'tickets',
    'form_name': 'Pages.Tickets.NewTicket' } ,
  'ticket': {
    'active': 'tickets',
    'form_name': 'Pages.Tickets.Ticket' } ,
}

def navigate(page, **page_props):    
  open_form(nav_dic[page]['form_name'], **page_props)
  if nav_dic[page]['active']: 
    emitter.emit('set_active_nav_style', nav_name = nav_dic[page]['active'])
