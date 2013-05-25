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
        pass

    def reload(self):

        # This will be used. DO NOT REMOVE
        # if not self.clips:
        #     print("No clips left")
        #     return
        # old_clip = self.clips.pop(0)

        bullets = self['bullets']
        clips = self['clips']
        clip_size = self['clip_size']
        delay = self['reload_delay']

        if self['timer_shoot'] < self['delay']:
            return
        if bullets < clip_size:
            if clips > 0:
                self['bullets'] = clip_size
                self['clips'] -= 1
                self['timer_shoot'] = 0.0

    def try_to_shoot(self, controller):
        if self['bullets'] <= 0:
            # TODO: Play empty clip sound
            return

        if self['timer_shoot'] < self['delay']:
            return

        self.shoot(controller)

    def shoot(self, controller):
        scene = bge.logic.getCurrentScene()
        ray = controller.sensors['gun_ray']
        # THIS WILL REPLACE bullets-property
        # self.clips[0] -= 1
        self['bullets'] -= 1  # This will be removed after migration is ready
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
    fire_object.setParent(point_gun_fire_obj, False, True)

    act_sound = obj.actuators['sound']
    act_sound.mode = 1
    act_sound.startSound()
