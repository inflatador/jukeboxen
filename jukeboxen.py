#!/usr/bin/env python3

# jukeboxen.py: given a band name, downloads song data from discogs and
# outputs a list of their songs in DNS hostname (RFC ???) format.
# Now you can name servers/containers/whatever after your favorite band's
# songs!

# Version: 0.0.1a
# Author: Brian King
# License: Apache 2.0

import discogs_client
# import keychain
import logging
import os
import plac

jb_logger = logging.getLogger("jukeboxen")
logging.basicConfig(level=logging.DEBUG)

def get_artist_id(artist_name, jb_client):
    artist_results = jb_client.search(artist_name, type='artist')
    jb_artist_name = artist_results.page(index=0)[0].name
    jb_artist_id = artist_results.page(index=0)[0].id
    jb_logger.debug("Naively matching on first result: \
Name: {} , ID: {}".format(jb_artist_name, jb_artist_id))
    return jb_artist_id

def get_artist_releases(jb_artist_id, jb_client):
    jb_artist = jb_client.artist(jb_artist_id)
    print ("{} released {}".format(jb_artist.name, jb_artist.releases.page(1)))
    jb_logger.debug("Found {} albums by {}...".format(len(jb_artist.releases), jb_artist.name))
    jb_releases = []
    for release in jb_artist.releases:
        jb_releases.append(release.id)
    jb_logger.debug("Found the following release IDs: {}".format(jb_releases))
    return jb_releases

def get_all_tracks(jb_releases, jb_client):
# using "MasterRelease" instead of "Release" as it seems to have the correct
# data, ref
# https://python3-discogs-client.readthedocs.io/en/latest/fetching_data_repl.html#masterrelease
    song_names = []
    for release in jb_releases:
        this_release = jb_client.master(release)
        for track in this_release.tracklist:
            song_names.append(track.title)

    jb_logger.debug("I got the tracks as {}".format(song_names))

@plac.annotations(
    # operation = plac.Annotation("operation to perform: bulk, create, delete, search, stats, update",
    #                             choices=["bulk", "create", "delete", "search", "stats", "update"]),
    # json_file = plac.Annotation("local json file to upload to ES", "option", "f"),
    # index_name = plac.Annotation("index to create, update, or delete", "option", "i"),
    # movie_id = plac.Annotation("ID of movie to update, delete, or create", "option", "m"),
    # primary_term = plac.Annotation("primary term number for targeted updates", "option", "p"),
    # seq_no = plac.Annotation("sequence number for targeted updates", "option", "q"),
    artist_name = plac.Annotation("artist name")
                )
def main(artist_name):
    jb_logger.debug("Artist name received: {}".format(artist_name))
    # discogs requires a unique user-agent per application
    jb_id = "Jukeboxen"
    jb_vers = "0.0.1a"
    jb_user_agent = "{}/{}".format(jb_id, jb_vers)
    jb_token = os.environ["JB_TOKEN"]
    jb_client = discogs_client.Client(jb_user_agent, user_token=jb_token)
    jb_artist_id = get_artist_id(artist_name, jb_client)
    jb_releases = get_artist_releases(jb_artist_id, jb_client)
    get_all_tracks(jb_releases, jb_client)

if __name__ == '__main__':
    import plac
    plac.call(main)
