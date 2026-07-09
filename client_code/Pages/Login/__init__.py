from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.users
from ...utils.Navigation import navigate

class Login(LoginTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  # If already logged in, go to dashboard
  def form_show(self, **event_args):
    if anvil.users.get_user():
      navigate(page="dashboard")

  def login_button_click(self, **event_args):
    if anvil.users.login_with_form():
      navigate(page="dashboard")