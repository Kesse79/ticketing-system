from .utils import Data
from .utils.Navigation import navigate
from anvil import set_default_error_handling
import anvil.users

# On Authentication failure, navigates back to login back. Throw error as usual for any other type of error
def error_handler(err):
  if isinstance(err, anvil.users.exceptions.AuthenticationFailed):
    navigate(page='login')
  else:
    raise err
set_default_error_handling(error_handler)

def start_up():
  Data.get_initial_data()
  navigate(page="login")

if __name__ == "__main__":
  start_up()