#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from glumpy import app, gl, gloo
from glumpy.app import clock

def main():

    vertex = """
    attribute vec2 position;
    void main (void)
    {
        gl_Position = vec4(position, 0.0, 1.0);
    }
    """
    
    fragment = open('/tmp/tt.fs').read()

    app.use('glfw')
    
    window = app.Window(width=640, height=480)
    
    @window.event
    def on_draw(dt):
        quad['time']+=dt*.5
        window.clear()
        quad.draw(gl.GL_TRIANGLE_STRIP)
        title ='FPS:%f' % (clock.get_fps())
        window.set_title(title)

    quad = gloo.Program(vertex, fragment, count=4)
    quad['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
    quad['resolution'] = [window.width, window.height]
    quad['time']=0
    app.run()

if __name__ == '__main__':
  # some initialization code
  reload(sys)
  sys.setdefaultencoding('utf8')

  main()

