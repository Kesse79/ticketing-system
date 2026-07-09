from ._anvil_designer import PlusTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
from anvil import HtmlTemplate
from ....utils import Properties

class Plus(PlusTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)

  visible = HtmlTemplate.visible
  align = Properties.align_property('component')

  def set_size(self, value):
    self.dom_nodes['icon'].style.width = f"{value}px"
  size = Properties.property_with_callback(set_size)

  def set_fill(self, value):
    color = Properties.theme_color_to_css(value)
    for node in self.dom_nodes['icon'].querySelectorAll('.st2'):
      node.style.stroke = color
  fill = Properties.property_with_callback(set_fill)
