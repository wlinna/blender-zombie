import bge
from python import text, effect


class Player(bge.types.BL_ArmatureObject):
    def __init__(self, old):
        self.health = self['health']
        self.blood_effects = []

    def update(self, controller):
        if self['time_since_hit'] > 0.4 and self['blood_active']:
            scene = bge.logic.getCurrentScene()
            # FIXME: Make update remove the correct effect, not just last one
            scene.post_draw.remove(self.blood_effects.pop())
            print("Removed effect")
            if not self.blood_effects:
                self['blood_active'] = False


    def message(self, controller):
        sensor = controller.sensors['message']
        subjects = sensor.subjects


        if not subjects:
            return

        print(subjects)
        for i in range(len(subjects)):
            subject = subjects[i]
            body = sensor.bodies[i]
            is_simple_motion = False
            local_linear_velocity = [0.0, 0.0, 0.0]
            if subject == 'jump':
                act = self.actuators[subject]
                if sensor.bodies[0] == 'stop':
                    controller.deactivate(act)
                else:
                    controller.activate(act)

            if subject == 'forward':
                is_simple_motion = True
                act = self.actuators[subject]
                if sensor.bodies[0] == 'stop':
                    controller.deactivate(act)
                else:
                    controller.activate(act)

            if subject == 'left':
                is_simple_motion = True
                act = self.actuators[subject]
                if sensor.bodies[0] == 'stop':
                    controller.deactivate(act)
                else:
                    controller.activate(act)

            if subject == 'backward':
                is_simple_motion = True
                act = self.actuators[subject]
                if sensor.bodies[0] == 'stop':
                    controller.deactivate(act)
                else:
                    controller.activate(act)

            if subject == 'right':
                is_simple_motion = True
                act = self.actuators[subject]
                if sensor.bodies[0] == 'stop':
                    controller.deactivate(act)
                else:
                    controller.activate(act)

        # if is_simple_motion:
        #     act = self.actuators['movement']
        #     act.useLocalLinV = True


    def health_changed(self, controller):
        sensor = controller.sensors['property_changed']
        print(sensor.propName)

        if sensor.propName == "health":
            obj = controller.owner
            health = obj['health']
            scene = bge.logic.getCurrentScene()

            # FIXME: Check if player got health or lost health
            # before showing blood effect
            fx = effect.blood_screen()
            self.blood_effects.append(fx)

            obj['blood_active'] = True
            obj['time_since_hit'] = 0.0
            # controller.activate(controller.actuators['hit_effect'])
            if health <= 0:
                text_obj = text.TextObject("Dead", 0.5, 0.5, 100, 0)
                text.text_objects.append(text_obj)



def convert_to_player(controller):
    old = controller.owner
    mutated = Player(old)

    assert(old is not mutated)
    assert(old.invalid)
    assert(mutated is controller.owner)
    print("Converted to player object")


def update(controller):
    controller.owner.update(controller)

def message(controller):
    controller.owner.message(controller)

def health_changed(controller):
    controller.owner.health_changed(controller)
