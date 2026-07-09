from ._anvil_designer import FlexContainerTemplate
from ....utils import Properties

class FlexContainer(FlexContainerTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)
 
  def set_use_background(self, value):
    self.dom_nodes['main-content-section'].style.backgroundImage = "url('_/theme/resources/grey-squiggles.png')" if value else ""
  use_background = Properties.property_with_callback(set_use_background)
