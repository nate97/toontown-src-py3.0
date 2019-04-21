from direct.task.Task import Task
import random

from toontown.town import Street


class BRStreet(Street.Street):
    def enter(self, requestStatus):
        Street.Street.enter(self, requestStatus)

    def exit(self):
        Street.Street.exit(self)
