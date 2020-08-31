import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject
import threading
import signal
import time
import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self, i=0):
        obj = pipeline.videosrc
        if int(i) == 1:
            obj.set_property("pattern", "ball")
        else:
            obj.set_property("pattern", "snow")

def change_pattern():
    time.sleep(1)
    obj = pipeline.videosrc
    obj.set_property("pattern", "ball")

class MainPipeline():
    def __init__(self):
        self.pipeline = None
        self.videosrc = None
        self.videosink = None

    
    def gst_thread(self):
        print("Initializing GST Elements")
        Gst.init(None)

        self.pipeline = Gst.Pipeline.new("hello")

        # instantiate the camera source
        self.videosrc = Gst.ElementFactory.make("videotestsrc", "test")
        self.videosrc.set_property("pattern", "snow")

        # instantiate the appsink - allows access to raw frame data
        self.videosink = Gst.ElementFactory.make("autovideosink", "vid-sink")
        
        # add all the new elements to the pipeline
        print("Adding Elements to Pipeline")
        self.pipeline.add(self.videosrc)
        self.pipeline.add(self.videosink)

        self.videosrc.link(self.videosink)
        # link the elements in order, adding a filter to ensure correct size and framerate
        # print("Linking GST Elements")
        # self.videosrc.link_filtered(self.videoparse,
        #     Gst.caps_from_string('image/jpeg,width=640,height=480,framerate=30/1'))
        # self.videoparse.link(self.videosink)

        # start the video
        print("Setting Pipeline State")
        self.pipeline.set_state(Gst.State.PAUSED)
        self.pipeline.set_state(Gst.State.PLAYING)

def signal_handler(signum, frame):
    print("Interrupt caught")

if __name__ == "__main__":
    pipeline = MainPipeline()
    gst_thread = threading.Thread(target=pipeline.gst_thread)
    gst_thread.start()

    # gst_thread = threading.Thread(target=change_pattern)
    # gst_thread.setDaemon(True)
    # gst_thread.start()
    cherrypy.quickstart(HelloWorld())

    print("registering sigint")
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
