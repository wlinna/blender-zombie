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
        scene = bge.logic.getCurrentScene()
        self.gun_pos = self.childrenRecursive['gun_pos']
        # FIXME: Get gun somewhere else. This is semi dangerous
        self.weapon = scene.objects['pistol']
        self.take_weapon(self.weapon)
        self.character = bge.constraints.getCharacter(self)
        self.clips_pistol = [self.weapon['clip_size']] * 4  # Temporary solution
        print(self.clips_pistol)
        self.input_status = {
            'forward': False
            , 'backward': False
            , 'left': False
            , 'right': False
            , 'jump': False
            , 'shoot': False
            , 'reload': False
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

        input_status = self.input_status
        dy = 0.0
        if input_status['forward']:
            dy -= self['speed_forward']
        if input_status['backward']:
            dy += self['speed_backward']

        dx = 0.0
        if input_status['left']:
            dx += self['speed_strafe']
        if input_status['right']:
            dx -= self['speed_strafe']

        act_motion = self.actuators['movement']
        act_motion.dLoc = [dx, dy, 0]
        act_motion.useLocalDLoc = True
        controller.activate(act_motion)

        if input_status['jump']:
            self.character.jump()


        if input_status['reload']:
            self.try_reload()
        if input_status['shoot']:
            conditions = bool(self.weapon) \
                         and self.clips_pistol \
                         and self.clips_pistol[0] > 0

            if conditions:
                self.sendMessage('shoot', '', self.weapon.name)

    def message(self, controller):
        sensor = controller.sensors['message']
        subjects = sensor.subjects

        for i in range(len(subjects)):
            subject = subjects[i]
            body = sensor.bodies[i]
            if subject in self.input_status.keys():
                if body == 'stop':
                    self.input_status[subject] = False
                else:
                    self.input_status[subject] = True

            if subject == 'shooting_succesful':
                self.clips_pistol[0] -= 1

            if subject == 'reload_successful':
                self.reload()

            if subject == 'throw' and body == '':
                self.throw_weapon()

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

    def try_reload(self):
        if not self.weapon:
            return
        if not self.clips_pistol:
            return
        if self.clips_pistol[0] == self.weapon['clip_size']:
            return

        if len(self.clips_pistol) == 1:
            return

        if self.weapon['timer_shoot'] < self.weapon['reload_delay']:
            return

        self.sendMessage('reload', '', self.weapon.name)


    def reload(self):
        old_clip = self.clips_pistol.pop(0)
        if old_clip > 0:
            self.clips_pistol.append(old_clip)

        print("Clips after reload:", self.clips_pistol)

    def take_weapon(self, weapon):
        # Save the old weapon somewhere
        self.weapon = weapon
        self.weapon.free = False
        weapon.setParent(self.gun_pos, False, True)
        weapon.localPosition = [0, 0, 0]
        forward = [0, -1, 0]
        up = [0, 0, 1]
        weapon.alignAxisToVect(forward, 1)
        weapon.alignAxisToVect(up, 2)

    def throw_weapon(self):
        if not self.weapon:
            return
        self.weapon.free = True
        self.weapon.localLinearVelocity = [0.0, -2.0, 0.0]
        scene = bge.logic.getCurrentScene()
        ground = scene.objects['ground']
        self.weapon.setParent(ground, False, False)
        self.weapon = None


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
