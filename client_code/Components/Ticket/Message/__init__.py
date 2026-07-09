from ._anvil_designer import MessageTemplate
from ....utils import Data

class Message(MessageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def set_to_labels(self):
    if self.item['type'] == Data.INTERNAL:
      return "[INTERNAL NOTE]"
    elif self.item['type'] == Data.INCOMING:
      return "To: Support"
    else:
      return f"To: {self.item['ticket']['customer']['first_name']} {self.item['ticket']['customer']['last_name']}"

  def set_from_labels(self):
    if self.item['type'] == Data.INCOMING:
      self.left.visible = True
      self.right.visible = False
      return f"From: {self.item['ticket']['customer']['first_name']} {self.item['ticket']['customer']['last_name']}"
    else:
      return f"From: {self.item['agent']['email']}"

 

