from ._anvil_designer import BlankPrimaryWithFormTemplate

class BlankPrimaryWithForm(BlankPrimaryWithFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)