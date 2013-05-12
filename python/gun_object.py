
class Gun(object):
    """
    """

    def __init__(self, name, damage, clipsize, delay, reaload_delay):
        """

        Arguments:
        - `delay`:
        - `damage`:
        - `clipsize`:
        - `reaload_delay`:
        """
        self.name = name
        self.damage = damage
        self.clipsize = clipsize
        self.delay = delay
        self.reaload_delay = reaload_delay
