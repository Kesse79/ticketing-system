from ._anvil_designer import StatCardTemplate
from ....utils import Properties

class StatCard(StatCardTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.item = {'number': 0, 'delta': None}
    self.init_components(**properties)

  def set_up_is_good(self, value):
    self.set_diff_marker()
  up_is_good = Properties.property_with_callback(set_up_is_good)

  def set_title(self, value):
    self.title_label.text = value or "Title"
  title = Properties.property_with_callback(set_title)

  def set_diff_marker(self):
    diff = self.item['delta']
    if diff is None:
      self.delta_label.text = "currently unsesolved"
      return None
    elif diff == 0:
      self.delta_label.text = "- -"
      self.role = "stat-card"
      self.delta_label.foreground = "theme:Lilac 700"
      return None
    elif diff > 0:
      self.delta_label.text = abs(self.item['delta'])
      self.delta_label.foreground = "theme:Secondary 600" if self.up_is_good else "theme:Error 500"
      self.role = ["stat-card", "stat-card-up"]
      return 'fa:arrow-up'
    else:
      self.delta_label.text = abs(self.item['delta'])
      self.delta_label.foreground = "theme:Error 500" if self.up_is_good else "theme:Secondary 600"
      self.role = ["stat-card", "stat-card-down"]
      return 'fa:arrow-down'

  def link_1_click(self, **event_args):
    self.raise_event("click")
