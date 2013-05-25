import bge

class Gun(bge.types.KX_GameObject):
    """
    """

    def __init__(self, old):
        """
        - `old`: old is the original object. You may not reference to it.
        """
        self.rate_fire = 0.3
        self.time_reload = 1.0  # How long it takes to reload
        self.clip_size = 12
        self.clips = [self.clip_size, self.clip_size, self.clip_size]
        self.fire_fx_size_max = 0.5


    def message(self, controller):
        sensor = controller.sensors['message']
        subjects = sensor.subjects

        if not subjects: return

        for i in range(len(subjects)):
            subject = subjects[i]
            body = subjects[i]

            if subject == 'shoot' and body == '':
                pass

    def update(self):
        pass

    def reload(self):
        if not self.clips:
            print("No clips left")
            return
        old_clip = self.clips.pop(0)

    def try_to_shoot(self, controller):
        if self['bullets'] <= 0:
            # TODO: Play empty clip sound
            return

        if self['timer_shoot'] < self['delay']:
            return

        self.shoot(controller)

    def shoot(self, controller):
        if self['tap_to_shoot']:
            pass

        scene = bge.logic.getCurrentScene()
        ray = controller.sensors['gun_ray']
        self['timer_shoot'] = 0.0



def convert_to_gun(controller):
    old = controller.owner
    mutated = Gun(old)

    assert(old is not mutated)
    assert(old.invalid)
    assert(mutated is controller.owner)

def update(controller):
    controller.owner.update()
