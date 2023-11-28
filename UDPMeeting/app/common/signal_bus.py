# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ Signal bus """

    switchToSampleCard = pyqtSignal(str, int)
    supportSignal = pyqtSignal()
    sdLaunchSignal = pyqtSignal(int)


signalBus = SignalBus()