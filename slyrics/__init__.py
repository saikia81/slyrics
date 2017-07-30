import argparse
import signal
import sys
import threading
import time

from slyrics.gui import SlyricsUI
from slyrics.spotify import SpotifyClient
from slyrics.util import die
from slyrics.version import __version__
import slyrics.scrapers as scrapers

def loop(ui):
    client = None
    def find():
        client = SpotifyClient()
        try:
            client.find()
        except Exception as e:
            return None
        print("found spotify on port {0}".format(client.get_port()))
        return client

    status = None
    def update():
        try:
            temp = client.get_status()
        except Exception as e:
            print("error retrieving status: {0}".format(e))
            temp = None
        if (not temp) ^ (not status):
            ui.on_connection_status_change(temp is not None)
        if not temp:
            return None
        if temp != status:
            ui.on_status_change(temp)
            lyrics = None
            try:
                lyrics = scrapers.find(temp.get_track_name(), temp.get_track_artist())
            except:
                pass
            ui.on_lyrics_change(lyrics)
        return temp

    while True:
        if not client:
            client = find()
            continue
        status = update()
        if not status:
            print("finding spotify...")
            client = None
            continue
        time.sleep(0.5)

def main():
    parser = argparse.ArgumentParser(description="An external lyrics addon for Spotify")
    parser.add_argument("--host", dest="host", help="the host to scan")
    parser.add_argument("--port", dest="port", type=int, default=-1,
                        help="instead of scanning, use this port")
    parser.add_argument("--version", dest="version", action="store_true", default=False,
                        help="print version")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
                        help="be verbose")
    args = parser.parse_args(sys.argv[1:])

    if args.version:
        die("slyrics {0}".format(__version__))

    # todo: find a way to fix this
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    ui = SlyricsUI()
    thread = threading.Thread(target=loop, args=(ui,))
    thread.daemon = True
    thread.start()
    ui.start()
