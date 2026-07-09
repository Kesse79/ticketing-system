"""This module collects global variables to be used throughout the app"""

import anvil.server


# CATEGORIES = [(x['name'], x) for x in app_tables.categories.search()]
# PRIORITIES = [(x['name'], x) for x in app_tables.priorities.search()]
# STATUS = [(x['name'], x) for x in app_tables.status.search()]
# OPEN = app_tables.status.get(name="Open")
# URGENT = app_tables.priorities.get(name="Urgent")
# CLOSED = app_tables.status.get(name="Closed")
# OUTGOING = app_tables.types.get(name="OUTGOING_EMAIL")
# INTERNAL = app_tables.types.get(name="INTERNAL_NOTE")
# INCOMING = app_tables.types.get(name="INCOMING_EMAIL")
# CURRENT_TICKET_NO = app_tables.currentticketno.search()[0]['number']
# NO_AGENTS_SELECTED = 'None'
# NEW_CATEGORY = app_tables.categories.get(name="New")
# NEW_PRIORITY = app_tables.priorities.get(name="New")

data = {}


# allows for autocompletions of this module
def __dir__():
  return [
    "CATEGORIES",
    "PRIORITIES",
    "STATUS",
    "OPEN",
    "URGENT",
    "CLOSED",
    "OUTGOING",
    "INTERNAL",
    "INCOMING",
    "CURRENT_TICKET_NO",
    "NO_AGENTS_SELECTED",
    "NEW_CATEGORY",
    "NEW_PRIORITY"
  ]


def get_initial_data():
  global data
  data = anvil.server.call("get_initial_data")


def __getattr__(name):
  rv = data.get(name)
  if rv is None:
    raise AttributeError(name)
  return rv
