#!/usr/bin/env python

import json
import praw
import webbrowser

while True:
    try:
        print(
            "Please go to https://www.reddit.com/prefs/apps if you are authorizing your own app,"
        )
        print(
            "or enter the values provided by the app owner who asked you to complete this step..."
        )
        clientID = input("Enter App ID from Reddit App settings: ")
        clientSecret = input("Enter Secret from Reddit App settings: ")
        redirectURI = input("Enter redirect uri from Reddit App settings: ")
        scopes = input(
            'Enter scopes to authorize in json list format (e.g. ["identity", "submit", "edit", "read", "modposts", "privatemessages", "flair", "modflair"]): '
        )
        r = praw.Reddit(
            client_id=clientID,
            client_secret=clientSecret,
            redirect_uri=redirectURI,
            user_agent="redball standalone reddit oauth utility v1 https://github.com/toddrob99/redball",
        )
        url = r.auth.url(json.loads(scopes), "...", "permanent")
        webbrowser.open(url)
        print(
            "\nIf your browser did not open, go to the following URL to authorize the app: {}".format(
                url
            )
        )
        print(
            "After clicking the 'allow' button, you will receive a browser error. Locate the code at the end of the URL in the address bar and paste it at the prompt below."
        )
        print(
            "For example, if the URL is http://localhost:8080/?state=...&code=sE7KbryJwK5wihhrBYEDngYUGwc, enter sE7KbryJwK5wihhrBYEDngYUGwc"
        )
        code = input("Enter code: ")
        access_information = r.auth.authorize(code)
        print("Here is your refresh token: {}".format(access_information))
        input(
            "Provide the above refresh token to the person who asked you to run this utility. Press Enter to run the utility again."
        )
    except Exception as e:
        input("Error: {}\n\nAn error occurred, press Enter to start over.".format(e))
