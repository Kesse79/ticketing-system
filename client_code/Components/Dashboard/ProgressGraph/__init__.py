from ._anvil_designer import ProgressGraphTemplate
from ....utils import Properties

class ProgressGraph(ProgressGraphTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)

  percentage = Properties.style_property("progress-chart", "--percent")

  def set_display_value(self, value):
    text = value
    if isinstance(value, (int, float)):
      text = f"{value:.0%}"
    self.dom_nodes["progress-chart-text"].textContent = text

  display_value = Properties.property_with_callback(set_display_value)
