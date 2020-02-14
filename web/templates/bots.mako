<%inherit file="base.mako" />
<%! 
	import cherrypy
	import redball
	from redball import config, user

	if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_all_rw'):
		priv = 3
	elif user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_all_startstop'):
		priv = 2
	elif user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_all_ro'):
		priv = 1
	else:
		priv = 0

	explicitPrivCount = sum(1 for x in redball.BOTS.values() if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_startstop'.format(x.id)) or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_ro'.format(x.id)))
%>

<%block name="topright">
	% if priv > 0 or explicitPrivCount > 0:
	<div id="botStatus_autoRefresh" name="botStatus_autoRefresh" class="refreshInterval">
		<label for="botStatus_refreshInterval">Auto Refresh Bot Status:</label>
		<select name="botStatus_refreshInterval" id="botStatus_refreshInterval" class="text ui-widget-content ui-corner-all" title="Warning: enabling auto refresh will prevent your session from timing out.">
			<option value="0" selected="selected">None</option>
			<option value="5">5 Seconds</option>
			<option value="15">15 Seconds</option>
			<option value="30">30 Seconds</option>
			<option value="60">1 Minute</option>
			<option value="300">5 Minutes</option>
			<option value="600">10 Minutes</option>
			<option value="1800">30 Minutes</option>
			<option value="3600">1 Hour</option>
		</select>
		<span id="refreshBotStatusButton" onclick="refreshBotStatus();" title="Refresh Bot Status Now" class="ui-icon ui-icon-refresh"></span>
	</div>
	% endif
</%block>

