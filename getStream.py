#!/usr/bin/env python3
import sys
import logging

import gi

gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gst', '1.0')

from gi.repository import Gst, GObject, GLib

logging.basicConfig(level=logging.DEBUG, format="[%(name)s] [%(levelname)8s] - %(message)s")
logger = logging.getLogger(__name__)

def main(argv):
    pipeline = None
    bus = None
    message = None

    default_url = 'https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm'

    if (len(argv) >= 1):

        uri = argv[0]
    else:
        uri = default_url

    # initialize GStreamer
    Gst.init(argv)

    # build the pipeline
    pipeline = Gst.parse_launch(
        f"playbin uri={uri}"
    )

    # start playing
    pipeline.set_state(Gst.State.PLAYING)

    # wait until EOS or error
    bus = pipeline.get_bus()
    msg = bus.timed_pop_filtered(
        Gst.CLOCK_TIME_NONE,
        Gst.MessageType.ERROR | Gst.MessageType.EOS
    )

    # free resources
    pipeline.set_state(Gst.State.NULL)
    ret = pipeline.set_state(Gst.State.PLAYING)
    if ret == Gst.StateChangeReturn.FAILURE:
        logger.error("Unable to set the pipeline to the playing state.")
        sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])