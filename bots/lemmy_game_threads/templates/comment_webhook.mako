## This template produces data in JSON format suitable for Discord webhooks
## Be sure to include \n for line breaks, because actual linebreaks will be stripped out!
{"content": "${commentText.replace('"','\"').replace('\r','').replace('\n','\\n')}"}