<%block name="content">
	% if priv > 0 or explicitPrivCount > 0:
	<% redditAuths = config.get_redditAuths() %>
	% if bot_id == None:
		<div id="botGrid" class="botGrid layoutGrid">
		<% botTypes = config.get_botTypes() %>
		% for b in redball.BOTS.values():
			% if priv > 0 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_ro'.format(b.id)) or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_startstop'.format(b.id)):
			<div class="bot gridItem">
				<div class="gridItemContent">
					<form id="botStatus" method="post" action="/bots?bot_id=${str(b.id)}">
						<span class="botName">${b.name}</span>
						<span class="botDetail"><strong>Type</strong>: ${next((x['description'] for x in botTypes if str(x['id']) == str(b.botType)),'Unknown')}</span>
						<span class="botDetail"><strong>Auto Run</strong>: ${b.autoRun}</span>
						<span class="botDetail"><strong>Reddit Auth</strong>: ${next((redditAuth['description'] for redditAuth in redditAuths if str(redditAuth['id']) == str(b.redditAuth)),'Unknown')}</span>
						<span class="botDetail"><strong>Status</strong>: ${'<span id="botStatus_{}" class="greenBold">Running</span>'.format(b.id) if b.isRunning() == True else '<span id="botStatus_{}" class="redBold">Stopped</span>'.format(b.id)} <span id="refreshBotStatusButton" onclick="${"refreshBotStatus('{}')".format('botId='+str(b.id))};" title="Refresh Bot Status Now" class="ui-icon ui-icon-refresh"></span></span>
						<span class="botControls">
							% if priv > 1 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_startstop'.format(b.id)):
							<button type="Submit" name="action" title="Start Bot" value="start" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-play">Start</button>
							<button type="Submit" name="action" title="Stop Bot" value="stop" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-stop">Stop</button> 
							% endif
							<button type="Submit" name="action" title="View/Edit Bot Settings" value="edit" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-wrench">Edit</button></form> 
							% if priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id)):
							<form id="deleteBot" method="post" action="/bots?bot_id=${str(b.id)}" onsubmit="return confirm('Are you sure you want to permanently delete this bot?');">
							<button type="Submit" name="action" title="Delete Bot" value="delete" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-trash">Delete</button>
							% endif
						</span>
					</form>
				</div>
			</div>
			% endif
		% endfor
			% if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_create'):
			<div class="bot compact gridItem">
				<div class="gridItemContent">
					<form id="addBot" method="post" action="#">
						<span class="botDetail"><label for="bot_name">Name:</label><input type="text" size="16" name="bot_name" class="text ui-widget-content ui-corner-all" /></span>
						<span class="botDetail"><label for="bot_type">Type:</label><select name="bot_type" class="text ui-widget-content ui-corner-all">
							% for botType in botTypes:
								<option value="${botType['id']}">${botType['description']}</option>
							% endfor
						</select></span>
						<span class="botDetail"><label for="bot_autoRun">Auto Run:</label> <select name="bot_autoRun" class="text ui-widget-content ui-corner-all">
							<option value="True">True</option>
							<option value="False" selected="selected">False</option>
						</select></span>
						<span class="botDetail"><label for="bot_redditAuth">Reddit Auth:</label> <select name="bot_redditAuth" class="text ui-widget-content ui-corner-all">
							% for redditAuth in config.get_redditAuths():
								<option value="${redditAuth['id']}">${redditAuth['description']}</option>
							% endfor
						</select></span>
						<span class="botControls"><button type="submit" name="action" value="create" class="ui-button ui-widget ui-corner-all button-disk">Create</button></span>
					</form>
				</div>
			</div>
			% endif
		</div>
	% else:
		<% b = redball.BOTS[bot_id] %>
		% if priv > 0 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_ro'.format(b.id)):
		<div id="bot_${b.id}" class="singleBot">
			<form id="editBot" method="post" action="/bots?bot_id=${b.id}">
				<input type="hidden" name="singleBot" value="True" />
				<span class="botDetail"><label for="bot_name">Name:</label><input type="text" size="16" name="bot_name" value="${b.name}" class="text ui-widget-content ui-corner-all" /></span>
				<span class="botDetail"><label for="bot_type">Type:</label><select name="bot_type" class="text ui-widget-content ui-corner-all">
					% for botType in config.get_botTypes():
						<option value="${botType['id']}"${' selected="selected"' if str(botType['id']) == str(b.botType) else ''}>${botType['description']}</option>
					% endfor
				</select></span>
				<span class="botDetail"><label for="bot_autoRun">Auto Run:</label><select name="bot_autoRun" class="text ui-widget-content ui-corner-all">
					<option value="True"${' selected="selected"' if str(b.autoRun) == 'True' else ''}>True</option>
					<option value="False"${' selected="selected"' if str(b.autoRun) == 'False' else ''}>False</option>
				</select></span>
				<span class="botDetail"><label for="bot_redditAuth">Reddit Auth:</label><select name="bot_redditAuth" class="text ui-widget-content ui-corner-all">
					% for redditAuth in redditAuths:
						<option value="${redditAuth['id']}"${' selected="selected"' if str(redditAuth['id']) == str(b.redditAuth) else ''}>${redditAuth['description']}</option>
					% endfor
				</select></span>
				<span class="botDetail"><strong>Status</strong>: ${'<span id="botStatus_{}" class="greenBold">Running</span>'.format(b.id) if b.isRunning() == True else '<span id="botStatus_{}" class="redBold">Stopped</span>'.format(b.id)} <span id="refreshBotStatusButton" onclick="refreshBotStatus();" title="Refresh Bot Status Now" class="ui-icon ui-icon-refresh"></span></span>
				<span class="botControls">
					% if priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id)):
					<button type="submit" name="action" title="Save Bot Settings" value="save_bot" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-disk">Save</button>
					% endif
					<button type="submit" name="action" title="Cancel and Return to Bot Status" value="cancel" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-return">Cancel</button>
					% if priv > 1 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_startstop'.format(b.id)):
					<button type="Submit" name="action" title="Start Bot" value="start" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-play">Start</button>
					<button type="Submit" name="action" title="Stop Bot" value="stop" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-stop">Stop</button></form>
					% endif
					% if priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id)):
					<form id="deleteBot" method="post" action="/bots?bot_id=${str(b.id)}" onsubmit="return confirm('Are you sure you want to permanently delete this bot?');">
						<button type="Submit" name="action" title="Delete Bot" value="delete" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-trash">Delete</button>
					</form>
					% endif
				</span>
			</form>
		</div>
		% if b.detailedState['summary']['text'] != '' and (priv > 0 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_ro'.format(b.id))):
		<div id="botDetailedState_${b.id}" class="botState singleBot">
			<strong>Bot State Summary:</strong> <span id="refreshBotStatusButton" onclick="refreshBotDetailedState();" title="Refresh Bot State Summary Now" class="ui-icon ui-icon-refresh"></span><br />
			<span class="botDetail" id="botDetailedStateSummary_${b.id}">
				${b.detailedState['summary']['html']}
			</span>
		</div>
		% endif
		<% allConfig = config.get_bot_config(bot_id) %>
		<div id="botConfigGrid" class="configGrid layoutGrid">
		% for cat in set(c['category'] for c in allConfig):
			% if any((x for x in allConfig if x['category']==cat)):
				<div class="configCategory gridItem">
					<div class="gridItemContent">
						<form id="${cat}" method="post" action="/bots?bot_id=${b.id}">
						<input type="hidden" name="type" value="${cat}" />
						<span class="configCategoryName">${cat}</span>
						% for x in (x for x in allConfig if x['category']==cat):
							% if x['parent_key'] in ['', None]:
								<label for="${x['category']}|${x['key']}|${x['type']}" title="${x['description'] if x['description'] not in ['', None] else ''}">${x['key']}:</label> 
								% if x['system'] != 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
								<button type="submit" name="action" onclick="return confirm('Are you sure you want to permanently delete this setting?');" value="del_botConfig---${x['category']}|${x['key']}|${x['type']}" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-trash">Delete</button>
								% elif x['system'] == 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
								<span class="ui-icon ui-icon-info" title="System settings cannot be deleted"></span>
								% endif
								% if len(x['options']):
									<select name="${x['category']}|${x['key']}|${x['type']}" class="text ui-widget-content ui-corner-all">
										% for opt in x['options']:
											<option value="${opt}"${' selected="selected"' if str(opt) == str(x['val']) else ''}>${opt}</option>
										% endfor
									</select> 
								% else:
									% if x.get('type','') in ['str','int','',None]:
										<input id="${x['category']}|${x['key']}|${x['type']}" name="${x['category']}|${x['key']}|${x['type']}" value="${str(x['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if x['read_only'] == 'True' else ''}/> 
									% elif x.get('type','') == 'list':
										<input id="${x['category']}|${x['key']}|${x['type']}" name="${x['category']}|${x['key']}|${x['type']}" value="${', '.join(x['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if x['read_only'] == 'True' else ''}/> 
									% endif
								% endif
								% if len(x['subkeys']):
									% for y in (y for y in allConfig if y['parent_key'] == x['key']):
										<span class="indent">
										<label for="${y['category']}|${y['key']}|${y['type']}" title="${y['description'] if y['description'] not in ['', None] else ''}">${y['key']}:</label> 
										% if y['system'] != 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
											<button type="submit" name="action" onclick="return confirm('Are you sure you want to permanently delete this setting?');" value="del_botConfig---${y['category']}|${y['key']}|${y['type']}" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-trash">Delete</button>
										% elif y['system'] == 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
											<span class="ui-icon ui-icon-info" title="System settings cannot be deleted"></span>
										% endif
										% if len(y['options']):
											<select name="${y['category']}|${y['key']}|${y['type']}" class="text ui-widget-content ui-corner-all">
												% for opt in y['options']:
													<option value="${opt}"${' selected="selected"' if str(opt) == str(y['val']) else ''}>${opt}</option>
												% endfor
											</select>
										% else:
											% if y.get('type','') in ['str','int','',None]:
												<input id="${y['category']}|${y['key']}|${y['type']}" name="${y['category']}|${y['key']}|${y['type']}" value="${str(y['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if y['read_only'] == 'True' else ''}/>
											% elif y.get('type','') == 'list':
												<input id="${y['category']}|${y['key']}|${y['type']}" name="${y['category']}|${y['key']}|${y['type']}" value="${', '.join(y['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if y['read_only'] == 'True' else ''}/> 
											% endif
										% endif
										</span>
										% if len(y['subkeys']):
											% for z in (z for z in allConfig if z['parent_key'] == y['key']):
												<span class="indent-twice">
												<label for="${z['category']}|${z['key']}|${z['type']}" title="${z['description'] if z['description'] not in ['', None] else ''}">${z['key']}:</label>  
												% if z['system'] != 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
													<button type="submit" name="action" onclick="return confirm('Are you sure you want to permanently delete this setting?');" value="del_botConfig---${z['category']}|${z['key']}|${z['type']}" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-trash">Delete</button>
												% elif z['system'] == 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
													<span class="ui-icon ui-icon-info" title="System settings cannot be deleted"></span>
												% endif
												% if len(z['options']):
													<select name="${z['category']}|${z['key']}|${z['type']}" class="text ui-widget-content ui-corner-all">
														% for opt in z['options']:
															<option value="${opt}"${' selected="selected"' if str(opt) == str(z['val']) else ''}>${opt}</option>
														% endfor
													</select>
												% else:
													% if z.get('type','') in ['str','int','',None]:
														<input id="${z['category']}|${z['key']}|${z['type']}" name="${z['category']}|${z['key']}|${z['type']}" value="${str(z['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if z['read_only'] == 'True' else ''}/>
													% elif z.get('type','') == 'list':
														<input id="${z['category']}|${z['key']}|${z['type']}" name="${z['category']}|${z['key']}|${z['type']}" value="${', '.join(z['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if z['read_only'] == 'True' else ''}/> 
													% endif
												% endif
												</span>
												% if len(z['subkeys']):
													% for a in (a for a in allConfig if a['parent_key'] == z['key']):
														<span class="indent-thrice">
														<label for="${a['category']}|${a['key']}|${a['type']}" title="${a['description'] if a['description'] not in ['', None] else ''}">${a['key']}:</label>  
														% if a['system'] != 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
															<button type="submit" name="action" onclick="return confirm('Are you sure you want to permanently delete this setting?');" value="del_botConfig---${a['category']}|${a['key']}|${a['type']}" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-trash">Delete</button>
														% elif a['system'] == 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
															<span class="ui-icon ui-icon-info" title="System settings cannot be deleted"></span>
														% endif
														% if len(a['options']):
															<select name="${a['category']}|${a['key']}|${a['type']}" class="text ui-widget-content ui-corner-all">
																% for opt in a['options']:
																	<option value="${opt}"${' selected="selected"' if str(opt) == str(a['val']) else ''}>${opt}</option>
																% endfor
															</select>
														% else:
															% if a.get('type','') in ['str','int','',None]:
																<input id="${a['category']}|${a['key']}|${a['type']}" name="${a['category']}|${a['key']}|${a['type']}" value="${str(a['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if a['read_only'] == 'True' else ''}/>
															% elif a.get('type','') == 'list':
																<input id="${a['category']}|${a['key']}|${a['type']}" name="${a['category']}|${a['key']}|${a['type']}" value="${', '.join(a['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if a['read_only'] == 'True' else ''}/> 
															% endif
														% endif
														</span>
														% if len(a['subkeys']):
															% for c in (c for c in allConfig if c['parent_key'] == a['key']):
																<span class="indent-fource">
																<label for="${c['category']}|${c['key']}|${c['type']}" title="${c['description'] if c['description'] not in ['', None] else ''}">${c['key']}:</label>  
																% if c['system'] != 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
																	<button type="submit" name="action" onclick="return confirm('Are you sure you want to permanently delete this setting?');" value="del_botConfig---${c['category']}|${c['key']}|${c['type']}" class="ui-button ui-widget ui-corner-all ui-button-icon-only button-trash">Delete</button>
																% elif c['system'] == 'True' and (priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id))):
																	<span class="ui-icon ui-icon-info" title="System settings cannot be deleted"></span>
																% endif
																% if len(c['options']):
																	<select name="${c['category']}|${c['key']}|${c['type']}" class="text ui-widget-content ui-corner-all">
																		% for opt in c['options']:
																			<option value="${opt}"${' selected="selected"' if str(opt) == str(c['val']) else ''}>${opt}</option>
																		% endfor
																	</select>
																% else:
																	% if c.get('type','') in ['str','int','',None]:
																		<input id="${c['category']}|${c['key']}|${c['type']}" name="${c['category']}|${c['key']}|${c['type']}" value="${str(c['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if c['read_only'] == 'True' else ''}/>
																	% elif c.get('type','') == 'list':
																		<input id="${c['category']}|${c['key']}|${c['type']}" name="${c['category']}|${c['key']}|${c['type']}" value="${', '.join(c['val']).replace('"','&quot;')}" class="text ui-widget-content ui-corner-all"${' readonly="readonly"' if c['read_only'] == 'True' else ''}/> 
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
							% if priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id)):
							<hr>
							<label for="botConfig_addKey">Add Key:</label><input type="text" name="botConfig_addKey" class="text ui-widget-content ui-corner-all" />
							<label for="botConfig_addVal">Value:</label><input type="text" name="botConfig_addVal" class="text ui-widget-content ui-corner-all" />
							<label for="botConfig_addDataType">Data Type:</label>
							<select name="botConfig_addDataType" class="text ui-widget-content ui-corner-all">
								<option value="str">String</option>
								<option value="int">Integer</option>
								<option value="bool">Boolean</option>
								<option value="list">List (comma-separated)</option>
							</select>
							<button type="submit" name="action" value="save_botConfig" class="ui-button ui-widget ui-corner-all button-disk">Save</button>
							% endif
						</form>
					</div>
				</div>
			% endif
		% endfor
		% else:
		Bot not found.
		% endif
		% if priv > 2 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_rw'.format(b.id)):
		<div class="configCategory gridItem">
			<div class="gridItemContent">
				<form id="new_botConfigCat" method="post" action="/bots?bot_id=${b.id}">
				<input type="hidden" name="type" value="New" />
				<span class="configCategoryName">Add Settings Category</span>
					<label for="botConfig_add_cat_name">Category Name:</label> <input id="botConfig_add_cat_name" name="botConfig_add_cat_name" value="" class="text ui-widget-content ui-corner-all" />
					<label for="botConfig_add_cat_key">Add Key:</label> <input type="text" name="botConfig_add_cat_key" class="text ui-widget-content ui-corner-all" />
					<label for="botConfig_add_cat_val">Value:</label> <input type="text" name="botConfig_add_cat_val" class="text ui-widget-content ui-corner-all" />
					<label for="botConfig_add_cat_dataType">Data Type:</label>
					<select name="botConfig_add_cat_dataType" class="text ui-widget-content ui-corner-all">
						<option value="str">String</option>
						<option value="int">Integer</option>
						<option value="bool">Boolean</option>
						<option value="list">List (comma-separated)</option>
					</select>
					<button type="submit" name="action" value="botConfig_add_cat" class="ui-button ui-widget ui-corner-all button-disk">Create</button>
				</form>
			</div>
		</div>

		<div class="configCategory gridItem">
			<div class="gridItemContent">
				<form id="upload_botConfig" method="post" action="/bots?bot_id=${b.id}" enctype="multipart/form-data">
				<span class="configCategoryName">Upload Config JSON</span>
					<div id="controlgroup" class="ui-widget ui-controlgroup ui-controlgroup-vertical">
						<div id="botConfig_upload_file_div" class="ui-button ui-widget ui-corner-all button-folder-open"><span id="botConfig_upload_selected_file">Select a file...</span></div><input type="file" id="botConfig_upload_file_input" name="botConfig_upload_file" />
						<input type="checkbox" id="botConfig_upload_replace" name="botConfig_upload_replace" value="True" /><label for="botConfig_upload_replace">Replace Existing Values</label>
						<input type="checkbox" id="botConfig_upload_clean" name="botConfig_upload_clean" value="True" /><label for="botConfig_upload_clean">Delete All Settings Before Importing</label>
					</div><br />
					<button type="submit" name="action" value="botConfig_upload" class="ui-button ui-widget ui-corner-all button-disk">Upload</button>
				</form>
			</div>
		</div>
		% endif

		% if priv > 0 or user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_bot_{}_ro'.format(b.id)):
		<div class="configCategory gridItem">
			<div class="gridItemContent">
				<form id="export_botConfig" method="post" action="/bots?bot_id=${b.id}">
				<span class="configCategoryName">Export Config JSON</span>
					<button type="submit" name="action" value="botConfig_export" class="ui-button ui-widget ui-corner-all button-save">Export</button>
				</form>
			</div>
		</div>
		% endif
		</div>
	% endif
	% else:
	No bots found.
	% endif
