<%inherit file="base.mako" />
<%! 
	import cherrypy
	import redball
	from redball import config, user

	if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_config_rw'):
		priv = 2
	elif user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_config_ro'):
		priv = 1
	else:
		priv = 0
%>

<%block name="content">
	% if priv > 0:
	% if botType_id == None and redditAuth_id == None and user_id == None:
		<div id="sysConfigGrid" class="configGrid layoutGrid">
			<% allConfig = config.get_sys_config() %>
			% for cat in set(c['category'] for c in allConfig):
				% if any((x for x in allConfig if x['category']==cat)):
					<div id="sysConfig_${cat}" class="configCategory gridItem">
						<div class="gridItemContent">
							<form id="${cat}" method="post" action="/config"${'onsubmit="return confirm(' + "'The webserver will be restarted. Continue?'" + ');"' if cat=='Web/Security' else ''}>
							<input type="hidden" name="type" value="${cat}" />
							<span class="configCategoryName">${cat}</span>
							% for x in (x for x in allConfig if x['category']==cat):
								% if x['parent_key'] == '':
									<label for="${x['category']}|${x['key']}|${x['type']}">${x['description']}:</label> 
									% if len(x['options']):
										<select name="${x['category']}|${x['key']}|${x['type']}" class="text ui-widget-content ui-corner-all">
											% for opt in x['options']:
												<option value="${opt}"${' selected="selected"' if str(opt) == str(x['val']) else ''}>${opt}</option>
											% endfor
										</select>
									% else:
										% if x['type'] in ['str','int']:
											<input id="${x['category']}|${x['key']}|${x['type']}" name="${x['category']}|${x['key']}|${x['type']}" value="${x['val']}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if x['read_only'] == 'True' else ''} />
										% endif
									% endif
									% if len(x['subkeys']):
										% for y in (y for y in allConfig if y['parent_key'] == x['key']):
											<span class="indent">
											<label for="${y['category']}|${y['key']}|${y['type']}">${y['description']}:</label> 
											% if len(y['options']):
												<select name="${y['category']}|${y['key']}|${y['type']}" class="text ui-widget-content ui-corner-all">
													% for opt in y['options']:
														<option value="${opt}"${' selected="selected"' if str(opt) == str(y['val']) else ''}>${opt}</option>
													% endfor
												</select>
											% else:
												% if y['type'] in ['str','int']:
													<input id="${y['category']}|${y['key']}|${y['type']}" name="${y['category']}|${y['key']}|${y['type']}" value="${y['val']}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if y['read_only'] == 'True' else ''}/><br />
												% endif
											% endif
											</span>
											% if len(y['subkeys']):
												% for z in (z for z in allConfig if z['parent_key'] == y['key']):
													<span class="indent-twice">
													<label for="${z['category']}|${z['key']}|${z['type']}">${z['description']}:</label> 
													% if len(z['options']):
														<select name="${z['category']}|${z['key']}|${z['type']}" class="text ui-widget-content ui-corner-all">
															% for opt in z['options']:
																<option value="${opt}"${' selected="selected"' if str(opt) == str(z['val']) else ''}>${opt}</option>
															% endfor
														</select>
													% else:
														% if z['type'] in ['str','int']:
															<input id="${z['category']}|${z['key']}|${z['type']}" name="${z['category']}|${z['key']}|${z['type']}" value="${z['val']}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if z['read_only'] == 'True' else ''}/><br />
														% endif
													% endif
													</span>
													% if len(z['subkeys']):
														% for a in (a for a in allConfig if a['parent_key'] == z['key']):
															<span class="indent-thrice">
															<label for="${a['category']}|${a['key']}|${a['type']}">${a['description']}:</label> 
															% if len(a['options']):
																<select name="${a['category']}|${a['key']}|${a['type']}" class="text ui-widget-content ui-corner-all">
																	% for opt in a['options']:
																		<option value="${opt}"${' selected="selected"' if str(opt) == str(a['val']) else ''}>${opt}</option>
																	% endfor
																</select>
															% else:
																% if a['type'] in ['str','int']:
																	<input id="${a['category']}|${a['key']}|${a['type']}" name="${a['category']}|${a['key']}|${a['type']}" value="${a['val']}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if a['read_only'] == 'True' else ''}/><br />
																% endif
															% endif
															</span>
															% if len(a['subkeys']):
																% for c in (c for c in allConfig if c['parent_key'] == a['key']):
																	<span class="indent-fource">
																	<label for="${c['category']}|${c['key']}|${c['type']}">${c['description']}:</label> 
																	% if len(c['options']):
																		<select name="${c['category']}|${c['key']}|${c['type']}" class="text ui-widget-content ui-corner-all">
																			% for opt in c['options']:
																				<option value="${opt}"${' selected="selected"' if str(opt) == str(c['val']) else ''}>${opt}</option>
																			% endfor
																		</select>
																	% else:
																		% if c['type'] in ['str','int']:
																			<input id="${c['category']}|${c['key']}|${c['type']}" name="${c['category']}|${c['key']}|${c['type']}" value="${c['val']}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if c['read_only'] == 'True' else ''}/><br />
																		% endif
																	% endif
																	</span>
																% endfor
															% endif
														% endfor
													% endif
												% endfor
											% endif
										% endfor
									% endif
								% endif
							% endfor
							% if priv > 1:
								<button type="submit" name="action" value="save_sysConfig" class="ui-button ui-widget ui-corner-all button-disk">Save</button>
							% endif
							</fieldset>
							</form>
						</div>
					</div>
				% endif
			% endfor
			<div id="sysConfig_botTypes" class="configCategory gridItem">
				<div class="gridItemContent">
					<span class="configCategoryName">Bot Types</span>
					<% botTypes = config.get_botTypes() %>
					% for x in botTypes:
						<div id="botType_${str(x['id'])}" class="botType">
							<form id="botType-${x['id']}" method="post" action="/config?botType_id=${str(x['id'])}">
								<strong>Description</strong>: ${x['description']}<br />
								<strong>Module Name</strong>: ${x['moduleName']}<br />
								% if priv > 1:
								<button type="Submit" name="action" value="edit_botType" class="ui-button ui-widget ui-corner-all button-wrench">Edit</button></form>
								<form id="deleteBotType" method="post" action="/config?botType_id=${str(x['id'])}" onsubmit="return in_use('botType',${str(x['id'])});">
								<button type="Submit" name="action" value="delete_botType" class="ui-button ui-widget ui-corner-all button-trash">Delete</button>
								% endif
							</form>
						</div>
					% endfor
					% if priv > 1:
						<div id="botType_new" class="botType">
							<form id="addBotType" method="post" action="/config">
								<label for="botType_description">Description:</label> <input id="botType_description" name="botType_description" value="" class="text ui-widget-content ui-corner-all" />
								<label for="botType_moduleName">Module Name:</label> <input id="botType_moduleName" name="botType_moduleName" value="" class="text ui-widget-content ui-corner-all" />
								<label for="botType_defaultSettings">Default Settings (json):</label><textarea id="botType_defaultSettings" name="botType_defaultSettings" class="text ui-widget-content ui-corner-all"></textarea>
								<button type="submit" name="action" value="create_botType" class="ui-button ui-widget ui-corner-all button-disk">Create</button>
							</form>
						</div>
					% endif
				</div>
			</div>
			<div id="sysConfig_redditAuths" class="configCategory gridItem">
				<div class="gridItemContent">
					<span class="configCategoryName">Reddit Authorizations</span>
					<% redditAuths = config.get_redditAuths() %>
					% for x in redditAuths:
						% if x['id'] > 0:
							<div id="redditAuth_${str(x['id'])}" class="redditAuth">
								<form id="redditAuth-${x['id']}" method="post" action="/config?redditAuth_id=${str(x['id'])}">
									<strong>Description</strong>: ${x['description']}<br />
									<strong>Reddit App ID</strong>: ${x['reddit_appId']}<br />
									<strong>Reddit App Secret</strong>: ${x['reddit_appSecret']}<br />
									<strong>Reddit Refresh Token</strong>: ${x['reddit_refreshToken']}<br />
									<strong>Reddit Scopes</strong>: ${x['reddit_scopes']}<br />
									% if priv > 1:
									<button type="Submit" name="action" value="edit_redditAuth" class="ui-button ui-widget ui-corner-all button-wrench">Edit</button> 
									<button type="Submit" name="action" value="authorize_redditAuth" class="ui-button ui-widget ui-corner-all button-key"${' onclick="return confirm({}Are you sure you want to re-authorize? There is already a refresh token present.{});"'.format("'","'") if x['reddit_refreshToken'] not in ['',None] else ''}>Authorize</button></form> 
									<form id="deleteRedditAuth" method="post" action="/config?redditAuth_id=${str(x['id'])}" onsubmit="return in_use('redditAuth',${str(x['id'])});">
									<button type="Submit" name="action" value="delete_redditAuth" class="ui-button ui-widget ui-corner-all button-trash">Delete</button>
									% endif
								</form>
							</div>
						% endif
					% endfor
					% if priv > 1:
					<div id="redditAuth_new" class="redditAuth">
						<form id="addRedditAuth" method="post" action="/config">
							<label for="redditAuth_description">Description:</label> <input id="redditAuth_description" name="redditAuth_description" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="redditAuth_redditAppId">Reddit App ID:</label> <input id="redditAuth_redditAppId" name="redditAuth_redditAppId" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="redditAuth_redditAppSecret">Reddit App Secret:</label> <input id="redditAuth_redditAppSecret" name="redditAuth_redditAppSecret" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="redditAuth_redditRefreshToken">Reddit Refresh Token:</label> <input id="redditAuth_redditRefreshToken" name="redditAuth_redditRefreshToken" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="redditAuth_redditScopes">Reddit Scopes:</label> <select name="redditAuth_redditScopes" multiple class="text ui-widget-content ui-corner-all">
								% for redditScope in config.get_redditScopes():
									<option value="${redditScope['name']}" selected="selected">${redditScope['name']}</option>
								% endfor
							</select><br />
							<button type="submit" name="action" value="create_redditAuth" class="ui-button ui-widget ui-corner-all button-disk">Create</button>
						</form>
					</div>
					% endif
				</div>
			</div>
			% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_user_ro'):
			<div id="sysConfig_users" class="configCategory gridItem">
				<div class="gridItemContent">
					<span class="configCategoryName">Users</span>
					<%
						users = user.get_user_info()
						if isinstance(users, dict):
							users = [users]
					%>
					% for x in users:
						<div id="user_${str(x['id'])}" class="user">
							<form id="user-${x['id']}" method="post" action="/config?user_id=${str(x['id'])}">
								<strong>User ID</strong>: ${x['userid']}<br />
								<strong>Name</strong>: ${x['name']}<br />
								<strong>Email</strong>: ${x['email']}<br />
								<strong>Reddit Username</strong>: ${x['reddit_userid']}<br />
								% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_apikeys_rw'):
								<strong>API Key</strong>: ${x['apikey'] if x['apikey'] not in ['',None] else ''}<br />
								% elif user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_apikeys_ro'):
								<strong>API Key</strong>: ${user.mask_apikey(x['apikey'] if x['apikey'] not in ['',None] else '')}<br />
								% endif
								<strong>Privileges</strong>: ${x['privileges']}<br />
								% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_user_rw'):
								<button type="Submit" name="action" value="edit_user" class="ui-button ui-widget ui-corner-all button-wrench">Edit</button>
							</form> 
							<form id="resetUserPassword" method="post" action="/password?user_id=${str(x['id'])}">
								<button type="Submit" name="action" value="reset_user_password" class="ui-button ui-widget ui-corner-all button-gear" title="Change${' {}\'s '.format(x['userid']) if x['userid'] != cherrypy.session.get("_cp_username") else ''} Password">Password</button>
							</form>
								% endif
								% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_apikeys_rw'):
							<form id="generateUserApiKey" method="post" action="/config?user_id=${str(x['id'])}">
								<button type="submit" name="action" value="generate_user_apikey" class="ui-button ui-widget ui-corner-all button-gear" title="${'Generate' if x['apikey'] in ['',None] else 'Regenerate'} API Key" ${'onclick="return confirm(\'Are you sure you want to generate a new API Key? This will remove the current API Key.\');"' if x['apikey'] not in ['',None] else ''}>API</button>
							</form>
								% endif
								% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_user_rw'):
							<form id="deleteUser" method="post" action="/config?user_id=${str(x['id'])}" onsubmit="return confirm('Are you sure you want to permanently delete this user?');">
								<button type="Submit" name="action" value="delete_user" class="ui-button ui-widget ui-corner-all button-trash">Delete</button>
								% endif
							</form>
						</div>
					% endfor
					% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_user_rw'):
					<div id="user_new" class="user">
						<form id="addUser" method="post" action="/config">
							<label for="user_userid">User ID:</label> <input id="user_userid" name="user_userid" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="user_password">Password:</label> <input type="password" id="user_password" name="user_password" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="user_passwordConfirm">Confirm Password:</label> <input type="password" id="user_passwordConfirm" name="user_passwordConfirm" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="user_name">Name:</label> <input id="user_name" name="user_name" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="user_email">Email:</label> <input id="user_email" name="user_email" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="user_reddit_userid">Reddit Username:</label> <input id="user_reddit_userid" name="user_reddit_userid" value="" class="text ui-widget-content ui-corner-all" /><br />
							<label for="user_privileges">Privileges:</label> <select name="user_privileges" multiple class="text ui-widget-content ui-corner-all">
								% for p in user.get_privileges():
									<option value="${p['privilege']}">${'{} - {}'.format(p['privilege'], p['description'])}</option>
								% endfor
							</select><br />
							<button type="submit" name="action" value="create_user" class="ui-button ui-widget ui-corner-all button-disk">Create</button>
						</form>
					</div>
					% endif
				</div>
			</div>
			% endif
		</div>
	% elif botType_id != None:
		<div id="sysConfig_botType" class="configCategory gridItem">
			<div class="gridItemContent">
				<% x = config.get_botTypes(botType_id) %>
				<form id="editbotType" method="post" action="/config?botType_id=${str(x['id'])}">
					<label for="botType_description">Description:</label> <input id="botType_description" name="botType_description" value="${x['description']}" class="text ui-widget-content ui-corner-all" />
					<label for="botType_moduleName">Module Name:</label> <input id="botType_moduleName" name="botType_moduleName" value="${x['moduleName']}" class="text ui-widget-content ui-corner-all" />
					<label for="botType_defaultSettings">Default Settings (json):</label><textarea id="botType_defaultSettings" name="botType_defaultSettings" class="text ui-widget-content ui-corner-all">${x['defaultSettings'] if x.get('defaultSettings') else ''}</textarea>
					% if priv > 1:
					<button type="Submit" name="action" value="save_botType" class="ui-button ui-widget ui-corner-all button-disk">Save</button> <button type="submit" name="action" value="cancel" class="ui-button ui-widget ui-corner-all button-close">Cancel</button>
					% endif
				</form>
			</div>
		</div>
	% elif redditAuth_id != None:
		<div id="redditAuth" class="configCategory gridItem">
			<div class="gridItemContent">
				<% x = config.get_redditAuths(redditAuth_id) %>
				<form id="editRedditAuth" method="post" action="/config?redditAuth_id=${str(x['id'])}">
					<label for="redditAuth_description">Description:</label> <input id="redditAuth_description" name="redditAuth_description" value="${x['description']}" class="text ui-widget-content ui-corner-all" /><br />
					<label for="redditAuth_redditAppId">Reddit App ID</label> <input id="redditAuth_redditAppId" name="redditAuth_redditAppId" value="${x['reddit_appId']}" class="text ui-widget-content ui-corner-all" /><br />
					<label for="redditAuth_redditAppSecret">Reddit App Secret:</label> <input id="redditAuth_redditAppSecret" name="redditAuth_redditAppSecret" value="${x['reddit_appSecret']}" class="text ui-widget-content ui-corner-all" /><br />
					<label for="redditAuth_redditRefreshToken">Reddit Refresh Token:</label> <input id="redditAuth_redditRefreshToken" name="redditAuth_redditRefreshToken" value="${x['reddit_refreshToken']}" class="text ui-widget-content ui-corner-all" /><br />
					<label for="redditAuth_redditScopes">Reddit Scopes</label> <select name="redditAuth_redditScopes" multiple class="text ui-widget-content ui-corner-all">
						% for redditScope in config.get_redditScopes():
							<option value="${redditScope['name']}"${' selected="selected"' if str(redditScope['name']) in x['reddit_scopes'] else ''}>${redditScope['name']}</option>
						% endfor
					</select><br />
					% if priv > 1:
					<button type="submit" name="action" value="save_redditAuth" class="ui-button ui-widget ui-corner-all button-disk">Save</button> <button type="submit" name="action" value="cancel" class="ui-button ui-widget ui-corner-all button-close">Cancel</button> 
					<button type="Submit" name="action" value="authorize_redditAuth" class="ui-button ui-widget ui-corner-all button-key">Authorize</button>
					% endif
				</form>
			</div>
		</div>
	% elif user_id is not None:
		% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_user_ro'):
		<div id="user" class="configCategory gridItem">
			<div class="gridItemContent">
				<% x = user.get_user_info(uid=user_id) %>
				<form id="editUser" method="post" action="/config?user_id=${str(x['id'])}">
					<label for="user_userid">User ID:</label> <input id="user_userid" name="user_userid" value="${x['userid']}" class="text ui-widget-content ui-corner-all" /><br />
					<label for="user_name">Name:</label> <input id="user_name" name="user_name" value="${x['name']}" class="text ui-widget-content ui-corner-all" /><br />
					<label for="user_email">Email:</label> <input id="user_email" name="user_email" value="${x['email']}" class="text ui-widget-content ui-corner-all" /><br />
					<label for="user_reddit_userid">Reddit Username:</label> <input id="user_reddit_userid" name="user_reddit_userid" value="${x['reddit_userid']}" class="text ui-widget-content ui-corner-all" /><br />
					% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_apikeys_rw'):
					<label for="user_apikey">API Key:</label> <input id="user_apikey" name="user_apikey" value="${x['apikey'] if x['apikey'] not in ['',None] else ''}" class="text ui-widget-content ui-corner-all" readonly onclick="copyText(this)" /><br />
					% elif user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_apikeys_ro'):
					<label for="user_apikey">API Key:</label> <input id="user_apikey" name="user_apikey" value="${user.mask_apikey(x['apikey']) if x['apikey'] not in ['',None] else ''}" class="text ui-widget-content ui-corner-all" readonly /><br />
					% endif
					<label for="user_privileges">Privileges:</label> <select name="user_privileges" multiple class="text ui-widget-content ui-corner-all">
						% for p in user.get_privileges():
							<option value="${p['privilege']}"${' selected="selected"' if str(p['privilege']) in x['privileges'] else ''}>${'{} - {}'.format(p['privilege'], p['description'])}</option>
						% endfor
					</select><br />
					% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_user_rw'):
					<button type="submit" name="action" value="save_user" class="ui-button ui-widget ui-corner-all button-disk">Save</button> <button type="submit" name="action" value="cancel" class="ui-button ui-widget ui-corner-all button-close">Cancel</button>
				</form> 
				<form id="resetUserPassword" method="post" action="/password?user_id=${str(x['id'])}">
					<button type="Submit" name="action" value="reset_user_password" class="ui-button ui-widget ui-corner-all button-gear" title="Change${' {}\'s '.format(x['userid']) if x['userid'] != cherrypy.session.get("_cp_username") else ''} Password">Password</button>
				</form>
					% endif
					% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_apikeys_rw'):
				<form id="generateUserApiKey" method="post" action="/config?user_id=${str(x['id'])}">
					<button type="submit" name="action" value="generate_user_apikey" class="ui-button ui-widget ui-corner-all button-gear" title="${'Generate' if x['apikey'] in ['',None] else 'Regenerate'} API Key" ${'onclick="return confirm(\'Are you sure you want to generate a new API Key? This will remove the current API Key.\');"' if x['apikey'] not in ['',None] else ''}>API</button>
				</form>
					% endif
					% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_user_rw'):
				<form id="deleteUser" method="post" action="/config?user_id=${str(x['id'])}" onsubmit="return confirm('Are you sure you want to permanently delete this user?');">
					<button type="Submit" name="action" value="delete_user" class="ui-button ui-widget ui-corner-all button-trash">Delete</button>
					% endif
				</form>
			</div>
		</div>
		% else:
		Insufficient privileges.
		% endif
	% endif
	% else:
	Insufficient Privileges.
	% endif
</%block>
<%block name="pagejs">
% if priv > 0:
<script type='text/javascript'>
	function copyText(field) {
		field.select()
		document.execCommand("copy")
	}
	function in_use(field, id) {
		var result = false;
		if (field=='botType'){var prettyField='Bot Type';}
		else {var prettyField='Reddit Authorization';}
		$.ajax({
			async: false,
			url: '/inuse?'+field+'_id='+id,
			complete: function(data) {
				var count = JSON.parse(Object(data).responseText).count;
				if (count=='ERROR') {return false;}
				if (parseInt(count)>0) {
					$('#errorcontainer').html('<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>'+prettyField+' '+id+' cannot be deleted because it is in use by '+count+' bot(s).</p>').removeClass('hide');
					result = false;
				}
				if (parseInt(count)==0) {
					result = confirm('Are you sure you want to permanently delete this '+prettyField+'?');
				}
			},
			error: function() {
				$('#errorcontainer').html('<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>Error checking if '+prettyField+' '+id+' is in use by any bots.</p>').removeClass('hide');
				result = false;
			}
		});
		return result;
	}
</script>
% endif
</%block>