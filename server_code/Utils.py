import anvil.server
import functools
import anvil.users


authenticated_callable = anvil.server.callable(require_user=True)