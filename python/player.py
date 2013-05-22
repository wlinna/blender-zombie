import bge
from python import text, effect


def message(controller):
    obj = controller.owner
    sensor = controller.sensors['message']
    subjects = sensor.subjects


    if not subjects:
        return

    subject = subjects[0]
    body = sensor.bodies[0]

    if subject == 'jump':
        act = obj.actuators[subject]
        if sensor.bodies[0] == 'stop':
            controller.deactivate(act)
        else:
            controller.activate(act)

    if subject == 'forward':
        act = obj.actuators[subject]
        if sensor.bodies[0] == 'stop':
            controller.deactivate(act)
        else:
            controller.activate(act)

    if subject == 'left':
        act = obj.actuators[subject]
        if sensor.bodies[0] == 'stop':
            controller.deactivate(act)
        else:
            controller.activate(act)

    if subject == 'backward':
        act = obj.actuators[subject]
        if sensor.bodies[0] == 'stop':
            controller.deactivate(act)
        else:
            controller.activate(act)

    if subject == 'right':
        act = obj.actuators[subject]
        if sensor.bodies[0] == 'stop':
            controller.deactivate(act)
        else:
            controller.activate(act)


def health_changed(controller):
    sensor = controller.sensors['property_changed']
    print(sensor.propName)

    if sensor.propName == "health":
        obj = controller.owner
        health = obj['health']
        scene = bge.logic.getCurrentScene()
        fx = effect.blood_screen()
        print(obj['time_since_hit'])

        obj['blood_active'] = True
        obj['time_since_hit'] = 0.0
        # controller.activate(controller.actuators['hit_effect'])
        if health <= 0:
            text_obj = text.TextObject("Dead", 0.5, 0.5, 100, 0)
            text.text_objects.append(text_obj)

def update(controller):
    obj = controller.owner
    if obj['time_since_hit'] > 0.4 and obj['blood_active']:
        scene = bge.logic.getCurrentScene()
        # FIXME: Make update remove the correct effect, not just last one
        scene.post_draw.pop()
        print("Removed effect")
        if not scene.post_draw:
            obj['blood_active'] = False
