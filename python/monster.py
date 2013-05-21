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

TIME_TO_DISAPPEAR = 2.0  # Seconds
TIME_TO_DODGE = 0.7


class Monster(bge.types.BL_ArmatureObject):
    """ Base class for all monsters like zombies
    """

    def __init__(self, old):
        """
        """
        print("Converted to monster")
        self['health'] = 5
        self.is_alive = True
        self.attacked = False
        self.is_near_good_guy = False

    def update(self):
        if self['health'] <= 0:
            if self.is_alive:
                self.die()
            self.is_alive = False
            if self['disappear'] > TIME_TO_DISAPPEAR:
                self.endObject()
            return

        if self.localLinearVelocity[1] < -0.01:
            self.playAction('walk2', 0.0, 41.0, 0, 2, 0, bge.logic.KX_ACTION_MODE_LOOP)


    def near_good_guy(self, controller):
        if self.is_alive:
            self.playAction('attack3', 0.0, 40.0, 0, 1, 0.5)
            if self.getActionFrame() == 0:
                self['time_near'] = 0.0
                self.attacked = False

        if self['time_near'] >= TIME_TO_DODGE and not self.attacked:
            self.attacked = True
            print("attacked")
            self['time_near'] = 0
            sensor_attack_distance = controller.sensors['attack_distance']
            target = sensor_attack_distance.hitObject
            target['health'] -= 1

    def see_good_guy(self, controller):
        if self.is_alive:
            # self.setLinearVelocity([0, -4.0, 0], True)
            # if not self.is_near_good_guy:
            controller.activate(self.actuators['face_good_guy'])
            # else:
            #     controller.deactivate(self.actuators['face_good_guy'])

    def die(self):
        self.playAction('dead1', 0.0, 40.0, 0, 0)
        self['disappear'] = 0.0
        # self.suspendDynamics()
        # self.setOcclusion(False, True)
        # self.disableRigidBody()
        # res = self.reinstancePhysicsMesh("no_collision_object", None)
        # if not res:
        #     print("Failed to reinstance physics mesh")
        # self.setParent('no_collision_object', False, True)


        # self.replaceMesh("no_collision_object", False, True)

def convert_to_monster(controller):
    old = controller.owner
    mutated = Monster(old)

    assert(old is not mutated)
    assert(old.invalid)
    assert(mutated is controller.owner)

def update(controller):
    controller.owner.update()

def near_good_guy(controller):
    controller.owner.near_good_guy(controller)

def see_good_guy(controller):
    controller.owner.see_good_guy(controller)
