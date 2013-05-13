import bge

class Monster(bge.types.BL_ArmatureObject):
    """ Base class for all monsters like zombies
    """

    def __init__(self, old):
        """
        """
        pass

    def update(self):
        # FIXME: Remove this immediately when updating works
        print("Updating monster")

def convert_to_zombie(controller):
    old = controller.owner
    mutated = Monster(old)

    assert(old is not mutated)
    assert(old.invalid)
    assert(mutated is controller.owner)

def update(controller):
    controller.owner.update()
