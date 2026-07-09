from ._anvil_designer import AppBaseTemplate
import anvil.users
from ....utils.Navigation import navigate

class AppBase(AppBaseTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
  def dashboard_link_click(self, **event_args):
    navigate(page='dashboard')

  def tickets_link_click(self, **event_args):
    navigate(page='tickets')

  def customers_link_click(self, **event_args):
    navigate(page='customers')

  def new_ticket_button_click(self, **event_args):
    navigate(page='new_ticket')

  def signout_links_click(self, **event_args):
    anvil.users.logout()
    navigate(page='login')

  def form_show(self, **event_args):
    if anvil.users.get_user():
      self.user_email_label.text = anvil.users.get_user()['name'] or anvil.users.get_user()['email']
  