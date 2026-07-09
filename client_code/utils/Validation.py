"""This module is responsible for validating user inputs.

It is used to verify inputs by both client code and server code
"""

required_customer_keys = ['first_name', 'last_name', 'title', 'company', 'email', 'phone']
required_ticket_keys = ['title', 'priority', 'category', 'due']
required_ticket_settings_keys = ['title', 'priority', 'category', 'due', 'status']
required_message_keys = ['type', 'details']

def make_error_validator(required_keys):
  def validate(data_dict):
    missing_keys = []
    for k in required_keys:
      if not data_dict.get(k, None):
        missing_keys.append(k)
    return missing_keys or None
  
  return validate

get_customer_errors = make_error_validator(required_customer_keys)

get_ticket_errors = make_error_validator(required_ticket_keys)

get_ticket_settings_errors = make_error_validator(required_ticket_settings_keys)

get_message_errors = make_error_validator(required_message_keys)
