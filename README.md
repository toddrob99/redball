# redball
Created by Todd Roberts - https://github.com/toddrob99/redball/

The redball bot management platform facilitates creating, configuring, and running of bots using a web interface. 

Standard bots are included, with the ability to import custom bots.

# Preview

The redball bot management platform and included bots are still in development. Here is a preview of the platform.

## Home / Bots
![Home/Bots](https://github.com/toddrob99/redball/blob/master/preview/redball_preview_home.png?raw=true)

## Bot Config
![Bot Config](https://github.com/toddrob99/redball/blob/master/preview/redball_preview_botconfig.png?raw=true)

## System Config
![System Config](https://github.com/toddrob99/redball/blob/master/preview/redball_preview_sysconfig.png?raw=true)

## Logs
![Logs](https://github.com/toddrob99/redball/blob/master/preview/redball_preview_logs.png?raw=true)

## API - GET Bots
![API - GET Bots](https://github.com/toddrob99/redball/blob/master/preview/redball_preview_api_get_bots.png?raw=true)

## API - GET Single Bot
![API - GET Single Bot Config](https://github.com/toddrob99/redball/blob/master/preview/redball_preview_api_get_bot.png?raw=true)

## API - GET Bot Types
![API - GET Bot Types](https://github.com/toddrob99/redball/blob/master/preview/redball_preview_api_get_bottypes.png?raw=true)

## API - GET Reddit Authorizations
![API - GET Reddit Authorizations](https://github.com/toddrob99/redball/blob/master/preview/redball_preview_api_get_redditauths.png?raw=true)

## API - POST, PUT, DELETE
The API also supports POST to create new records, PUT to modify existing records, and DELETE to delete records, for each of the entities shown above.

# Install & Run
## Dependencies
Before running redball, ensure you have Python 3 (Python 2.7 support is ending soon),
and install praw and requests via pip if you'll be using the built-in bot types or reddit authorization management (`pip install praw`, `pip install requests`).

Install pyOpenSSL (`pip install pyOpenSSL`) if you will be enabling HTTPS. This is highly recommended if you plan to make the web interface internet-facing. You will need to provide the SSL certificate, private key, and certificate chain if applicable in System Config.

Download redball from [GitHub](https://github.com/toddrob99/redball/) and run `redball.py` from the root directory of the code.

Application startup will be logged to logs\redball.log by default. To enable debug logging in the console, use the `-v` or `--verbose` command line argument (`redball.py -v`). 
To disable console logging during startup, use the `-q` or `--quiet` command line argument (`redball.py -q`). To manage logging settings outside the startup process, go to the 
System Config page of the web interface.

## Web Interface
By default the web interface listens on port 8080. Override this during startup with the `-p` command line argument (`-p=80`). 
Then set the port in the System Config page of the web interface.

Access the web interface by navigating to http://localhost:8080, or whatever port you specified.

I highly recommend enabling authentication under System Config, especially if you plan to expose the web interface to the internet.

### Bots
The bots/home page includes a list of configured bots with start/stop controls and status, as well as a tile to create a new bot. 

Click Edit to change the bot properties and configuration. 
On the bot edit page, you can create new categories for your bot settings or add/edit/delete settings within existing categories. 
If you delete the last setting in a given category, the category will also be deleted.

When creating a new bot, select the applicable bot type and reddit auth, which are configured under the System Config page.

### System Config
The System Config page displays available system settings within the following categories: Web/Security, Logging, API, Bot Types, and Reddit Authorizations. 

* Web/Security
	* Authentication method, either none, basic, or form-based (default is form-based with username admin and password redball--be sure to change if you make redball internet-facing)
	* HTTP root for web interface - this should be the URL you use to access the web interface (including https if applicable), e.g. http://localhost:8080, or if you use a reverse proxy it might be something like https://redball.mydomain.com. This is important for reddit authorizations.
	* HTTP port for web interface
	* HTTP proxy support
	* HTTPS support
		* Port for HTTPS web interface (standard port is 443)
		* File paths to certificate, private key, and certificate chain (if applicable) should include escaped backspaces (\\), e.g. c:\certs\cert.pem -> C:\\certs\\cert.pem.
		* Option to disable HTTP when HTTPS is enabled
* Logging
	* Enable/disable logging to console and/or file
	* Log level for console and file
* API
	* Enable API by generating an API Key, disable by clearing
* Bot Types
	* Add/edit/delete bot types, including name and module name. More details in the Bot Types section below
* Reddit Authorizations
	* Add/edit/delete reddit authorizations. More details in the Reddit Authorizations section below

### Logs
The Logs page displays a list of log files from the /logs directory, sorted into groups for system, webserver, and each bot.
The filenames are links to the files, in case you find that more convenient than browsing to the /logs folder.

### Logout / Change Password
The logged in user name will display at the top-right of the website. Click the username to change the password. The default password for the admin user is redball.

Click the Logout link at the top-right of the website to log out; this will direct you back to the login page.

## Bot Setup
### Bot Types
There are three built-in bot types:
* MLB Game Threads - bots can be configured to post and update discussion threads on Reddit related to a specific MLB team
* MLB Data - bots will reply with requested MLB data when invoked via Reddit comment
* Placeholder - bots will just loop without actually doing anything. This is intended to serve as a template for custom bot types

Additional bot types can be defined on the System Config page, in the Bot Types section. Enter a description and module name (e.g. if your module is myCoolBot.py, module name would be myCoolBot)

To set up a custom bot type, place your Python module in the /bots folder and add a custom bot with the module filename (without .py) in the module name field.

### Reddit Authorizations
Reddit API access is managed through redball, rather than each bot having to handle it independently. This allows you to authorize your bot account once and use that authorization for each bot.

To set up a Reddit authorization, first you have to create an app on the Reddit developer website. 

* Log in to Reddit with the account you want your bot to run as
* Go to https://www.reddit.com/prefs/apps
* Click the link/button to create an app
* Give your app a name, redball for example
* Select web app, enter a description and about url if you want
* For redirect uri, it is very important that you enter the same value as the HTTP Root on the System Config page, suffixed with /authorize. This should be the URL you use to access the web interface, e.g. http://localhost:8080/authorize, or if you use a reverse proxy it might be something like https://redball.mydomain.com/authorize. If the redirect uri on your Reddit app does not match the HTTP Root setting plus /authorize, you will receive an `invalid grant` error when attempting to complete the authorization.
* Submit the form to create your app

Once your app is created, you will need to copy the client id and secret into a new Reddit Authorization in the redball System Config page. 

The client id is under your app's name at the top left of the app display. 

Click the edit link on your app to see the secret. 

Select the scopes required for your bot, or just select all of them if you don't know which are required. You can always come back to this page, edit the auth to change which scopes are allowed, and re-authorize if you miss one.

* `edit`: 'Edit and delete my comments and submissions.
* `identity`: Access my reddit username and signup date.
* `modconfig`: Manage the configuration, sidebar, and CSS of subreddits I moderate.
* `modflair`: Manage and assign flair in subreddits I moderate.
* `modlog`: Access the moderation log in subreddits I moderate.
* `modposts`: Approve, remove, mark nsfw, and distinguish content in subreddits I moderate.
* `mysubreddits`: Access the list of subreddits I moderate, contribute to, and subscribe to.
* `privatemessages`: Access my inbox and send private messages to other users.
* `read`: Access posts, listings and comments through my account.
* `submit`: Submit links and comments from my account.
* `subscribe`: Manage my subreddit subscriptions.
* `vote`: Submit and change my votes on comments and submissions.

After you save the Reddit Auth in redball System Config, click the authorize button to open Reddit and allow the app access to your account (make sure you're logged in as your bot account).

If your browser does not open automatically, check the redball log for the URL. The log entry will say `Failed to launch web browser for Reddit authorization. URL:` followed by the URL. Go to that URL in your browser.

After you authorize the app to access your Reddit account, you should be redirected to redball with a code in the address bar of your browser. The code should be processed by redball automatically, and you should see a refresh token listed under the Reddit Auth you just authorized. If you see an error instead, your redirect uri likely did not match. See above and try again.

### Adding Your Bot
Add a bot on the Bots page by entering a name, selecting the bot type, selecting whether or not to enable auto run, selecting a Reddit Auth if applicable, and clicking Create.

### Running Your Bot
If you enable auto run for your bot, it will start automatically when redball starts up. 

If you manually stop a bot, it will remain stopped until you start it or redball is restarted (if auto run is enabled).

If your bot stops unexpectedly due to an error, redball includes an overwatch process that will start it again within seconds.

### Configuring Your Bot
Each bot has its own flexible configuration. You can view and manage a bot's configuration by clicking the bot's Edit button on the Bots page.
This includes the ability to upload a file in json format containing the bot's settings. See the API section (POST and PUT /api/v1/bots/<bot_id>/config) for example format.

The redball platform will pass two parameters to the start() function of the bot module. 

* A bot object, so the bot can monitor for the bot.STOP flag and end its process when instructed to do so.
* A multi-level dict of categories > settings, including the following as well as any settings defined for the bot:
	* `Database`
		* `dbPath` - path where the bot should access the sqlite database
		* `dbFile` - filename of the sqlite database the bot should use
		* `dbTablePrefix` - prefix the bot should use for all tables it creates/uses
	* `Reddit Auth`
		* `reddit_clientId` - client id from the Reddit app associated with the bot's configured Reddit Auth
		* `reddit_clientSecret` - secret from the Reddit app associated with the bot's configured Reddit Auth
		* `reddit_refreshToken` - refresh token associated with the bot's configured Reddit Auth
	* *`Category`*
		* *`Key`* - Any additional settings defined for the bot will be included in the settings dict with the category as the key and that category's settings as a nested dict.

## API
The redball restful API is disabled by default. Enable it by generating an API key on the System Config page.

The API URL is HTTP_ROOT/api/v1, for example http://localhost:8080/api/v1 or http://127.0.0.1:8080/api/v1 depending on your HTTP root.

Every request must include the apikey parameter, with your API key as the value. For example: http://localhost:8080/api/v1/bots?apikey=1234567890abcdefghijklmnopqrstuvwxyz. 

Each API response will by in JSON format with the following top-level keys:
* meta - dict containing api_version and timestamp when the response was generated
* errors - string or list of strings if request encountered error(s)
* response - requested data

### GET /api/v1/bots
Request with no additional parameters to return a list of bots with their id, name, type, associated reddit authorization id, auto run setting, and current status.

Request with bot id for info about a specific bot: GET /api/v1/bots/1.

Request with bot id and specific configuration field to return only the bot id and requested field: GET /api/v1/bots/1/name.

Request with config as the field name (/api/v1/bots/<bot_id>/config) to return the configuration settings for the bot. The config data will be in the same format you can use with POST and PUT, but it will include id and bot id which you should remove when importing (although they will be ignored).

Request with config as field name followed by a specific botConfig id (/api/v1/bots/<bot_id>/config/<botConfig_id>) to return the single configuration setting.

### POST /api/v1/bots
Use POST to create a new record. The request will fail if the bot already exists (use PUT to update).

The following parameters are accepted:
* name (required) - the name you want to assign to your new bot
* botType (required) - the internal id of the type of bot you want to create (obtain through bottypes endpoint)
* autoRun (required) - True or False, if you want the bot to run on startup or not
* redditAuth (optional) - if included, should be the internal id of the reddit authorization obtained through the redditauth endpoint.

If successful, the response will include the new bot id.

Use POST /api/v1/bots/<bot_id>/config to add configuration settings to a given bot. Existing settings will not be updated. Use PUT to overwrite existing settings.

Create a single config setting with the following fields:

* category (required)
* key (required)
* val (required)
* description - will be displayed on the bot settings page; key will be displayed if description is empty
* type - string containing either str, int, bool, or list - currently not used but intended to help with config validation
* options - list of valid values for the key; if present, the field will be a dropdown instead of a text field ont he bot settings page
* subkeys - list of keys (in the same category) which are subkeys of the given key
* parent_key - to be populated on subkeys, the key of the parent

To create multiple settings in a single request, include the settings info in json format in the POST request body using the following structure. The only required fields are category, key, and val.

The only difference between POST /api/v1/bots/<bot_id>/config and PUT /api/v1/bots/<bot_id>/config is POST will preserve existing values and PUT will replace existing values. 

Neither POST nor PUT will delete settings that exist in the DB but do not exist in the uploaded file. 
Either DELETE via API first (DELETE /api/v1/bots/<bot_id>/config to delete all settings), or upload the file with the clean option in the UI.

```
{
	"<Category1>" : [{
			"key" : "<KEY>",
			"description" : "<DESCRIPTION>",
			"type" : "<str OR int OR bool OR list>",
			"val": "<VALUE>",
			"options" : ["<opt1>", "<opt2>", "<opt3>"],
			"subkeys" : ["<subkey1_key>", "<subkey2_key>", "<subkey3_key>"],
			"parent_key" : "<parent_key>"
		},{
			"key" : "<KEY>",
			"description" : "<DESCRIPTION>",
			"type" : "<str OR int OR bool OR list>",
			"val": "<VALUE>",
			"options" : ["<opt1>", "<opt2>", "<opt3>"],
			"subkeys" : ["<subkey1_key>", "<subkey2_key>", "<subkey3_key>"],
			"parent_key" : "<parent_key>"
		}],
	"<Category2>" : [{
			"key" : "<KEY>",
			"description" : "<DESCRIPTION>",
			"type" : "<str OR int OR bool OR list>",
			"val": "<VALUE>",
			"options" : ["<opt1>", "<opt2>", "<opt3>"],
			"subkeys" : ["<subkey1_key>", "<subkey2_key>", "<subkey3_key>"],
			"parent_key" : "<parent_key>"
		},{
			"key" : "<KEY>",
			"description" : "<DESCRIPTION>",
			"type" : "<str OR int OR bool OR list>",
			"val": "<VALUE>",
			"options" : ["<opt1>", "<opt2>", "<opt3>"],
			"subkeys" : ["<subkey1_key>", "<subkey2_key>", "<subkey3_key>"],
			"parent_key" : "<parent_key>"
		}]
}
```

### PUT /api/v1/bots/<bot_id>
Use PUT to update an existing bot. Bot_id should be the internal id of the bot to update.

Supported parameters include name, botType, autoRun, and redditAuth. Include any or all that you want to update.

Start and stop a bot via PUT /api/v1/bots/<bot_id>/start and PUT /api/v1/bots/<bot_id>/stop.

Update bot configuration with json payload via PUT /api/v1/bots/<bot_id>/config. 
This functions the same as POST to the same endpoint, except existing values will be overwritten in addition to new settings being inserted.

Update a single bot configuration setting via PUT /api/v1/bots/<bot_id>/config/<botConfig_id>.
The same fields are supported as listed under POST to create a single configuration setting.

### DELETE /api/v1/bots/<bot_id>
Use DELETE to delete a bot. Bot_id should be the internal id of the bot you want to delete.

Use DELETE /api/v1/bots/<bot_id>/config to delete all config for the given bot id, 
or DELETE /api/v1/bots/<bot_id>/config/<botConfig_id> to delete a specific configuration setting.

Use extreme caution, because DELETE actions cannot be undone.

### GET /api/v1/botTypes
Request with no additional parameters to return a list of bot types with their id, name, description, and module name.

Request with botType id for info about a specific bot type: GET /api/v1/bottypes/1.

Request with botType id and specific configuration field to return only the botType id and requested field: GET /api/v1/bottypes/1/moduleName.

### POST /api/v1/botTypes
Use POST to create a new record. The request will fail if the record already exists (use PUT to update).

The following parameters are accepted:
* description (required) - the name of the bot type you want to create
* moduleName (required) - the filename of the python module associated with the new bot type; module should be placed in the /bots directory

### PUT /api/v1/botTypes/<botType_id>
Use PUT to update an existing record. BotType_id should be the internal id of the botType to update.

Supported parameters include description and moduleName. Include one or both.

### DELETE /api/v1/botTypes/<botType_id>
Use DELETE to delete a record. BotType_id should be the internal id of the botType you want to delete.

Use extreme caution, because this action cannot be undone.

### GET /api/v1/redditAuths
Request with no additional parameters to return a list of reddit authorizations with their id, description, reddit_appId, reddit_appSecret, reddit_scopes, reddit_refreshToken, and reddit_uniqueCode.

Request with redditAuth id for info about a specific reddit authorization: GET /api/v1/redditAuths/1.

Request with redditAuth id and specific configuration field to return only the redditAuth id and requested field: GET /api/v1/redditAuths/1/reddit_scopes.

### POST /api/v1/redditAuths
Use POST to create a new record. The request will fail if the record already exists (use PUT to update).

The following parameters are accepted:
* description (required) - the name of the reddit authorization you want to create (e.g. BotUserName AllScopes)
* reddit_appId (required) - app id from your reddit app (see Reddit Authorizations section)
* reddit_appSecret (required) - app secret from your reddit app (see Reddit Authorizations section)
* reddit_scopes (required) - reddit scopes to authorize (see scopes listed in Reddit Authorizations section). The format for reddit_scopes should be ['scope1','scope2','scopeN'].
* reddit_refreshToken (optional) - refresh token, which will normally be obtained through redball (see Reddit Authorizations section)

### PUT /api/v1/redditAuths/<redditAuth_id>
Use PUT to update an existing record. redditAuth_id should be the internal id of the redditAuth to update.

Supported parameters include description, reddit_appId, reddit_appSecret, reddit_scopes, and reddit_refreshToken. Include any or all that you wish to update.

The format for reddit_scopes should be ['scope1','scope2','scopeN'].

### DELETE /api/v1/redditAuths/<redditAuth_id>
Use DELETE to delete a record. RedditAuth_id should be the internal id of the redditAuth you want to delete.

Use extreme caution, because this action cannot be undone.
