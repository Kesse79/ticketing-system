from ._anvil_designer import PublicTicketIntakeTemplate
from anvil import *
import anvil.server

from ...utils import emitter
from ...utils.Navigation import navigate


ONE_TIME_FEE = 27
ANNUAL_FEE = 9
MAX_ID_NUMBERS = 100


class PublicTicketIntake(PublicTicketIntakeTemplate):
  def __init__(self, **properties):
    self.id_numbers = []
    self.init_components(**properties)
    emitter.form_subscribe(self, "remove-public-id-number", self.remove_id_number)
    self.update_invoice_totals()
    self.set_status("")

  def set_status(self, message, is_error=False):
    self.status_label.text = message
    self.status_label.visible = bool(message)
    self.status_label.role = "customer-intake-error" if is_error else "customer-intake-success"

  def get_payload(self):
    return {
      "company_name": self.company_name_input.text,
      "company_address": self.company_address_area.text,
      "company_vat": self.company_vat_input.text,
      "contact_first_name": self.contact_first_name_input.text,
      "contact_last_name": self.contact_last_name_input.text,
      "company_email": self.company_email_input.text,
      "company_phone": self.company_phone_input.text,
      "folder_name": self.folder_name_input.text,
      "id_numbers": list(self.id_numbers),
    }

  def get_missing_fields(self, payload):
    required_fields = [
      ("company_name", "Company name"),
      ("company_address", "Company address"),
      ("company_vat", "Company VAT"),
      ("contact_first_name", "Contact name"),
      ("contact_last_name", "Contact surname"),
      ("company_email", "Company email"),
      ("company_phone", "Company phone"),
      ("folder_name", "Folder name"),
    ]
    missing = [label for key, label in required_fields if not (payload.get(key) or "").strip()]
    if not payload["id_numbers"]:
      missing.append("At least one ID number")
    return missing

  def update_invoice_totals(self):
    count = len(self.id_numbers)
    self.id_numbers_panel.items = [{"value": value} for value in self.id_numbers]
    self.id_count_label.text = f"{count} ID number{'s' if count != 1 else ''}"
    self.one_time_total_label.text = f"{count} x {ONE_TIME_FEE} EUR = {count * ONE_TIME_FEE} EUR"
    self.annual_total_label.text = f"{count} x {ANNUAL_FEE} EUR = {count * ANNUAL_FEE} EUR per year"
    self.id_limit_label.text = f"{MAX_ID_NUMBERS - count} remaining this session"

  @handle("operator_login_button", "click")
  def operator_login_button_click(self, **event_args):
    navigate(page="login")

  @handle("add_id_button", "click")
  def add_id_button_click(self, **event_args):
    self.add_id_number()

  @handle("id_number_input", "pressed_enter")
  def id_number_input_pressed_enter(self, **event_args):
    self.add_id_number()

  def add_id_number(self):
    value = (self.id_number_input.text or "").strip()
    if not value:
      self.set_status("Enter an ID number before adding it.", True)
      return
    if len(self.id_numbers) >= MAX_ID_NUMBERS:
      self.set_status("You can add up to 100 ID numbers per session.", True)
      return
    self.id_numbers.append(value)
    self.id_number_input.text = ""
    self.set_status("")
    self.update_invoice_totals()

  def remove_id_number(self, item=None, **event_args):
    if item and item.get("value") in self.id_numbers:
      self.id_numbers.remove(item["value"])
      self.update_invoice_totals()
      self.set_status("")

  @handle("clear_button", "click")
  def clear_button_click(self, **event_args):
    self.company_name_input.text = ""
    self.company_address_area.text = ""
    self.company_vat_input.text = ""
    self.contact_first_name_input.text = ""
    self.contact_last_name_input.text = ""
    self.company_email_input.text = ""
    self.company_phone_input.text = ""
    self.folder_name_input.text = ""
    self.id_number_input.text = ""
    self.id_numbers = []
    self.update_invoice_totals()
    self.set_status("")

  @handle("submit_button", "click")
  def submit_button_click(self, **event_args):
    payload = self.get_payload()
    missing = self.get_missing_fields(payload)
    if missing:
      self.set_status("Please complete: " + ", ".join(missing), True)
      return

    self.submit_button.enabled = False
    self.set_status("Submitting your ticket...")
    try:
      result = anvil.server.call("create_public_ticket", payload)
      self.set_status(f"Ticket #{result['number']} has been created. We will contact you by email.")
    except Exception as err:
      self.set_status(str(err), True)
    finally:
      self.submit_button.enabled = True
