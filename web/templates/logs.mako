<%inherit file="base.mako" />
<%! 
	import cherrypy
	import os
	import redball
	from redball import user

	if user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_log_rw'):
		priv = 2
	elif user.check_privilege(cherrypy.session.get("_cp_username"), 'rb_log_ro'):
		priv = 1
	else:
		priv = 0
%>

<%block name="content">
	% if priv > 0:
	<% logDirList = os.listdir(redball.LOG_PATH) %>
	<% used = [] %>
	<div id="logsConfigGrid" class="logsGrid layoutGrid">
		<div class="logs gridItem">
			<div class="gridItemContent">
				<span class="logType">System</span>
				% for f in (f for f in logDirList if 'redball.log' in f):
					<span class="logFile">
						<a href="/logs?action=downloadLog&logId=${f}" class="ui-icon ui-widget ui-icon-disk"></a> 
						% if f[-4:] != '.log' and priv > 1:
							<a href="/logs?action=deleteLog&logId=${f}" class="ui-icon ui-widget ui-icon-trash" onclick="return confirm('Are you sure you want to permanently delete this log file?');"></a>
						% endif
						${f}
					</span>
					<% used.append(f) %>
				% endfor
			</div>
		</div>
		<div class="logs gridItem">
			<div class="gridItemContent">
				<span class="logType">Webserver</span>
				% for f in (f for f in logDirList if 'access.log' in f or 'error.log' in f):
					<span class="logFile">
						<a href="/logs?action=downloadLog&logId=${f}" class="ui-icon ui-widget ui-icon-disk"></a>
						% if f[-4:] != '.log' and priv > 1:
							<a href="/logs?action=deleteLog&logId=${f}" class="ui-icon ui-widget ui-icon-trash" onclick="return confirm('Are you sure you want to permanently delete this log file?');"></a>
						% endif
						${f}
					</span>
					<% used.append(f) %>
				% endfor
			</div>
		</div>
		% for b in redball.BOTS.values():
			% if any(f for f in logDirList if f.find('bot-{}-'.format(b.id))!=-1):
				<div class="logs gridItem">
					<div class="gridItemContent">
						<span class="logType">${b.name} (#${str(b.id)})</span>
						% for f in (f for f in logDirList if f.find('bot-{}-'.format(b.id))!=-1):
							<span class="logFile">
								<a href="/logs?action=downloadLog&logId=${f}" class="ui-icon ui-widget ui-icon-disk"></a>
								% if (f[-4:] != '.log' or b.name.replace(' ','-') not in f) and priv > 1:
									<a href="/logs?action=deleteLog&logId=${f}" class="ui-icon ui-widget ui-icon-trash" onclick="return confirm('Are you sure you want to permanently delete this log file?');"></a>
								% endif
								${f}
							</span>
						<% used.append(f) %>
						% endfor
					</div>
				</div>
			% endif
		% endfor
		% if len(used) < len(logDirList):
			<div class="logs gridItem">
				<div class="gridItemContent">
					<span class="logType">Other</span>
					% for f in (f for f in logDirList if f not in used):
						<span class="logFile">
							<a href="/logs?action=downloadLog&logId=${f}" class="ui-icon ui-widget ui-icon-disk"></a>
							% if priv > 1:
							<a href="/logs?action=deleteLog&logId=${f}" class="ui-icon ui-widget ui-icon-trash" onclick="return confirm('Are you sure you want to permanently delete this log file?');"></a>
							% endif
							${f}
						</span>
						<% used.append(f) %>
					% endfor
				</div>
			</div>
		% endif
	</div>
% else:
Insufficient privileges.
% endif
</%block>