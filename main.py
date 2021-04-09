# Press Umschalt+F10 to execute it or replace it with your code.

import logging

import re
import praw
import requests

if __name__ == '__main__':

    #print("Start logger")

    #handler = logging.StreamHandler()
    #handler.setLevel(logging.DEBUG)
    #for logger_name in ("praw", "prawcore"):
    #    logger = logging.getLogger(logger_name)
    #    logger.setLevel(logging.DEBUG)
    #    logger.addHandler(handler)

    print("Start praw")

    reddit = praw.Reddit(
        user_agent="USER AGENT",
        client_id="ID",
        client_secret="SECRET",
        username="WKN-Bot",
        password="PASSWORD",
    )

    # print("OBACHT! Da hat wohl jemand eine WKN genannt ohne KLIPP und KLAR den BASISWERT zu erwähnen.")

    print("Start fetching comments")

    subreddit = reddit.subreddit("mauerstrassenwetten")
    for comment in subreddit.stream.comments(skip_existing=True):
        print("Found new comment: ")
        print(comment.body)
        print("\n")

        answer = [""]
        answerTxt = [""]

        if comment.body == "!WKN" or comment.body == "!wkn":
            tier = comment.parent_id.split("_")
            if tier[0] == "t1":
                parentComment = reddit.comment(tier[1])
                matchIterator = 0
                for match in re.findall(r'\b[A-Z0-9]{6}\b', parentComment.body):
                    print("Found WKN in comment:", match)
                    print(f"https://onvista.de/{match}")
                    templink: str = f"https://onvista.de/{match}"
                    xlink = requests.get(templink)
                    link = xlink.url
                    if matchIterator == 0:
                        answer[0] = link
                        answerTxt[0] = match
                    else:
                        answer.append(link)
                        answerTxt.append(match)
                    matchIterator = matchIterator + 1

                if matchIterator == 0:
                    comment.reply("Ich habe leider keine gültigen WKNs gefunden.")
                else:
                    matchIterator = 0
                    antwort = "Ich habe folgende WKNs gefunden:\n\n"
                    for nix in answer:
                        antwort = antwort + f"[{answerTxt[matchIterator]}]({answer[matchIterator]})\n"

                    print(antwort)
                    comment.reply(antwort)

        # # Finde passende Posts
        # if len(submission.title.split()) > 10:
        #     return
        #
        # questions = ["what is", "who is", "what are"]
        # normalized_title = submission.title.lower()
        # for question_phrase in questions:
        #     if question_phrase in normalized_title:
        #         # mache etwas
        #         from urllib.parse import quote_plus
        #         reply_template = "[Let me google that for you](https://lmgtfy.com/?q={})"
        #         url_title = quote_plus(submission.title)
        #         reply_text = reply_template.format(url_title)
        #         submission.reply(reply_text)
        #         break
