from ._anvil_designer import TicketsTemplate
from anvil import *
import anvil.server
from ....utils import Data, emitter

class Tickets(TicketsTemplate):
  def __init__(self, search_filters=None, initial_date_filters=None, **properties):
    self.filters = search_filters or {'status': Data.OPEN}
    self.date_filter = initial_date_filters or {}

    # setting up databindings for forms
    self.categories = Data.CATEGORIES
    self.priorities = Data.PRIORITIES
    self.status = Data.STATUS
    self.sort = "date"
    self.customers = [(f"{x['first_name']} {x['last_name']}", x) for x in anvil.server.call('get_customers')]
    self.owners = [(x['email'], x) for x in anvil.server.call('get_users')]
    self.owners.append(('None', Data.NO_AGENTS_SELECTED))
    
    self.selected_tickets = []
    self.filtered_tickets = []
    self.init_components(**properties)
    self.load_tickets()

    emitter.form_subscribe(self, 'select-ticket', self.select_ticket_change)
    emitter.form_subscribe(self, 'unselect-select-all-tickets-box', self.unselect_box)
  
  def load_tickets(self):
    self.filters = {k: v for k, v in self.filters.items() if v is not None}
    self.filtered_tickets = anvil.server.call('get_tickets', self.sort, self.filters, self.date_filter)
    self.refresh_data_bindings()
    self.set_pages()
  
  def update_selected_tickets(self):
    if len(self.selected_tickets) == 0:
      self.selected_label.text = ""
      self.selected_label.visible = False
      self.clear_selected_link.visible = False
    else:
      self.selected_label.text = f"{len(self.selected_tickets)} tickets selected"
      self.selected_label.visible = True
      self.clear_selected_link.visible = True
    
  def clear_filters_link_click(self, **event_args):
    self.filters = {}
    self.date_filter = {}
    self.sort_dropdown.selected_value = 'Date'
    self.load_tickets()

  def select_ticket_change(self, ticket, selected, **event_args):
    if selected:
      if ticket not in self.selected_tickets:
        self.selected_tickets.append(ticket)
    else:
      if ticket in self.selected_tickets:
        self.selected_tickets.remove(ticket)
    self.update_selected_tickets()

  def clear_selected_link_click(self, **event_args):
    self.select_all_box.checked = False
    self.select_all_box_change()
    self.update_selected_tickets()
    
  def first_page_link_click(self, **event_args):
    self.data_grid_1.jump_to_first_page()
    self.set_pages()

  def previous_page_link_click(self, **event_args):
    self.data_grid_1.previous_page()
    self.set_pages()

  def next_page_link_click(self, **event_args):
    self.data_grid_1.next_page()
    self.set_pages()

  def last_page_link_click(self, **event_args):
    self.data_grid_1.jump_to_last_page()
    self.set_pages()

  def close_tickets_link_click(self, **event_args):
    """ set to closed status """
    confirmed = True
    if len(self.selected_tickets) > 1:
      confirmed = confirm("You are about to close multiple tickets. Are you sure?")
    
    if confirmed: 
      anvil.server.call('close_tickets', self.selected_tickets) 
      self.refresh_data_bindings()

  def select_all_box_change(self, **event_args):
    self.selected_tickets = []
    if self.select_all_box.checked:
      self.selected_tickets += self.filtered_tickets
      for t in self.tickets_repeating_panel.get_components():
        # t.pseudo_select_click(force = {'value': True})
        t.select_ticket.checked = True
        t.select_ticket.select_ticket_change()
    else:
      for t in self.tickets_repeating_panel.get_components():
        # t.pseudo_select_click(force = {'value': False})
        t.select_ticket.checked = False
        t.select_ticket.select_ticket_change()

  def sort_dropdown_change(self, **event_args):
    if self.sort_dropdown.selected_value == 'Agent':
      self.sort = 'owner'
    else:
      self.sort = self.sort_dropdown.selected_value.lower()
    self.load_tickets()

  def apply_filter_button_click(self, **event_args):
    print(self.filters, self.date_filter)
    self.load_tickets()

  # manages the pagination label and controls
  def set_pages(self):
    page = self.data_grid_1.get_page()
    no_rows = self.data_grid_1.rows_per_page
    start_page = ((page + 1) * no_rows)
    end_page = min(start_page, len(self.filtered_tickets))
    text = f"{(page * no_rows) + 1}-{end_page} of {len(self.filtered_tickets)}"
    self.pagination_label.text = text

    self.last_page_link.visible = end_page is not len(self.filtered_tickets)
    self.next_page_link.visible = end_page is not len(self.filtered_tickets)

    self.first_page_link.visible = (page * no_rows) is not 0
    self.previous_page_link.visible = (page * no_rows) is not 0
    
  def unselect_box(self, **event_args):
    self.select_all_box.checked = False