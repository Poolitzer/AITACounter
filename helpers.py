import re


def get_id_from_link(link):
    result = re.search('r/AmItheAsshole/comments/(.+?)((?=/)|$| )', link)
    if result:
        return result[1]
    return False


def percentage(part, whole):
    return round(100 * float(part)/float(whole), 2)


def result_message(results):
    return f"The results of *{results[2]}*:\n\n* YTA: {results[1]['YTA']}% ({results[0]['YTA']})\n\n* NTA: " \
           f"{results[1]['NTA']}% ({results[0]['NTA']})\n\n* ESH: {results[1]['ESH']}% ({results[0]['ESH']})\n\n" \
           f"* NAH: {results[1]['NAH']}% ({results[0]['NAH']})\n\n* INFO: {results[1]['INFO']}% ({results[0]['INFO']})"
