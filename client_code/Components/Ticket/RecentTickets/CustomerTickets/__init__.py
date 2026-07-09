from ._anvil_designer import CustomerTicketsTemplate
from .....utils.Navigation import navigate

class CustomerTickets(CustomerTicketsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def recent_ticket_link_click(self, **event_args):
    navigate(page='ticket', ticket=self.item['ticket'])
