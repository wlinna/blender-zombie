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

class Monster(bge.types.BL_ArmatureObject):
    """ Base class for all monsters like zombies
    """

    def __init__(self, old):
        """
        """
        print("Converted to monster")
        self['health'] = 5
        self.is_alive = True

    def update(self):
        if self['health'] <= 0:
            if self.is_alive:
                self.die()
            self.is_alive = False
            if self['disappear'] > TIME_TO_DISAPPEAR:
                self.endObject()


    def near_good_guy(self, controller):
        if self.is_alive:
            self.playAction('attack3', 0.0, 40.0)

    def see_good_guy(self, controller):
        if self.is_alive:
            self.playAction('walk2', 0.0, 41.0)

    def die(self):
        self.playAction('dead1', 0.0, 40.0)
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
