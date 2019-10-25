import re

from praw.models import Submission, MoreComments
from prawcore.exceptions import NotFound

from constants import abbreviations
from helpers import percentage


def return_votes(reddit, post_id):
    post = Submission(reddit, post_id)
    try:
        # this check makes sure we have an actual AITA post
        if post.subreddit.id != "2xhvq":
            raise NotFound
    except NotFound:
        return False
    vote_dict = dict.fromkeys(abbreviations, 0)
    for top_level_comment in post.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        # wth is going on here
        if not top_level_comment.author.id:
            print(vars(top_level_comment))
            continue
        # escaping automod
        if top_level_comment.author.id == "6l4z3":
            continue
        vote = re.search("|".join(abbreviations), top_level_comment.body)
        if vote:
            vote_dict[vote[0]] += 1
    percentage_dict = dict.fromkeys(abbreviations, 0)
    all_votes = 0
    for amount in vote_dict.values():
        all_votes += amount
    for key in vote_dict:
        percentage_dict[key] = percentage(vote_dict[key], all_votes)
    return vote_dict, percentage_dict, post.title, post.permalink
