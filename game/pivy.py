#!/usr/bin/python
# coding=utf-8

__author__ = 'Simon Charest'
__copyright__ = 'Copyright 2019, SLCIT inc.'
__credits__ = []
__email__ = 'simoncharest@gmail.com'
__license__ = 'GNU'
__maintainer__ = 'Simon Charest'
__project__ = 'Pivy'
__status__ = 'Developement'
__version__ = '1.0.0'

"""
Prerequisites:
    python -m pip install --upgrade pip wheel setuptools
    python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
    python -m pip install kivy.deps.gstreamer
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label


def main():
    BattleMenu().run()


class BattleMenu(App):
    def build(self):
        # Creating box layouts
        root = BoxLayout(orientation='vertical')
        top = BoxLayout(size_hint=(1, .67))
        status = BoxLayout(orientation='vertical', size_hint=(.33, 1))
        right = BoxLayout(orientation='vertical', size_hint=(.67, 1))
        commands = BoxLayout(orientation='vertical', size_hint=(1, .33))
        row1 = BoxLayout(size_hint=(1, .34))
        row2 = BoxLayout(size_hint=(1, .33))
        row3 = BoxLayout(size_hint=(1, .33))
        battle = BoxLayout(size_hint=(1, .67))
        # battle = FloatLayout(pos_hint={'x': .5, 'y': .5}, size_hint=(1, .67))
        bottom = BoxLayout(size_hint=(1, .33))

        # Status box
        name = Label(text='Solo')
        lv = Label(text='LV 1')
        hp = Label(text='HP 15')
        mp = Label(text='MP 5')
        gp = Label(text='G 125')
        xp = Label(text='E 0')
        status.add_widget(name)
        status.add_widget(lv)
        status.add_widget(hp)
        status.add_widget(mp)
        status.add_widget(gp)
        status.add_widget(xp)
        top.add_widget(status)
        top.add_widget(right)

        # Command box
        command = Label(text='Command')
        fight = Button(text='Fight', background_color=(255, 0, 0, 255))
        spell = Button(text='Spell')
        run = Button(text='Run')
        item = Button(text='Item')
        row1.add_widget(command)
        row2.add_widget(fight)
        row2.add_widget(spell)
        row3.add_widget(run)
        row3.add_widget(item)
        commands.add_widget(row1)
        commands.add_widget(row2)
        commands.add_widget(row3)
        right.add_widget(commands)

        # Battle box
        background = Image(source='../img/background.png', allow_stretch=True, keep_ratio=False)
        enemy = Image(source='../img/DQ_Slime.png')
        battle.add_widget(background)
        # battle.add_widget(enemy)
        right.add_widget(battle)

        # Message box
        message = Label(text='A Slime draws near!\nCommand?')
        bottom.add_widget(message)

        # Root box
        root.add_widget(top)
        root.add_widget(bottom)

        return root


if __name__ == '__main__':
    main()
