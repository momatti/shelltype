from _curses import window

class StartHeader:
  """Header for the start menu interface."""
  def __init__(self, window: window):
    self.window = window
    self.height, self.width = window.getmaxyx()

    self.title = "TERMINAL TYPING SESSION"

  def draw(self):
    if (self.width - len(self.title)) // 2 > 0 and 3 < self.height:
      self.window.addstr(3, (self.width - len(self.title)) // 2, self.title)
