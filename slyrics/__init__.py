import argparse
import signal
import sys
import threading
import time

from slyrics.gui import SlyricsUI
from slyrics.spotify import SpotifyWebClient, SpotifyBusClient
from slyrics.util import die
from slyrics.version import __version__
import slyrics.scrapers as scrapers

def loop(ui):
    client = None
    def find():
        client = SpotifyWebClient()
        try:
            client.find()
        except Exception as e:
            pass  # try a different client
        else:
            print("found spotify on port {0}".format(client.get_port()))
            return client

        client = SpotifyBusClient()
        try:
            client.find()
        except Exception as e:
            return None
        else:
            print("found spotify on dbus")
        return client

    status = None
    def update():
        try:
            _status = client.get_status()
        except Exception as e:
            print("error retrieving status: {0}".format(e))
            return status  # reuse the old status, if an error ocurred
        if (not _status) ^ (not status):
            ui.on_connection_status_change(_status is not None)
        if not _status:
            return None
        if _status != status:
            ui.on_status_change(_status)
            lyrics = None
            try:
                lyrics = scrapers.find(_status.get_track_name(), _status.get_track_artist())
            except:
                pass
            ui.on_lyrics_change(lyrics)
        return _status

    while True:
        if client is None or not client:
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
    #parser.add_argument("--host", dest="host", help="the host to scan")
    #parser.add_argument("--port", dest="port", type=int, default=-1,
    #                    help="instead of scanning, use this port")
    parser.add_argument("--version", dest="version", action="store_true", default=False,
                        help="print version")
    #parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
    #                    help="be verbose")
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
