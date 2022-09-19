# jukeboxen.py

Given a band name, downloads song data from [discogs](https://www.discogs.com) and
outputs a list of their songs in DNS hostname (RFC ???) format.
Now you can name your servers/containers/whatever after your favorite band's
songs!

## Using the Discogs API

The script requires a Discogs API user token as described [here](https://www.discogs.com/developers/#page:authentication).

You should set the token as an environment variable "JB_TOKEN" before running the script:
`export JB_TOKEN=blahblahyourtokenhere`

## Usage

### Invoke

`./jukeboxen.py "Sir-Mix-a-Lot"`

### Example Output
```./jukeboxen.py "Sir Mix-a-Lot"
INFO:jukeboxen:Artist name received: Sir Mix-a-Lot
INFO:jukeboxen:Found 180 song names...
INFO:jukeboxen:Found 106 potential hostnames...
Suggested hostnames from the catalog of Sir Mix-a-Lot:
2-horse
a-rappers-reputation
aintsta
at-the-next-show
attack-on-the-stars
aunt-thomasina
baby-got-back
[...]
```

## Required Libraries

- [discogs_client](https://github.com/joalla/discogs_client)

- [plac](https://github.com/ialbert/plac)

- [validators](https://github.com/python-validators/validators)

## Known Issues

The following features could use some work. Feel free to file Github issues
and/or submit pull requests if interested.

- Transformation
- Validation
- Rate-limit avoidance
