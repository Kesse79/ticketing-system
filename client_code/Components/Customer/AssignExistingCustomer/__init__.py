from ._anvil_designer import AssignExistingCustomerTemplate
from ....utils import Properties, emitter

class AssignExistingCustomer(AssignExistingCustomerTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)
    emitter.form_subscribe(self, 'assign-existing-customer', self.on_selected)

  def set_selected(self, value):
    self._anvil_dom_element_.classList.toggle("selected", value)
    if value: 
      self.check_box.icon = "fa:check-square"
      self.last_name_label.foreground = "theme:Lilac 500"
      self.role = ["assign-customer-card", "assigned"]
    else:
      self.check_box.icon = "fa:square-o"
      self.last_name_label.foreground = "theme:Grey 950"
      self.role = ["assign-customer-card"]
  selected = Properties.property_with_callback(set_selected)

  def customer_link_click(self, **event_args):
    emitter.emit('assign-existing-customer', item = self.item)

  def on_selected(self, item = None, **event_args):
    self.selected = item is self.item