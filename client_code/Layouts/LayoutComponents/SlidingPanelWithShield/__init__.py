from ._anvil_designer import SlidingPanelWithShieldTemplate
from ....utils import Properties, emitter

class SlidingPanelWithShield(SlidingPanelWithShieldTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.handle_shield_click = self.handle_shield_click
    self.init_components(**properties)
    
    self.add_event_handler("x-anvil-page-added", self.on_mount)
    self.add_event_handler("x-anvil-page-removed", self.on_cleanup)  
    
  def on_mount(self, **event_args):
    self.dom_nodes['shield'].addEventListener('click', self.handle_shield_click)
    
  def on_cleanup(self, **event_args):
    self.dom_nodes['shield'].removeEventListener('click', self.handle_shield_click)
  
  def handle_shield_click(self, *args):
    emitter.emit('close-sliding-panel')

  def set_open(self, value):
    self.dom_nodes['shield'].classList.toggle('open', value)
  open = Properties.property_with_callback(set_open)
