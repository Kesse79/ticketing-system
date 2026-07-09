from ._anvil_designer import BaseLayoutTemplate

class BaseLayout(BaseLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
