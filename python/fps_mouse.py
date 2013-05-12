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

SENSITIVY = 0.0005

def ctrl_fps_cam(controller):
    """
    """
    obj = controller.owner
    move = calculate_mouse_move(controller, obj)
    use_mouse_look(controller, move)
    center_cursor(controller)


def get_window_dimensions():
    width = bge.render.getWindowWidth()
    height = bge.render.getWindowHeight()

    return width, height


def calculate_mouse_move(controller, obj):
    mouse = controller.sensors['mouse_look']

    width, height = get_window_dimensions()

    x = width / 2 - mouse.position[0]
    y = height / 2 - mouse.position[1]

    if not 'mouse_init' in obj:
        obj['mouse_init'] = True
        x = 0
        y = 0

    if not mouse.positive:
        x = 0
        y = 0

    return x, y


def use_mouse_look(controller, move):

    up_down = move[1] * SENSITIVY
    left_right = move[0] * SENSITIVY

    act_left_right, act_up_down = get_actuators(controller)

    act_left_right.dRot = [0.0, 0.0, left_right]
    act_left_right.useLocalDRot = True

    act_up_down.dRot = [up_down, 0.0, 0.0]
    act_up_down.useLocalDRot = True

    controller.activate(act_left_right)
    controller.activate(act_up_down)

def center_cursor(controller):

    width, height = get_window_dimensions()
    mouse = controller.sensors['mouse_look']
    pos = mouse.position

    if pos != [int(width / 2), int(height / 2)]:
        bge.render.setMousePosition(int(width / 2), int(height / 2))
    else:
        act_left_right, act_up_down = get_actuators(controller)

        controller.deactivate(act_left_right)
        controller.deactivate(act_up_down)

def get_actuators(controller):
    act_left_right = controller.actuators['left_right']
    act_up_down = controller.actuators['up_down']

    return act_left_right, act_up_down
