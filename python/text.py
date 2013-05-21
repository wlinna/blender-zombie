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
