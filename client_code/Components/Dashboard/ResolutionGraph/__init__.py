from ._anvil_designer import ResolutionGraphTemplate
from ....utils import Properties
from anvil.js.window import Chart

Chart.defaults.font.size = 12
options = {
  'elements': {'point': {'radius': 0, 'hitRadius': 5, 'hoverRadius': 5}, 'line': {'fill': True, 'tension': 0.4}},
  'layout': {'padding': {'left': 50, 'right': 50, 'top': 0, 'bottom': 50}},
  'legend': {'position': 'top'},
  'scales': {
    'x': [{'gridLines': {'display': False}}],
    'y': [{'display': True, 'ticks': {'beginAtZero': True}}]
  },
  'responsive': True,
  'maintainAspectRatio': True,
}

class ResolutionGraph(ResolutionGraphTemplate):
  """This 'ResolutionGraph' custom component accepts 'labels' and 'datasets' properties will take care of its own display.

  Component properties:
    labels: a list of dates in the form '%A, %d'
    datasets: list of data in the form:
              [{
                    'label': 'Resolved',
                    'backgroundColor': '#9389DF',
                    'borderColor': '#7D71D8',
                    'data': list of data e.g [1,0,1,2,3,4,5]
                },{
                    'label': 'Unresolved',
                    'backgroundColor': '#00FFAF',
                    'borderColor': '#00FFAF',
                    'data': list of data e.g [1,0,1,2,3,4,5]
                }]
  """

  def __init__(self, **properties):
    self._props = properties
    ctx = self.dom_nodes["chart"].getContext('2d')
    self.chart = Chart(ctx, {'type': 'line', 'options': options})
    self.init_components(**properties)

  def update_chart(self, *args, **kws):
    self.chart.data = {'labels': self.labels, 'datasets': self.datasets}
    self.chart.update()

  labels = Properties.property_with_callback(update_chart)
  datasets = Properties.property_with_callback(update_chart)
