from ._anvil_designer import AppButtonTemplate
from anvil import HtmlTemplate
from ....utils import Properties

class AppButton(AppButtonTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)
    self._handle_click = self._handle_click

    self.add_event_handler("x-anvil-page-added", self._on_mount)
    self.add_event_handler("x-anvil-page-removed", self._on_cleanup)

  def _on_mount(self, **event_args):
    self.dom_nodes['app-button-component'].addEventListener('click', self._handle_click)
  def _on_cleanup(self, **event_args):
    self.dom_nodes['app-button-component'].removeEventListener('click', self._handle_click)
  
  def _handle_click(self, event):
    event.preventDefault()
    self.raise_event("click")

  visible = HtmlTemplate.visible
  align = Properties.align_property('app-button-component')

  def set_size(self, value):
    self.dom_nodes['app-button'].classList.toggle('small', False)
    self.dom_nodes['app-button'].classList.toggle('large', False)
    self.dom_nodes['app-button'].classList.toggle(value, True)
  size = Properties.property_with_callback(set_size)

  def set_appearance(self, value):
    self.dom_nodes['app-button'].classList.toggle('primary', False)
    self.dom_nodes['app-button'].classList.toggle('secondary', False)
    self.dom_nodes['app-button'].classList.toggle(value, True)
  appearance = Properties.property_with_callback(set_appearance)
  