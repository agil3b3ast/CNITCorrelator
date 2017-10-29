class WindowHelper(object):

    def __init__(self, ctx):
        self._ctx = ctx

    def checkCorrelationWindow(self):
        pass

class WindowHolder(object):

    def __init__(self):
        self._windowHelpers = []

    def getWindowHelpers(self):
        return self._windowHelpers()

    def addWindowHelper(self, window_helper):
        self._windowHelpers.append(window_helper)
