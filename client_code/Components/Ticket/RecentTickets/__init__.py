from ._anvil_designer import RecentTicketsTemplate

class RecentTickets(RecentTicketsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
