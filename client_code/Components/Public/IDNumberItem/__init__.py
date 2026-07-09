from ._anvil_designer import IDNumberItemTemplate
from anvil import *

from ....utils import emitter


class IDNumberItem(IDNumberItemTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  @handle("remove_button", "click")
  def remove_button_click(self, **event_args):
    emitter.emit("remove-public-id-number", item=self.item)
