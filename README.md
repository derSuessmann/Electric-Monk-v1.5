# Electric Monk v1.5

This is the version 1.5 of the Electric Monk. Further market research
has shown that an Electric Monk nowadays does not answer the door
anymore. There are simply no people showing up unannounced at the door.
Therefore the version 1.5 needs no pinkish-looking skin top make it
distinguishable from the normal purple skintones.

A new requirement is believing the uttered nonsense on Twitter.
Electric Monk v1.5 will save you from the tedious task of believing all
the tweets of selected Twitter users. Electric Monk v1.5 can only
follow a small group of Twitter users. Believing everything on Twitter
is just not possible without developping a fault.

## Installation instructions

Create a python virtual environment for the project
```bash
python -m venv venv
```

Activate the virtual envirnment
```bash
. venv/bin/activate
```

Install tweepy
```bash
pip install tweepy
```

Optional: Install python-escpos for hardcopies on Epson ESCPOS compatible printers
```bash
pip install python-escpos
```

Rename myconf.example.py to myconf.py and insert your Twitter consumer key, secret, access token and secret.
