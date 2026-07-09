class _EventEmitter:
  def __init__(self):
    self.subscribers = {}

  def emit(self, event, **kws):
    callbacks = self.subscribers.get(event, [])
    for cb in callbacks:
      kws["event_name"] = event
      cb(**kws)

  def subscribe(self, event, callback):
    callbacks = self.subscribers.setdefault(event, [])
    callbacks.append(callback)

  def unsubscribe(self, event, callback):
    callbacks = self.subscribers.get(event, [])
    callbacks = [cb for cb in callbacks if cb != callback]
    self.subscribers[event] = callbacks

  def form_subscribe(self, form, event, callback):
    _shown = {'shown': False} # hack: non-local not supported
    def show(**event_args):
      if _shown['shown']:
        return
      _shown['shown'] = True
      self.subscribe(event, callback)
    
    def hide(**event_args):
      _shown['shown'] = False
      self.unsubscribe(event, callback)
      
    form.add_event_handler('show', show)
    form.add_event_handler('hide', hide)

emitter = _EventEmitter()
