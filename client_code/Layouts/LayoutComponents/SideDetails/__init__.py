from ._anvil_designer import SideDetailsTemplate
from anvil import HtmlTemplate

class SideDetails(SideDetailsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  visible = HtmlTemplate.visible
