from ._anvil_designer import PrimaryContentTemplate

class PrimaryContent(PrimaryContentTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
