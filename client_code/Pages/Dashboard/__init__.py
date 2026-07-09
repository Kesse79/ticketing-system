from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
from ...utils import Data, Properties, emitter
from ...utils.Navigation import navigate
from datetime import datetime, timedelta, date

class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.last_week = date.today() - timedelta(days=6)
    # Initialise a dict of empty filters when the dashboard loads
    self.filters = {}
    # Initialise a dict of empty date filters when the dashboard loads
    self.date_filters = {}
    self.initialise_start_dates()
    # This returns a list of tuples to form the items of the category_dropdown. 
    # category_dropdown is data bound to self.categories
    self.categories = Data.CATEGORIES
    # This returns a list of tuples to form the items of the priority_dropdown. 
    # priority_dropdown is data bound to self.priorities
    self.priorities = Data.PRIORITIES
    # Set Form properties and Data Bindings.
    self.headline_stats = {'new_tickets': {'delta': 0, 'number': 0}, 'closed_tickets': {'delta': 0, 'number': 0}, 'all_open': {'number': 0, 'delta': None}}
    self.colors = {
      'unresolved-line': Properties.theme_color_to_css('theme:Secondary 500'),
      'unresolved-fill': Properties.theme_color_to_css('theme:Secondary 500'),
      'resolved-line': Properties.theme_color_to_css('theme:Lilac 500'),
      'resolved-fill': Properties.theme_color_to_css('theme:Lilac 400')
    }
    
    self.init_components(**properties)
  def initialise_start_dates(self):
    # Initialise the DatePickers so that Dashboard auto-displays data for the previous week
    self.date_filters['start'] = (date.today() - timedelta(days=6))
    self.date_filters['end'] = date.today()
    # Work out the time period for the dashboard data
    self.date_filters['time_period'] = (self.date_filters['end'] - self.date_filters['start']).days
    
  def initialise_dashboard_data(self):
    # Ensure timeperiod runs from start date to *end* of end date, by adding a day to end date
    self.date_filters['end'] = self.end_date_picker.date + timedelta(days=1)
    # Work out the time period for the dashboard data
    self.date_filters['time_period'] = (self.date_filters['end'] - self.date_filters['start']).days
    # Get all the data to populate the dashboard from the server
    headline_stats, progress_dash_stats, resolution_data = anvil.server.call('get_dashboard_data', self.date_filters, self.filters)
    self.headline_stats = headline_stats

    self.initialise_progress_charts(progress_dash_stats)
    self.initialise_resolution_chart(resolution_data)
    self.refresh_data_bindings()
  
  def form_show(self, **event_args):
    self.initialise_dashboard_data()

  def apply_filter_button_click(self, **event_args):
    self.initialise_dashboard_data()

  def clear_filters_link_click(self, **event_args):
    self.filters = {}
    self.initialise_start_dates()
    self.refresh_data_bindings()
    self.initialise_dashboard_data()

  def change_filter(self, sender, **event_args):
    if sender.selected_value is None:
      self.filters = {k: v for k, v in self.filters.items() if v is not None}
    self.refresh_data_bindings()

  # This is called initially in the form_show event of the Dashboard Form
  def initialise_progress_charts(self, progress_dash_stats):
    """Collect data and populate the two ProgressGraph charts, and the text for the accompanying labels.
    
    Arguments:
      progress_dash_stats: dict of data in this form:
                          {
                            'resolved': {
                              'total_resolved': len(resolved_tickets), 'closed_on_first':len(closed_on_first)
                            }, 
                            'customers':{
                              'new_customers':len(new_customers), 'returning_customers':len(returning_customers)
                            }
                          }  
    """
    # Get number of total resolved tickets and number of tickets closed on the first reply
    total_resolved = progress_dash_stats['resolved']['total_resolved']
    closed_on_first = progress_dash_stats['resolved']['closed_on_first']
    # Set display values to zero if no tickets resolved over the period
    if total_resolved == 0:
      self.closed_on_first_label.text = "No tickets resolved"
      self.closed_on_first_chart.percentage = 0
    # If tickets were resolved over the period, populate the data accordingly
    else:
      closed_on_first_percent = round(max((closed_on_first/total_resolved), 0),2)
      self.closed_on_first_label.text = f"{closed_on_first} ticket{' was' if closed_on_first == 1 else 's were'} resolved with the first reply"
      self.closed_on_first_chart.percentage = closed_on_first_percent
    # Get number of new customers and number of returning customers
    new_customers = progress_dash_stats['customers']['new_customers']
    returning_customers = progress_dash_stats['customers']['returning_customers']
    # If no new customers, set the data accordingly
    if new_customers == 0:
      self.new_custs_label.text = f"No new customers \n{returning_customers} returning customers"
      self.new_custs_chart.percentage = 0
      self.new_custs_chart.display_value = 0
    else:
      # Set percentage of new customers
      new_cust_percent = round(max((new_customers / (new_customers + returning_customers)), 0),2)
      self.new_custs_chart.percentage = new_cust_percent
      self.new_custs_chart.display_value = new_cust_percent
      self.new_custs_label.text = f"{new_customers} new customer{'' if new_customers == 1 else 's'} \n{returning_customers} returning customer{'' if returning_customers == 1 else 's'}"
  
  def initialise_resolution_chart(self, resolution_data):
    """Collect data and populate the ResolutionGraph custom component. 
    
    Arguments:
      resolution_data: dict of data in this form:
                      {'dates':dates, 'data':
                          {'resolved':resolved, 
                          'unresolved':unresolved}
                      }
    Dates is a list of dates in the form '%A, %d' 
    e.g. ['Friday, 07', 'Saturday, 08', 'Sunday, 09', 'Monday, 10', 'Tuesday, 11', 'Wednesday, 12', 'Thursday, 13']
    Resolved and unresolved are lists of numbers of tickets created on the days in the dates list 
    e.g [1,0,1,2,3,4,5]
    """
    labels = resolution_data['dates']
    data = resolution_data['data']
    self.resolution_graph.labels = labels
    self.resolution_graph.datasets = [{
            'label': 'Resolved',
            'backgroundColor': self.colors['resolved-fill'],
            'borderColor': self.colors['resolved-line'],
            'data': data['resolved']
        },{
            'label': 'Unresolved',
            'backgroundColor': self.colors['unresolved-fill'],
            'borderColor': self.colors['unresolved-line'],
            'data': data['unresolved']
        }]

  def unassigned_card_click(self, **event_args):
    navigate(page='tickets', search_filters = None, initial_date_filters = self.date_filters)

  def unresolved_card_click(self, **event_args):
    navigate(page='tickets', search_filters = {'status': Data.OPEN}, initial_date_filters = self.date_filters)

  def urgent_card_click(self, **event_args):
    navigate(page='tickets', search_filters = {'priority': Data.URGENT}, initial_date_filters = self.date_filters)

  def new_tickets_stat_click(self, **event_args):
    filters = {'category': None, 'status': None, 'priority': None, 'customer': None, 'owner': None} 
    navigate(page='tickets', search_filters = filters, initial_date_filters = {'start': self.last_week})

  def closed_tickets_stat_click(self, **event_args):
    navigate(page='tickets', search_filters = {'status': Data.CLOSED}, initial_date_filters = {'closed_start': self.last_week})

  def open_tickets_stat_click(self, **event_args):
    navigate(page='tickets', search_filters = {'status': Data.OPEN})
    
   