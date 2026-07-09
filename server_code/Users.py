from anvil.tables import app_tables
from .Utils import *

@authenticated_callable
def get_users():
  return app_tables.users.search()