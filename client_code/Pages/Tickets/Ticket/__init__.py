from ._anvil_designer import TicketTemplate
from anvil import *
import anvil.server
from ....utils import Data, Validation, emitter
from datetime import date

class Ticket(TicketTemplate):
  def __init__(self, ticket, **properties):
    self.ticket = ticket or {}
    self.customer_tickets = anvil.server.call('get_customer_tickets', filters={'customer': self.ticket['customer']})

    self.messages = None
    self.message = {}
    self.ticket_copy = {key: self.ticket[key] for key in ['title', 'category', 'status', 'priority', 'owner', 'due']}
    
    # setting up databindings for dropdowns and text forms
    self.categories = Data.CATEGORIES
    self.priorities = Data.PRIORITIES
    self.status = Data.STATUS
    users = anvil.server.call('get_users')
    self.agents = [(x['email'], x) for x in users]

    self.ticket_locked = True
    self.init_components(**properties)

    self.set_status_label()
    self.populate_messages()
    self.populate_to_dropdown()
    
  def populate_messages(self):
    self.messages = anvil.server.call('get_messages', self.ticket)
    self.messages_repeating_panel.items = self.messages
      
  def populate_to_dropdown(self):
    INTERNAL = Data.INTERNAL
    OUTGOING = Data.OUTGOING
    # Populate values of the to_dropdown
    self.to_dropdown.items = [
      (f"{self.ticket['customer']['first_name']} {self.ticket['customer']['last_name']}", OUTGOING), 
      ('Internal Note', INTERNAL)
    ]
    self.message['type'] = OUTGOING

  def lock_link_click(self, **event_args):
    self.ticket_locked = not self.ticket_locked
    self.refresh_data_bindings()
    self.lock_link.icon = 'fa:lock' if self.ticket_locked else 'fa:unlock'
  
  def update_ticket(self, **event_args):
    anvil.server.call('update_ticket', self.ticket, self.ticket_copy)
    self.customer_tickets = anvil.server.call('get_customer_tickets', filters={'customer': self.ticket['customer']}) 
    self.refresh_data_bindings()
    self.set_status_label()
      
  def update_ticket_priority(self, **event_args):
    anvil.server.call('update_ticket_priority', self.ticket, self.ticket_copy['priority'])

  def update_title(self, **event_args):
    if self.ticket_copy['title'] == "":
      self.ticket_copy['title'] = self.ticket['title']
      Notification('Ticket title cannot be blank').show()
    elif self.ticket_copy['title'] == self.ticket['title']:
      return
    else:
      self.update_ticket()

  def add_message_button_click(self, **event_args):
    self.ticket_reply.visible = True
    self.ticket_reply.scroll_into_view()

  def send_message_button_click(self, **event_args):
    message_validation_errors = Validation.get_message_errors(self.message)
    if not message_validation_errors:
      self.message_detail_area.text = ""
      self.ticket_reply.visible = False
      anvil.server.call('add_message', self.message, self.ticket)
      Notification('Reply added').show()
      self.populate_messages()
    else:
      alert("\nThe following field are missing for your reply: \n{}".format(
        ' \n'.join(message_validation_errors)
      ))

  def cancel_message_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.ticket_reply.visible = False

  def set_status_label(self):
    if self.ticket['status'] == Data.CLOSED:
      self.overdue_label.visible = True
      self.overdue_label.text = 'CLOSED'
      self.overdue_label.foreground = 'theme:Secondary 600'
    elif self.ticket['due'] < date.today():
      self.overdue_label.visible = True
      self.overdue_label.text = 'OVERDUE'
      self.overdue_label.foreground = 'theme:Error 500'
    else:
      self.overdue_label.visible = False

