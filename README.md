# jukeboxen.py

Given a band name, downloads song data from [discogs](https://www.discogs.com) and
outputs a list of their songs in DNS hostname (RFC ???) format.
Now you can name your servers/containers/whatever after your favorite band's
songs!

## Invoking

./jukeboxen.py "Band Name"

# Required Libraries

- [discogs_client](https://github.com/joalla/discogs_client)

- [plac](https://github.com/ialbert/plac)

- [validators](https://github.com/python-validators/validators)

# Using the Discogs API

The script requires a Discogs API user token as described [here](https://www.discogs.com/developers/#page:authentication).

You should set the token as an environment variable "JB_TOKEN" before running the script:
`export JB_TOKEN=blahblahyourtokenhere`
