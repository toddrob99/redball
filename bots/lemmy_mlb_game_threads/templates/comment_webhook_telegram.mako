## This template produces data in JSON format suitable for Telegram webhooks
## Be sure to include \n for line breaks, because actual linebreaks will be stripped out!
{"text": "${commentText.replace('"','\"').replace('\r','').replace('\n','\\n')}"}