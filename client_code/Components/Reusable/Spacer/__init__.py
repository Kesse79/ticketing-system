from ._anvil_designer import SpacerTemplate
from ....utils import Properties

class Spacer(SpacerTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)
  spacing = Properties.spacing_property('spacer')
