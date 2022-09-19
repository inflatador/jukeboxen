#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

# jukeboxen.py: given a band name, downloads song data from discogs and
# outputs a list of their songs in DNS hostname (RFC ???) format.
# Now you can name servers/containers/whatever after your favorite band's
# songs!

# Version: 0.0.3a
# Author: Brian King

import discogs_client
import logging
import os
import plac
import sys
import validators


jb_logger = logging.getLogger("jukeboxen")

def get_releases(artist_name, jb_client):
    artist_results = jb_client.search(artist_name, artist=artist_name, type='master')
    # print (dir(artist_results))
    # 'client', 'count', 'filter', 'page', 'pages', 'per_page', 'sort', 'url'
    # FIXME: Only using the first page of search results to avoid rate-limiting.
    # We'll handle more results eventually.
    first_page_of_releases = artist_results.page(1)
    song_names = []
    for release in first_page_of_releases:
        # print ("Tracklist: {}".format(release.tracklist))
        for track in release.tracklist:
            song_names.append(track.title)
            jb_logger.debug("Appending track titled '{}' to song names...".format(track.title))
    jb_logger.info("Found {} song names...".format(len(song_names)))
    return song_names

# FIXME: Better transformation (existing library/regex?)
def convert_to_hostnames(song_names):
    converted_hostnames = []
    badchars = ['.', '~', '?', '!', '`']
    for song_name in song_names:
        for badchar in badchars:
            song_name = song_name.replace(badchar,"")
        song_name = song_name.replace(" ", "-")
        song_name = song_name.replace("--", "-")
        song_name = song_name.replace("'", "")
        song_name = song_name.lower()
        converted_hostnames.append(song_name)
    return converted_hostnames

# FIXME: Better validation
def validate_hostnames(converted_hostnames):
    validated_hostnames = []
    for hostname in converted_hostnames:
        jb_logger.debug("Validating hostname {}...".format(hostname))
        if validators.domain("{}.example.com".format(hostname)):
            validated_hostnames.append(hostname)
    jb_logger.info("Found {} potential hostnames...".format(len(validated_hostnames)))
    return validated_hostnames

@plac.annotations(
    artist_name = plac.Annotation("artist name"),
    verbose = plac.Annotation("verbose output", "flag", "v")
                )
def main(artist_name, verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    jb_logger.info("Artist name received: {}".format(artist_name))
    # discogs requires a unique user-agent per application
    jb_id = "Jukeboxen"
    jb_vers = "0.0.3a"
    jb_user_agent = "{}/{}".format(jb_id, jb_vers)
    try:
        jb_token = os.environ["JB_TOKEN"]
    except:
        print ("Error, environment variable 'JB_TOKEN' is unset. Please set \
to your discogs user token and try again.")
        sys.exit(1)
    jb_client = discogs_client.Client(jb_user_agent, user_token=jb_token)
    song_names = get_releases(artist_name, jb_client)
    converted_hostnames = convert_to_hostnames(song_names)
    validated_hostnames = validate_hostnames(converted_hostnames)
    validated_hostnames = sorted(set(validated_hostnames))
    print ("Suggested hostnames from the catalog of {}: ".format(artist_name))
    for vh in validated_hostnames:
        print (vh)
if __name__ == '__main__':
    import plac
    plac.call(main)
