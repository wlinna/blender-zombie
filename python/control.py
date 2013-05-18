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
import itertools

counter = itertools.count(0, 1)
EVT_JUMP = next(counter)
EVT_FORWARD = next(counter)
EVT_BACKWARD = next(counter)
EVT_LEFT = next(counter)
EVT_RIGHT = next(counter)
EVT_RELOAD = next(counter)

EVT_SHOOT = next(counter)

key_bindings = {bge.events.SPACEKEY: EVT_JUMP
                , bge.events.WKEY: EVT_FORWARD
                , bge.events.AKEY: EVT_LEFT
                , bge.events.SKEY: EVT_BACKWARD
                , bge.events.DKEY: EVT_RIGHT
                , bge.events.RKEY: EVT_RELOAD
           }

mouse_bindings = {bge.events.LEFTMOUSE: EVT_SHOOT}

def key_event(controller):
    sensor = controller.sensors['key']
    obj = controller.owner
    for key, status in sensor.events:
        event = key_bindings.get(key, -1)
        if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
            if event == EVT_FORWARD:
                obj.sendMessage('forward', '', 'player')
            if event == EVT_LEFT:
                obj.sendMessage('left', '', 'player')
            if event == EVT_BACKWARD:
                obj.sendMessage('backward', '', 'player')
            if event == EVT_RIGHT:
                obj.sendMessage('right', '', 'player')
            if event == EVT_JUMP:
                obj.sendMessage('jump', '', 'player')
            if event == EVT_RELOAD:
                obj.sendMessage('reload', '', 'pistol')

        elif status == bge.logic.KX_INPUT_JUST_RELEASED:
            if event == EVT_FORWARD:
                obj.sendMessage('forward', 'stop', 'player')
            if event == EVT_LEFT:
                obj.sendMessage('left', 'stop', 'player')
            if event == EVT_BACKWARD:
                obj.sendMessage('backward', 'stop', 'player')
            if event == EVT_RIGHT:
                obj.sendMessage('right', 'stop', 'player')
            if event == EVT_JUMP:
                obj.sendMessage('jump', 'stop', 'player')
            if event == EVT_RELOAD:
                obj.sendMessage('reload', 'stop', 'pistol')

def mouse_always(controller):
    # sensor = controller.sensor
    mouse = bge.logic.mouse
    events = mouse.events
    obj = controller.owner

    for key, status in events.items():
        event = mouse_bindings.get(key, -1)
        if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
            if event == EVT_SHOOT:
                obj.sendMessage('shoot', '', 'pistol')

        elif status == bge.logic.KX_INPUT_JUST_RELEASED:
            if event == EVT_SHOOT:
                obj.sendMessage('shoot', 'stop', 'pistol')
