import pyglet

#pyglet.options['audio'] = ('openal', 'silent')
player = pyglet.media.Player()


window = pyglet.window.Window()

music = pyglet.media.load('E:\\m\\a.mp3')
player.volume=1
player.queue(music)
player.play()


pyglet.app.run()
