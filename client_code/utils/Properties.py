from anvil import *
from anvil.property_utils import set_element_spacing

class CustomProperty(property):
  def __set_name__(self, owner, name):
    self._name = name

def theme_color_to_css(color:str):
  if color.startswith('theme:'):
    color = color.lstrip('theme:')
    return app.theme_colors[color]
  else:
    return color

#REUSABLE PROPERTIES
def property_with_callback(cb):
  def getter(self):
    return self._props.get(prop._name)
  def setter(self, value):
    self._props[prop._name] = value
    cb(self, value)
  prop = CustomProperty(getter, setter)
  return prop
  
def basic_property():
  def getter(self):
    return self._props.get(prop._name)
  def setter(self, value):
    self._props[prop._name] = value
  prop = CustomProperty(getter, setter)
  return prop

def style_property(dom_node_name, style_prop):
  def set_style(self, value):
    self.dom_nodes[dom_node_name].style.setProperty(style_prop, value)
  return property_with_callback(set_style)

def align_property(dom_node_name):
  return style_property(dom_node_name, 'justify-content')

def innerText_property(dom_node_name):
  def set_innerText(self, value):
    self.dom_nodes[dom_node_name].innerText = value
  return property_with_callback(set_innerText)

def spacing_property(dom_node_name):
  def set_spacing(self, value):
    set_element_spacing(self.dom_nodes[dom_node_name], value)
  return property_with_callback(set_spacing)
