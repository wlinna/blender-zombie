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
import bgl
import blf

DPI = 72


class TextObject(object):
    def __init__(self, text, px, py, size, time=0):
        self.text = text
        self.px = px
        self.py = py
        self.size = size
        self.time = time


text_objects = []

def init(controller):
    font_path = bge.logic.expandPath('//fonts/DejaVuSans.ttf')
    bge.logic.font_id = blf.load(font_path)
    scene = bge.logic.getCurrentScene()
    scene.post_draw = [write]

def write():
    width = bge.render.getWindowWidth()
    height = bge.render.getWindowHeight()

    bgl.glMatrixMode(bgl.GL_PROJECTION)
    bgl.glLoadIdentity()
    bgl.gluOrtho2D(0, width, 0, height)
    bgl.glMatrixMode(bgl.GL_MODELVIEW)
    bgl.glLoadIdentity()

    font_id = bge.logic.font_id

    for text_obj in text_objects:
        blf.position(font_id, width * text_obj.px , height * text_obj.py, 0)
        blf.size(font_id, text_obj.size, DPI)
        blf.draw(font_id, text_obj.text)
