from ._anvil_designer import AllCustomerTemplate
from ....utils import emitter

class AllCustomer(AllCustomerTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    emitter.form_subscribe(self, 'style-opened-customer', self.style_opened)

  def style_opened(self, customer = None, **event_args):
    if self.item == customer:
      self.last_label.foreground = "theme:Lilac 500"
      self.role = ['all-customers-card', 'opened-customer']
    else:
      self.last_label.foreground = None
      self.role = ['all-customers-card']

  def customer_name_link_click(self, **event_args):
    emitter.emit('open-customer-details', customer=self.item)

  def checkbox_change(self, **event_args):
    if not self.checkbox.checked:
      emitter.emit('unselect-select-all-customers-box')
    emitter.emit('all-customer-select-customer', customer=self.item, selected = self.checkbox.checked)