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
import plac

# discogs requires a unique user-agent per application

jb_id = "Jukeboxen"
jb_vers = "0.0.1a"
jb_user_agent = "{}/{}".format(jb_id, jb_vers)

print("Jukeboxen user agent: {}".format(jb_user_agent))

jb_client = discogs_client.Client(jb_user_agent, user_token=jb_token)

album_results = jb_client.search('Zodiac', type='release')

# print(dir(album_results))

print(album_results.page(index=0))
