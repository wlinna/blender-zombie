import bge

class Gun(bge.types.KX_GameObject):
    """
    """

    def __init__(self, old):
        """
        - `old`: old is the original object. You may not reference to it but
        it's useful for reading properties
        """
        self.rate_fire = 0.3
        self.time_reload = 1.0  # How long it takes to reload
        self.bullets = 12
        self.clips = 4
        self.fire_fx_size_max = 0.5
        self.fire_fx_y = 0
        self.fire_fx_x = 0
        self.fire_fx_z = 0
        # This is useful for saving bullets when reloading
        # clip that is not empty
        self.total_bullets_left = self.bullets * self.clips


    def update(self):
        # FIXME: Remove this immediately when updating works
        print("Updating gun")


def convert_to_gun(controller):
    old = controller.owner
    mutated = Gun(old)

    assert(old is not mutated)
    assert(old.invalid)
    assert(mutated is controller.owner)

def update(controller):
    controller.owner.update()
