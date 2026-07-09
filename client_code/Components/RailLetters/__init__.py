from ._anvil_designer import RailLettersTemplate
from ...utils import emitter

class RailLetters(RailLettersTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    if self.item['visible']:
      self.rail_link.foreground = 'theme:Grey 600'

  def rail_link_click(self, **event_args):
    selected_letter = self.item['letter']
    emitter.emit('scroll-to-letter-group', letter = selected_letter)
