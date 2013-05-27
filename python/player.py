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
from python import text, effect


class Player(bge.types.BL_ArmatureObject):
    def __init__(self, old):
        self.health = self['health']
        self.blood_effects = []
        self.gun = None
        self.character = bge.constraints.getCharacter(self)
        self.key_status = {
            'forward': False
            , 'backward': False
            , 'left': False
            , 'right': False
            , 'jump': False
        }

    def update(self, controller):
        if self['health'] <= 0:
            controller.deactivate(self.actuators['movement'])
            return
        if self['time_since_hit'] > 0.4 and self['blood_active']:
            scene = bge.logic.getCurrentScene()
            scene.post_draw.remove(self.blood_effects.pop())
            if not self.blood_effects:
                self['blood_active'] = False

        key_status = self.key_status
        dy = 0.0
        if key_status['forward']:
            dy -= self['speed_forward']
        if key_status['backward']:
            dy += self['speed_backward']

        dx = 0.0
        if key_status['left']:
            dx += self['speed_strafe']
        if key_status['right']:
            dx -= self['speed_strafe']

        act_motion = self.actuators['movement']
        act_motion.dLoc = [dx, dy, 0]
        act_motion.useLocalDLoc = True
        controller.activate(act_motion)

        if key_status['jump']:
            self.character.jump()

    def message(self, controller):
        sensor = controller.sensors['message']
        subjects = sensor.subjects

        for i in range(len(subjects)):
            subject = subjects[i]
            body = sensor.bodies[i]
            if subject in self.key_status.keys():
                if body == 'stop':
                    self.key_status[subject] = False
                else:
                    self.key_status[subject] = True

    def health_changed(self, controller):
        sensor = controller.sensors['property_changed']

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


def update(controller):
    controller.owner.update(controller)


def message(controller):
    controller.owner.message(controller)


def health_changed(controller):
    controller.owner.health_changed(controller)
