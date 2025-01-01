
from logging import Logger
from logging import getLogger

from pyimage2pdf.Preferences import Preferences


class PyImage2Pdf:
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._preferences: Preferences = Preferences()
