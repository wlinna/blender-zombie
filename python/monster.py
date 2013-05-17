import bge

class Monster(bge.types.BL_ArmatureObject):
    """ Base class for all monsters like zombies
    """

    def __init__(self, old):
        """
        """
        print("Converted to monster")
        self['health'] = 5
        self.is_alive = True

    def update(self):
        if self['health'] <= 0:
            if self.is_alive:
                self.die()
            self.is_alive = False


    def near_good_guy(self, controller):
        if self.is_alive:
            self.playAction('attack3', 0.0, 40.0)

    def die(self):
        self.playAction('dead1', 0.0, 40.0)


def convert_to_monster(controller):
    old = controller.owner
    mutated = Monster(old)

    assert(old is not mutated)
    assert(old.invalid)
    assert(mutated is controller.owner)

def update(controller):
    controller.owner.update()

def near_good_guy(controller):
    controller.owner.near_good_guy(controller)
