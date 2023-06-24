#!/usr/bin/env python
'''
KViewer
=======

KViewer, for KV-Viewer, is a simple tool allowing you to dynamically display
a KV file, taking its changes into account (thanks to watchdog). The
idea is to facilitate design using the KV language. It's somewhat related to
the KivyCatalog demo, except it uses an on-disc file, allowing the user to use
any editor.

You can use the script as follows::

    python kviewer.py ./test.kv

This will display the test.kv and automatically update the display when the
file changes.

.. note: This scripts uses watchdog to listen for file changes. To install
   watchdog::

   pip install watchdog

'''

from sys import argv
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock, mainthread

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from os.path import dirname, basename
import os

from libs.uix.root import Root

from dotenv import load_dotenv
load_dotenv()

if len(argv) != 2:
    print('usage: %s filename.kv' % argv[0])
    exit(1)

init = 0

KVFILE = f"libs/uix/kv/{argv[1]}_screen.kv"
PATH = dirname(KVFILE)
TARGET = basename(KVFILE)
PAGE_NAME = argv[1]

class KvHandler(FileSystemEventHandler):
    def __init__(self, callback, target, **kwargs):
        super(KvHandler, self).__init__(**kwargs)
        self.callback = callback
        self.target = target

    def on_any_event(self, event):
        if basename(event.src_path) == self.target:
            self.callback()


class KvViewerApp(MDApp):
    def build(self):
        o = Observer()
        o.schedule(KvHandler(self.update, TARGET), PATH)
        o.start()
        Clock.schedule_once(self.update, 1)
        # return super(KvViewerApp, self).build()
        self.root = Root()
        self.root.set_current(PAGE_NAME)

    @mainthread
    def update(self, *args):
        print("update")
        global init
        if init > 0:
            self.root.set_current(PAGE_NAME, reload=True)
        init = init + 1


if __name__ == '__main__':
    Window.maximize()
    resolution = Window.system_size
    screen_preview_w = int(os.environ.get("SCREEN_PREVIEW_W", 400))
    screen_preview_h = int(os.environ.get("SCRREN_PREVIEW_H", 800))
    window_pos_top = int(os.environ.get("WINDOW_POS_TOP", 0))
    window_pos_left = int(os.environ.get("WINDOW_POS_LEFT", 400))
    Window.size = (screen_preview_w, screen_preview_h)
    Window.top = window_pos_top
    Window.left = resolution[0] - window_pos_left

    KvViewerApp().run()