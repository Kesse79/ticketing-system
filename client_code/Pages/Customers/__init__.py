from ._anvil_designer import CustomersTemplate
from anvil import *
import anvil.server
import string
from ...utils import emitter, Validation
from ...utils.Navigation import navigate

class Customers(CustomersTemplate):
  def __init__(self, open_customer = None, **properties):
    self.customers = anvil.server.call('get_customers')
    self.customer_groups = []
    self.open_customer = open_customer

    # Dummy object so databindings don't break on init if no customer is pre-selected
    self.customer_copy = dict(self.open_customer) if self.open_customer else { 
      'first_name': "",
      'last_name': "",
      'company': "",
      'title': "",
      'phone': "",
      'email': ""
    }
    self.customer_tickets = []

    self.selected_customers = []
    self.init_components(**properties)
    emitter.form_subscribe(self, 'close-sliding-panel', self.close_sliding_panel)
    emitter.form_subscribe(self, 'scroll-to-letter-group', self.scroll_to_letter)
    emitter.form_subscribe(self, 'open-customer-details', self.set_open_customer)
    emitter.form_subscribe(self, 'all-customer-select-customer', self.update_selected_customers)
    emitter.form_subscribe(self, 'unselect-select-all-customers-box', self.unselect_box)
    
    self.open_or_close_customer_panel()
    if self.open_customer:
      self.customer_tickets = anvil.server.call('get_customer_tickets', filters={'customer': self.open_customer})

    #for setting up letter rail
    letters = list(string.ascii_uppercase)
    data = []
    for let in letters:
    # Group all our customers by letter of the alphabet
      customers = [x for x in self.customers if x['last_name'][0].upper() == let]
      if customers:
        data.append({'letter': let, 'customers': customers})
    
    # Work out which letters of the alphabet should be visible
    # Don't show letters if none of our customers' surnames begin with that letter
    visible_letters = [x['letter'] for x in data]
    letters = [{
        'letter': x,
        'visible': x in visible_letters
      } for x in string.ascii_uppercase]
    
    self.customer_groups = data
    self.refresh_data_bindings()
    
    self.letters_repeating_panel.items = letters
  
  def scroll_to_letter(self, letter, **args):
    for letter_group in self.letter_group_repeating_panel.get_components():
      if letter_group.item['letter'] == letter:
        letter_group.letter.scroll_into_view() 

  def open_or_close_customer_panel(self):
    self.layout.details_visible = bool(self.open_customer)
    self.refresh_data_bindings()
    emitter.emit('style-opened-customer', customer = self.open_customer)
  
  def set_open_customer(self, customer, **args):
    self.customer_tickets = []
    if self.open_customer is customer:
      self.open_customer = None
    else:
      self.open_customer = customer
      self.customer_copy = dict(customer)
      self.customer_tickets = anvil.server.call('get_customer_tickets', filters={'customer': self.open_customer})
    self.open_or_close_customer_panel()
  
  def close_sliding_panel(self, **event_args):
    self.layout.slide_open = False

  def close_details_panel(self, **event_args):
    self.set_open_customer(self.open_customer)

  def edit_details_link_click(self, **event_args):
    self.layout.slide_open = True

  def update_selected_customers(self, customer, selected, **event_args):
    if selected:
      if customer not in self.selected_customers:
        self.selected_customers.append(customer)
    else:
      if customer in self.selected_customers:
        self.selected_customers.remove(customer)
    self.clear_selected_link.visible = len(self.selected_customers) > 0
  
  def delete_cust_link_click(self, **event_args):
    name = f"{self.open_customer['first_name']} {self.open_customer['last_name']}"
    if confirm("""Are you sure you want to delete these customer(s)?: \n{}
                \nThis will also delete all tickets associated with this customer.""".format(name)): 
      anvil.server.call('delete_customers', [self.open_customer])
      Notification('Customer deleted successfully').show()
      navigate(page='customers')

  def save_link_click(self, **event_args):
    cust_validation_errors = Validation.get_customer_errors(self.customer_copy)
    if not cust_validation_errors:
      anvil.server.call('update_customer', self.open_customer, self.customer_copy)
      Notification('Customer details updated').show()
      self.refresh_data_bindings()
      self.layout.slide_open = False
    else:
      alert("The following fields are missing for your customer: \n{}".format(
        ' \n'.join(cust_validation_errors)
      ))

  def on_select_all_toggled(self, **event_args):
    self.selected_customers = []
    if self.select_all_box.checked:
      for group in self.letter_group_repeating_panel.get_components():
        for customer in group.customer_repeating_panel.get_components():
          customer.checkbox.checked = True
          customer.checkbox_change();
    else:
      for group in self.letter_group_repeating_panel.get_components():
        for customer in group.customer_repeating_panel.get_components():
          customer.checkbox.checked = False
          customer.checkbox_change();
      self.clear_selected_link.visible = False

  def delete_link_click(self, **event_args):
    if (len(self.selected_customers) > 0):
      names = [f"{c['first_name']} {c['last_name']}" for c in self.selected_customers]
      if confirm("""Are you sure you want to delete these customer(s)?: \n{} 
                 \nThis will also delete all tickets associated with this customer.""".format(' \n'.join(names))):
        anvil.server.call('delete_customers', self.selected_customers)
        Notification('Customers deleted successfully').show()
        navigate(page='customers')
                   
    else:
      alert("No Customers selected", "Error")

  def clear_selected_link_click(self, **event_args):
    self.select_all_box.checked = False
    self.on_select_all_toggled()

  def unselect_box(self, **event_args):
    self.select_all_box.checked = False

  def new_ticket_of_customer_click(self, **event_args):
    navigate(page="new_ticket", customer=self.open_customer)
