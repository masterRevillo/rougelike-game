class Impossible(Exception):
    """exception raised when an action is impossible to perform
    the reason is given as the exception message
    """

class QuitWithoutSaving(SystemExit):
    """can be raised to exit the game without auto saving"""