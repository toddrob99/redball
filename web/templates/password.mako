<%inherit file="base.mako" />
<%! 
	import cherrypy
	import redball
	from redball import user
%>

<%block name="content">
	<%
		u = (
			user.get_user_info(uid=user_id)
			if user_id not in [None, UNDEFINED]
			else
			user.get_user_info(userid=cherrypy.session.get("_cp_username"))
		)
	%>
	<form id="pwchange" method="post" action="/password?user_id=${u['id']}">
		<input type="hidden" name="userid" value="${u['userid']}" />
	<div class="changePassword">
		<span class="configCategoryName">${u['userid'].capitalize()}</span>
		<label for="password|current">${'Your ' if u['userid'] != cherrypy.session.get("_cp_username") else ''}Current Password:</label><input type="password" id="password|current" name="password|current" value="" class="text ui-widget-content ui-corner-all" />
		<label for="password|new">${u['userid'].capitalize()+"'s " if u['userid'] != cherrypy.session.get("_cp_username") else ''}New Password:</label><input type="password" id="password|new" name="password|new" value="" class="text ui-widget-content ui-corner-all" />
		<label for="password|confirm">Confirm:</label><input type="password" id="password|confirm" name="password|confirm" value="" class="text ui-widget-content ui-corner-all" />
		<button type="submit" name="action" value="changePassword" class="button-key ui-button ui-corner-all ui-widget">Change ${u['userid'].capitalize()+"'s " if u['userid'] != cherrypy.session.get("_cp_username") else ''}Password</button>
	</div>
	</form>
</%block>
