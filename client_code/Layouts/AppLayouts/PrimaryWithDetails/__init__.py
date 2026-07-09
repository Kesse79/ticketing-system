from ._anvil_designer import PrimaryWithDetailsTemplate

class PrimaryWithDetails(PrimaryWithDetailsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)