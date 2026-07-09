from ._anvil_designer import CustomerLetterGroupTemplate

class CustomerLetterGroup(CustomerLetterGroupTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)
