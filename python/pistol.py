# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bge

## Shooting code starts here

def message(controller):
    obj = controller.owner
    sensor = controller.sensors['message']
    subjects = sensor.subjects

    if not subjects: return

    subject = subjects[0]
    body = sensor.bodies[0]

    if subject == 'shoot' and body == '':
        # act = obj.actuators[subject]
        # if sensor.bodies[0] == 'stop':
            # controller.deactivate(act)
        # else:
            # controller.activate(act)
        try_to_shoot(controller)

    if subject == 'reload' and body == '':
        # act = obj.actuators[subject]
        # if sensor.bodies[0] == 'stop':
        #     controller.deactivate(act)
        # else:
        #     controller.activate(act)
        reload_gun(controller)


def try_to_shoot(controller):
    obj = controller.owner
    # key = controller.sensors['mouse_lb']

    # if not key.positive:
    #     return
    if obj['bullets'] <= 0:
        return

    if obj['timer_shoot'] < obj['delay']:
        return

    shoot(obj, controller)


def shoot(obj, controller):
    scene = bge.logic.getCurrentScene()
    ray = controller.sensors['gun_ray']
    delay = obj['delay']

    # controller.activate(act_shoot)
    fx_object = scene.addObject("fx_gun_shot", obj, 60)

    fx_object.setParent(obj, False, True) # compound=False, Ghost=True
    obj['bullets'] -= 1
    obj['timer_shoot'] = 0.0
    if ray.positive:
        target = ray.hitObject

        if "health" in target:
            target["health"] -= 1
            # if target["health"] <= 0:
            #     target.endObject()

## Shooting effect code starts here

def ctrl_fx_shot(controller):
    obj = controller.owner
    scene = bge.logic.getCurrentScene()

    point_gun_fire_obj = obj.parent.childrenRecursive['point_gun_fire']
    fire_object = scene.addObject("gun_fire", "point_gun_fire", 1)
    fire_object.setParent(point_gun_fire_obj, False, True)

    act_sound = obj.actuators['sound']
    act_sound.mode = 1
    act_sound.startSound()

## Reloading code starts here


def reload_gun(controller):
    obj = controller.owner
    bullets = obj['bullets']
    clips = obj['clips']
    clip_size = obj['clip_size']
    delay = obj['reload_delay']

    if obj['timer_shoot'] < obj['delay']:
        return
    if bullets < clip_size:
        if clips > 0:
            obj['bullets'] = clip_size
            obj['clips'] -= 1
            obj['timer_shoot'] = 0.0
