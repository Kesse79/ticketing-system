import anvil.server
from anvil.tables import app_tables

CATEGORIES = [(x['name'], x) for x in app_tables.categories.search()]
PRIORITIES = [(x['name'], x) for x in app_tables.priorities.search()]
STATUS = [(x['name'], x) for x in app_tables.status.search()]
OPEN = app_tables.status.get(name="Open")
URGENT = app_tables.priorities.get(name="Urgent")
CLOSED = app_tables.status.get(name="Closed")
OUTGOING = app_tables.types.get(name="OUTGOING_EMAIL")
INTERNAL = app_tables.types.get(name="INTERNAL_NOTE")
INCOMING = app_tables.types.get(name="INCOMING_EMAIL")
CURRENT_TICKET_NO = app_tables.currentticketno.search()[0]['number']
NO_AGENTS_SELECTED = 'None'
NEW_CATEGORY = app_tables.categories.get(name="New")
NEW_PRIORITY = app_tables.priorities.get(name="New")

@anvil.server.callable
def get_initial_data():
  return dict(
    CATEGORIES = CATEGORIES,
    PRIORITIES = PRIORITIES,
    STATUS = STATUS,
    OPEN = OPEN,
    URGENT = URGENT,
    CLOSED = CLOSED,
    OUTGOING = OUTGOING,
    INTERNAL = INTERNAL,
    INCOMING = INCOMING,
    CURRENT_TICKET_NO = CURRENT_TICKET_NO,
    NO_AGENTS_SELECTED = NO_AGENTS_SELECTED,
    NEW_CATEGORY = NEW_CATEGORY,
    NEW_PRIORITY = NEW_PRIORITY
  )
