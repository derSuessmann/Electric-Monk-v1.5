import tweepy

from myconf import (consumer_key, consumer_secret,
                    access_token, access_token_secret)


class ElectricMonk(tweepy.StreamListener):

    def start(self, screen_names, onlyFrom=True, retweets=True, printer=None):
        self.onlyFrom = onlyFrom
        self.retweets = retweets
        self.screen_names = screen_names
        self.printer = printer

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        self.follow = map(lambda un: api.get_user(un).id_str, screen_names)

        myStream = tweepy.Stream(auth=api.auth, listener=self,
                                 tweet_mode='extended')
        myStream.filter(follow=self.follow)

    def on_status(self, status):
        if not self.retweets and self.is_retweet(status):
            return True

        if self.onlyFrom:
            if status.author.screen_name in self.screen_names:
                self.print_status(status)
        else:
            self.print_status(status)

        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False
        return True

    def is_retweet(self, status):
        return status.text[:2] == "RT"

    def print_status(self, status):
        msg = "@"+status.author.screen_name
        try:
            msg = msg + '\n' + status.extended_tweet["full_text"]
            print(msg)
        except:
            msg = msg + '\n' + status.text
            print(msg)
            if not self.is_retweet(status) and status.text[-1] == "…":
                # only retweets should be shown truncated
                print("TRUNCATED")
                print()
        print("=====")

        if self.printer:
            msg = msg.encode('ascii', 'ignore')
            msg = msg.decode()
            printer.text(msg + '\n\n')


if __name__ == "__main__":

    from escpos.printer import Usb
    import argparse

    parser = argparse.ArgumentParser(
        description='Electric Monk v1.5',
        epilog='''
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
                                     ''',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('screenname', nargs='+',
                        help='screen name to stream')
    parser.add_argument('-p', '--hardcopy', action='store_true',
                        help='print the tweets on a receipt printer')
    parser.add_argument('--only-from', action='store_true',
                        help='display only tweets from the given screen names')
    parser.add_argument('--no-retweets', action='store_true',
                        help='do not display retweets')

    args = parser.parse_args()

    if (args.hardcopy):
        try:
            printer = Usb(0x0416, 0x5011)
        except:
            print('can not open printer.')
    else:
        printer = None

    ElectricMonk().start(args.screenname, onlyFrom=args.only_from,
                         retweets=not args.no_retweets, printer=printer)
