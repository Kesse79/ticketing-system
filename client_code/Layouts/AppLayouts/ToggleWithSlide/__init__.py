from ._anvil_designer import ToggleWithSlideTemplate
from ....utils import Properties

class ToggleWithSlide(ToggleWithSlideTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)

  def set_slide_open(self, value):
    self.sliding_panel_with_shield.open = value
  slide_open = Properties.property_with_callback(set_slide_open)

  def set_details_visible(self, value):
    self.side_details_1.visible = value
    if not value:
      self.slide_open = False
  details_visible = Properties.property_with_callback(set_details_visible)
