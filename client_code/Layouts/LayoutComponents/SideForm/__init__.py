from ._anvil_designer import SideFormTemplate

class SideForm(SideFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
