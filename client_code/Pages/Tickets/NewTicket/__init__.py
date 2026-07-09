from ._anvil_designer import NewTicketTemplate
from anvil import *
import anvil.server
from ....utils import Validation, Data, emitter
from ....utils.Navigation import navigate

class NewTicket(NewTicketTemplate):
  def __init__(self, initial_customer = None, **properties):
    # setting up databindings for dropdowns and text forms
    self.agents = [(x['email'], x) for x in anvil.server.call('get_users')]
    self.categories = Data.CATEGORIES
    self.priorities = Data.PRIORITIES
    self.new_customer = {}
    self.selected_customer = {}
    self.details = None
    self.new = False
    self.customers = anvil.server.call('get_customers')
    self.repeating_panel_results.items = []
    
    self._props = properties
    self.init_components(**properties)
    
    curr_num = Data.CURRENT_TICKET_NO
    self.new_ticket_number.text = f"# {curr_num}"
    emitter.form_subscribe(self, 'assign-existing-customer', self.set_assigned_customer)
    
    # update the form if there is a preselected customer
    if initial_customer:
      self.text_box_search.text = f"{initial_customer['first_name']} {initial_customer['last_name']}"
      self.text_box_search_focus()
      comps = self.repeating_panel_results.get_components()
      for component in comps:
        if initial_customer == component.item:
          component.set_selected(True)
          self.selected_customer = initial_customer
    self.set_customer_label()

  def text_box_search_focus(self, **event_args):
    self.assign_new_customer_card.visible = False
    self.repeating_panel_results.visible = True
    self.new = False
    self.populate_results(self.text_box_search.text)
    self.set_customer_label()

  def text_box_search_change(self, **event_args):
    self.populate_results(self.text_box_search.text)
    
  # Populate the suggestions panel
  def populate_results(self, text):
    if text == '':
      self.repeating_panel_results.items = []
    else:
      # Populate the results list
      self.repeating_panel_results.items = [
        c for c in self.customers
        if text.lower() in c['first_name'].lower()
        or text.lower() in c['last_name'].lower()
        or text.lower() in f"{c['first_name'].lower()} {c['last_name'].lower()}"
      ]

  def add_ticket(self):
    ticket = self.item
    details = self.details
    
    if self.new:
      customer = self.new_customer
      cust_validation_errors = Validation.get_customer_errors(customer)
    else:
      customer = self.selected_customer
      cust_validation_errors = None
      if customer == {}:
        alert("Please choose a customer")
        return
    tick_validation_errors = Validation.get_ticket_errors(ticket)
    
    if not cust_validation_errors and not tick_validation_errors:
      ticket = anvil.server.call('add_ticket', ticket, details, customer)
      Notification('Ticket Added').show()
      navigate(page="ticket", ticket = ticket)
  
    elif cust_validation_errors and tick_validation_errors:
      alert("The following fields are missing for your customer: \n{}.\n\nThe following field are missing for your ticket: \n{}".format(
        ' \n'.join(word.capitalize() for word in cust_validation_errors),
        ' \n'.join(word.capitalize() for word in tick_validation_errors)
      ))
    elif tick_validation_errors and not cust_validation_errors:
      alert("The following ticket fields are missing: \n{}".format(' \n'.join(word.capitalize() for word in tick_validation_errors)))
    elif cust_validation_errors and not tick_validation_errors:
      alert("The following customer fields are missing: \n{}".format(' \n'.join(word.capitalize() for word in cust_validation_errors)))

  def set_assigned_customer(self, item, **event_args):
    self.selected_customer = item
    self.set_customer_label()

  def text_box_search_pressed_enter(self, **event_args):
    results = self.repeating_panel_results.get_components()
    if results:
      results[0].customer_link_click()

  def add_new_cust_link_click(self, **event_args):
    self.new = True
    self.assign_new_customer_card.visible = True
    self.repeating_panel_results.visible = False
    self.repeating_panel_results.items = []
    self.text_box_search.text = ""
    self.selected_customer = {}
    self.set_customer_label()

  def clear_link_click(self, **event_args):
    navigate(page='new_ticket')
    
  def send_button_click(self, **event_args):
    self.add_ticket()

  def set_customer_label(self, **event_args):
    if self.new:
      if self.new_customer.get('last_name', "") == self.new_customer.get('first_name', "") == "":
        self.no_customer.visible = True
        self.selected_customer_label.visible = False
      else:
        self.no_customer.visible = False
        self.selected_customer_label.visible = True
        self.selected_customer_label.text = f"{self.new_customer.get('first_name', '')} {self.new_customer.get('last_name', '')}"
    else:
      if self.selected_customer == {}:
        self.no_customer.visible = True
        self.selected_customer_label.visible = False
      else:
        self.no_customer.visible = False
        self.selected_customer_label.visible = True
        self.selected_customer_label.text = f"{self.selected_customer['first_name']} {self.selected_customer['last_name']}"
