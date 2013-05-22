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


import bgl
import bge


def blood_screen():
    scene = bge.logic.getCurrentScene()
    def fx():
        width = bge.render.getWindowWidth()
        height = bge.render.getWindowHeight()

        bgl.glMatrixMode(bgl.GL_PROJECTION)
        bgl.glLoadIdentity()
        bgl.gluOrtho2D(0, width, 0, height)
        bgl.glMatrixMode(bgl.GL_MODELVIEW)
        bgl.glLoadIdentity()


        bgl.glEnable(bgl.GL_BLEND)
        bgl.glColor4f(0.8, 0.0, 0.0, 0.4)
        # bgl.glRecti(0, 0, width, height)
        bgl.glBegin(bgl.GL_QUADS)
        bgl.glVertex2i(0, 0)
        bgl.glVertex2i(width, 0)
        bgl.glVertex2i(width, height)
        bgl.glVertex2i(0, height)

        # bgl.glVertex2f(0.0, 0.0)
        # bgl.glVertex2f(1.0, 0.0)
        # bgl.glVertex2f(1.0, 1.0)
        # bgl.glVertex2f(0.0, 1.0)



        bgl.glEnd()
        bgl.glDisable(bgl.GL_BLEND)
    scene.post_draw.append(fx)
    return fx
