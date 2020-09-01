import traceback
import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject  # noqa:F401,F402


# Initializes Gstreamer, it's variables, paths
Gst.init(sys.argv)


def on_message(bus: Gst.Bus, message: Gst.Message, loop: GObject.MainLoop):
    mtype = message.type
    """
        Gstreamer Message Types and how to parse
        https://lazka.github.io/pgi-docs/Gst-1.0/flags.html#Gst.MessageType
    """
    if mtype == Gst.MessageType.EOS:
        print("End of stream")
        loop.quit()

    elif mtype == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(err, debug)
        loop.quit()
    elif mtype == Gst.MessageType.WARNING:
        err, debug = message.parse_warning()
        print(err, debug)
    elif mtype == Gst.MessageType.STATE_CHANGED:
        print(message.parse_state_changed())
    else:
        print(mtype)
    return True

def on_status_changed(bus, message):
        print('status_changed message -> {}'.format(message))

def on_eos(bus, message):
    print('eos message -> {}'.format(message))

def on_info(bus, message):
    print('info message -> {}'.format(message))

def on_error(bus, message):
    print('error message -> {}'.format(message.parse_error()))


# Gst.Pipeline https://lazka.github.io/pgi-docs/Gst-1.0/classes/Pipeline.html
pipe="v4l2src device=/dev/video2 ! videoconvert ! autovideosink"
pipeline = Gst.parse_launch(pipe)



# https://lazka.github.io/pgi-docs/Gst-1.0/classes/Bus.html
bus = pipeline.get_bus()

# allow bus to emit messages to main thread
bus.add_signal_watch()
bus.connect('message::error', on_error)
bus.connect('message::state-changed', on_status_changed)
bus.connect('message::eos', on_eos)
bus.connect('message::info', on_info)
bus.enable_sync_message_emission()
# bus.connect('sync-message::element', set_frame_handle)

# Start pipeline
pipeline.set_state(Gst.State.PLAYING)

# Init GObject loop to handle Gstreamer Bus Events


loop = GObject.MainLoop()
# bus.connect("message", on_message, loop)
# Add handler to specific signal
# https://lazka.github.io/pgi-docs/GObject-2.0/classes/Object.html#GObject.Object.connect


try:
    loop.run()
except Exception:
    traceback.print_exc()
    loop.quit()

# Stop Pipeline
pipeline.set_state(Gst.State.NULL)
del pipeline


# SUBSYSTEM=="usb", KERNEL=="3-4", ATTR{idVendor}=="045e", ATTR{idProduct}=="0779", SYMLINK+="foo/video10"