from ._anvil_designer import TicketStatusIndicatorTemplate
from anvil import HtmlTemplate
from ....utils import Properties

class TicketStatusIndicator(TicketStatusIndicatorTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)

  visible = HtmlTemplate.visible
  def set_status(self, value):
    self.dom_nodes['indicator-text'].innerText = value
    if value == 'OVERDUE':
      self.dom_nodes['indicator-text'].style.removeProperty("background")
      self.dom_nodes['indicator-tail'].style.removeProperty("background")
    else:
      self.dom_nodes['indicator-text'].style.background = "var(--secondary-600)"
      self.dom_nodes['indicator-tail'].style.background = "var(--secondary-800)"
  status = Properties.property_with_callback(set_status)