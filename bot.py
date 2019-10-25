import asyncio
import time

import praw
import logging

from helpers import get_id_from_link, result_message
from post import return_votes

logging.basicConfig(level=logging.INFO, filename="log.log")


async def inbox(item):
    if not item.was_comment:
        pm(item)
    elif item.subject == "username mention":
        comment(item)


def pm(item):
    if "r/AmItheAsshole/comments/" in item.body:
        post_id = get_id_from_link(item.body)
        results = return_votes(item._reddit, post_id)
        message = f"Hey there. Your count request was valid! So here we go: {result_message(results)}\n\nIn case you " \
                  f"have questions, head over to my profile. And have a nice day!"
        item.reply(message)
    else:
        item.reply("Hey, I am sorry, but you need to send me a link to an r/AmITheAsshole post. Please do it from the "
                   "sharing button under the post which should give you a proper link. Head over to u/AITACounter and "
                   "press on the first post if you need additional help.")
    item.mark_read()


def comment(item):
    results = None
    if "r/AmItheAsshole/comments/" in item.body:
        post_id = get_id_from_link(item.body)
        results = return_votes(item._reddit, post_id)
    elif item.subreddit.id == "2xhvq":
        post_id = item.submission.id
        results = return_votes(item._reddit, post_id)
    elif hasattr(item.submission, "crosspost_parent_list"):
        for cross_post in item.submission.crosspost_parent_list:
            if cross_post["subreddit_id"][3:] == "2xhvq":
                post_id = cross_post["id"]
                results = return_votes(item._reddit, post_id)
    if results:
        message = f"Hey, {result_message(results)}\n\n[Get an updated version of this](https://np.reddit.com/message/" \
                  f"compose/?to=AITACounter&message={results[3]}&subject=Doesn't+matter)|[learn more about me]" \
                  f"(https://www.reddit.com/user/AITACounter/comments/dm9580/about_me/)|" \
                  f"[look at my source](https://github.com/Poolitzer/AITACounter)\n---------|----------|----------"
    else:
        message = f"Hey, I'm sorry, but your request wasn't valid. To learn more about when it is, please head " \
                  f"[over here](https://www.reddit.com/user/AITACounter/comments/dm9580/about_me/)"
    item.reply(message)
    item.mark_read()


def main():
    reddit = praw.Reddit("bot")
    while True:
        try:
            for item in reddit.inbox.unread():
                asyncio.run(inbox(item))
        except Exception as e:
            logging.info(f"Exception: {e}")
            reddit.redditor("JustCallMePoolitzer").message(f"FUCK ME AN EXCEPTION", f"{e}")
        # everybody needs a rest
        time.sleep(3)


if __name__ == "__main__":
    main()
