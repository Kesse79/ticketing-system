from ._anvil_designer import NavLinkTemplate
from ...utils import Properties, emitter


class NavLink(NavLinkTemplate):
  def __init__(self, **properties):
    self._props = properties
    self.init_components(**properties)
    emitter.form_subscribe(self, "set_active_nav_style", self.update_active)

    self.handle_click = self.handle_click
    self.add_event_handler("x-anvil-page-added", self.on_mount)
    self.add_event_handler("x-anvil-page-removed", self.on_cleanup)

  def on_mount(self, **event_args):
    self.dom_nodes["navlink-component"].addEventListener("click", self.handle_click)

  def on_cleanup(self, **event_args):
    self.dom_nodes["navlink-component"].removeEventListener("click", self.handle_click)

  name = Properties.basic_property()

  def handle_click(self, event):
    event.preventDefault()
    self.raise_event("click")

  text = Properties.innerText_property("navlink-text")

  def set_active(self, value):
    self.dom_nodes["navlink-component"].classList.toggle("activeNav", value)
  active = Properties.property_with_callback(set_active)

  def update_active(self, nav_name=None, **event_args):
    self.active = self.name == nav_name
