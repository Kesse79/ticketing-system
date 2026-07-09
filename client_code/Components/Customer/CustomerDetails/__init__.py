from ._anvil_designer import CustomerDetailsTemplate

class CustomerDetails(CustomerDetailsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)