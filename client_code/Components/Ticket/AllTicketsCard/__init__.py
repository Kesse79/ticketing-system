from ._anvil_designer import AllTicketsCardTemplate
from anvil import *
import anvil.server
from ....utils import Data, emitter
from ....utils.Navigation import navigate
from datetime import date

class AllTicketsCard(AllTicketsCardTemplate):
  def __init__(self, **properties):
    self.priorities = Data.PRIORITIES
    self.init_components(**properties)

    if self.item['priority'] == Data.URGENT:
      if self.item['status'] == Data.OPEN:
        self.urgent_dot.visible = True

    if self.item['status'] == Data.CLOSED:
      self.ticket_status_indicator.visible = True
      self.ticket_status_indicator.status = 'CLOSED'
    elif self.item['due'] < date.today():
      self.ticket_status_indicator.visible = True

  def priority_dropdown_change(self, **event_args):
    anvil.server.call('update_ticket_priority', self.item, self.priority_dropdown.selected_value)
    Notification("Ticket priority updated").show()

  def select_ticket_change(self, **event_args):
    if self.select_ticket.checked:
      self.role = ['all-tickets-card', 'all-tickets-card-selected']
      self.ticket_status_indicator.dom_nodes['indicator'].style.left = '-15px'
    else:
      emitter.emit('unselect-select-all-tickets-box')
      self.role = ['all-tickets-card']
      self.ticket_status_indicator.dom_nodes['indicator'].style.left = '-5px'
      
    emitter.emit('select-ticket', ticket = self.item, selected = self.select_ticket.checked)

  def ticket_title_link_click(self, **event_args):
    navigate(page="ticket", ticket = self.item)
    
  def cust_name_link_click(self, **event_args):
    print(self.item['customer']['first_name'])
    navigate(page="customers", open_customer=self.item['customer'])