</%block>
<%block name="pagejs">
% if priv > 0 or explicitPrivCount > 0:
<script>
	function refreshBotStatus(extraParam='') {
		if(extraParam != ''){sep = '&'}
		else{sep = ''}
		$.ajax({
			url: '/botstatus?' + extraParam + sep + '${'botId={}'.format(bot_id) if bot_id != None else ''}', 
			success: function(data) {
				var botStatus = JSON.parse(data)
				Object.keys(botStatus).forEach( function(botId) {
					if (botStatus.hasOwnProperty(botId)) {
						var oldStatus = $('#botStatus_'+botId).html()
						if (botStatus[botId] != oldStatus) {
							$('#botStatus_'+botId).html(botStatus[botId]);
							if (botStatus[botId] == 'Running') {
								$('#botStatus_'+botId).removeClass('redBold').addClass('greenBold');
								$('#botStatus_'+botId).effect("highlight", {color:'#0f0'}, 3000);
							}
							else {
								$('#botStatus_'+botId).removeClass('greenBold').addClass('redBold');
								$('#botStatus_'+botId).effect("highlight", {color:'#f00'}, 3000);
							}
						} else {
							$('#botStatus_'+botId).effect("highlight", {color:'#ddd'}, 500);
						}
					}
				});
			}
		});
	}
	% if bot_id is not None:
	function refreshBotDetailedState(extraParam='') {
		if(extraParam != ''){sep = '&'}
		else{sep = ''}
		$.ajax({
			url: '/botdetailedstate?' + extraParam + sep + '${'botId={}'.format(bot_id) if bot_id != None else ''}', 
			success: function(data) {
				var botStatus = JSON.parse(data)
				Object.keys(botStatus).forEach( function(botId) {
					if (botStatus.hasOwnProperty(botId)) {
						var oldStatus = $('#botDetailedStateSummary_'+botId).html()
						if (botStatus[botId]['html'] != oldStatus) {
							$('#botDetailedStateSummary_'+botId).html(botStatus[botId]['html']);
							$('#botDetailedStateSummary_'+botId).effect("highlight", {color:'#ddd'}, 3000);
						} else {
							$('#botDetailedStateSummary_'+botId).effect("highlight", {color:'#ddd'}, 500);
						}
					}
				});
			}
		});
	}
	% endif
	$(document).ready(function() {
		// bot status auto refresh settings
		if (Cookies.get('rb_autoRefreshInterval') != undefined) {
			$("#botStatus_refreshInterval").val(Cookies.get('rb_autoRefreshInterval'));
		}
		if ($("#botStatus_refreshInterval").val() == '0') {
			var refreshTimeout;
			% if bot_id is not None:
			var refreshTimeout_detailedState;
			% endif
		} else {
			var refreshTimeout = setInterval(refreshBotStatus, parseInt($("#botStatus_refreshInterval").val())*1000);
			% if bot_id is not None:
			var refreshTimeout_detailedState = setInterval(refreshBotDetailedState, parseInt($("#botStatus_refreshInterval").val())*1000);
			% endif
		}
		botStatus_refreshInterval.onchange = function() {
												clearInterval(refreshTimeout);
												% if bot_id is not None:
												clearInterval(refreshTimeout_detailedState);
												% endif
												if ($("#botStatus_refreshInterval").val() == '0') {
													// do nothing
												} else {
													clearInterval(refreshTimeout);
													refreshTimeout = setInterval(refreshBotStatus, parseInt($('#botStatus_refreshInterval').val())*1000);
													% if bot_id is not None:
													clearInterval(refreshTimeout_detailedState);
													refreshTimeout_detailedState = setInterval(refreshBotDetailedState, parseInt($('#botStatus_refreshInterval').val())*1000);
													% endif
												}
												Cookies.set('rb_autoRefreshInterval', $("#botStatus_refreshInterval").val());
											};

		//bot config json import button
		$("#botConfig_upload_file_div").on('click', function (event) {
			$("#botConfig_upload_file_input").click();
		});
		$("#botConfig_upload_file_input").change(function(){
			$("#botConfig_upload_selected_file").text($(this).val().replace("C:\\fakepath\\",""));
		});
	});
</script>
% endif
</%block>
