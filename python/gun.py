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

import random
import bge


GUN_FIRE_SCALE_RANGE = (0.0, 0.38)


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
        self.free = True

    def message(self, controller):
        sensor = controller.sensors['message']
        subjects = sensor.subjects
        bodies = sensor.bodies

        if not subjects: return

        for i in range(len(subjects)):
            subject = subjects[i]
            body = bodies[i]

            if subject == 'shoot' and body == '':
                self.try_to_shoot(controller)

            if subject == 'reload' and body == '':
                self.reload()

    def update(self):
        if self.free:
            self.applyForce(bge.logic.getCurrentScene().gravity)

    def reload(self):
        self['timer_shoot'] = 0.0
        # TODO: Do animation first, then reload
        self.sendMessage('reload_successful', '', 'player')

    def try_to_shoot(self, controller):
        if self['timer_shoot'] < self['delay']:
            return

        self.shoot(controller)

    def shoot(self, controller):
        scene = bge.logic.getCurrentScene()
        ray = controller.sensors['gun_ray']
        self.sendMessage('shooting_succesful', '', 'player')
        self['timer_shoot'] = 0.0

        fx_object = scene.addObject("fx_gun_shot", self, 60)
        fx_object.setParent(self, False, True)

        if ray.positive:
            target = ray.hitObject
            if 'health' in target:
                target['health'] -= 1


def convert_to_gun(controller):
    old = controller.owner
    mutated = Gun(old)

    assert(old is not mutated)
    assert(old.invalid)
    assert(mutated is controller.owner)


def update(controller):
    controller.owner.update()


def message(controller):
    controller.owner.message(controller)


def ctrl_fx_shot(controller):
    obj = controller.owner
    scene = bge.logic.getCurrentScene()

    point_gun_fire_obj = obj.parent.childrenRecursive['point_gun_fire']
    fire_object = scene.addObject("gun_fire", "point_gun_fire", 1)
    scale = random.uniform(GUN_FIRE_SCALE_RANGE[0], GUN_FIRE_SCALE_RANGE[1])
    fire_object.localScale = [scale, scale, scale]
    fire_object.setParent(point_gun_fire_obj, False, True)

    act_sound = obj.actuators['sound']
    act_sound.mode = 1
    act_sound.startSound()
