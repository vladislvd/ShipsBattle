import pyglet
from application import Application


def main():
    pyglet.font.add_file('config/AGENCYR.TTF')
    game = Application()
    pyglet.app.run()


if __name__ == "__main__":
    main()
