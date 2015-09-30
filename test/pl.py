# play an MP3 music file using Python module pyglet
# download pyglet free from: http://www.pyglet.org/download.html
# (no GUI window/frame is created)
import pyglet
# pick an MP3 music file you have in the working folder
# otherwise use the full file path
# (also file names are case sensitive with pyglet)
music_file = "a.mp3"
music = pyglet.resource.media(music_file)
music.play()
pyglet.app.run()