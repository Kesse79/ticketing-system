from ._anvil_designer import PrimaryWithTwoSecondaryTemplate

class PrimaryWithTwoSecondary(PrimaryWithTwoSecondaryTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
