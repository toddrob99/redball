<% 
    import cherrypy
    import redball
    from redball import config, user
    if cherrypy.session.get("_cp_username") and cherrypy.session["_cp_username"] in redball.LOGGED_IN_USERS.keys():
        user.refresh_user_privileges(cherrypy.session["_cp_username"])
    auth_type = config.get_sys_config(category="Web/Security", key="AUTH_TYPE")
    wideOpen = auth_type[0]["val"] == "None"
    basicAuth = auth_type[0]["val"] == "Basic"
    if wideOpen:
        cherrypy.session["_cp_username"] = "authOff"
    elif basicAuth:
        cherrypy.session["_cp_username"] = "basicAuth"
%>
<%page args="errors='', info='', errorcontainer_hide=' class=hide', infocontainer_hide=' class=hide'" />
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>${title} | <%block name="siteHeader">redball</%block></title>
<link href="/css/style.css" rel="stylesheet" type="text/css" />
<script src="//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
<link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css" />
<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
<script src="//cdn.jsdelivr.net/npm/js-cookie@2/src/js.cookie.min.js"></script>
<script>
$( function() {
	//form styles
	$(".button-key").button({
	  icon: "ui-icon-key"
	});
	$(".button-close").button({
	  icon: "ui-icon-close"
	});
	$(".button-return").button({
	  icon: "ui-icon-arrowreturnthick-1-w"
	});
	$(".button-disk").button({
	  icon: "ui-icon-disk"
	});
	$(".button-save").button({
	  icon: "ui-icon-arrowstop-1-s"
	});
	$(".button-play").button({
	  icon: "ui-icon-play"
	});
	$(".button-stop").button({
	  icon: "ui-icon-stop"
	});
	$(".button-gear").button({
	  icon: "ui-icon-gear"
	});
	$(".button-wrench").button({
	  icon: "ui-icon-wrench"
	});
	$(".button-refresh").button({
	  icon: "ui-icon-refresh"
	});
	$(".button-trash").button({
	  icon: "ui-icon-trash"
	});
	$(".button-folder-open").button({
	  icon: "ui-icon-folder-open"
	});
	$( ".ui-controlgroup-horizontal" ).controlgroup({
	  "direction": "horizontal"
	});
	$( ".ui-controlgroup-vertical" ).controlgroup({
	  "direction": "vertical"
	});
	
	//tooltip
    $( document ).tooltip();
} );
//grid layout helper functions -- taking some help from Rahul @ https://w3bits.com/css-grid-masonry/
function resizeGridItem(item){
	var grid = $(".layoutGrid").first(),
		rowGap = parseInt($(grid).css('grid-row-gap')),
		rowHeight = parseInt($(grid).css('grid-auto-rows')),
		gridItemExtraHeight = parseInt($(item).outerHeight(true)-$(item).height());
	$(item).css('grid-row-end', 'span '+Math.ceil(($(item).find('.gridItemContent').outerHeight(true)+gridItemExtraHeight+rowGap)/(rowHeight+rowGap)));
}
function resizeAllGridItems(){
	$(".gridItem").each(function(){
		resizeGridItem($(this));
	});
}
$(document).ready(function() {
	resizeAllGridItems();
});
$(window).resize(function() {
	resizeAllGridItems();
});
</script>
<%block name="pagejs"></%block>
</head>
<body>
<div id="loadingcontainer" class="hide"><div id="blackout"></div><div id="loadingdiv"><br /><img src="/img/spinner.gif" /><br /><span id="loadingtext">Loading...</span></div></div>
<header role="banner">
	<div id="loginstatus">
		<div id="userbox">
			${'' if wideOpen or basicAuth else '{}<a href="/password" title="Change Password"><span class="ui-icon ui-icon-wrench"></span></a><a href="/logout"><span class="ui-icon ui-icon-locked" title="Logout"></span></a>'.format(cherrypy.session.get("_cp_username")) if cherrypy.session.get("_cp_username") else '<a href="/login"><span class="ui-icon ui-icon-locked"></span>Login</a>'}
		</div>
	</div>
	<div id="logo"><a href="/" class="logo"><img src="/img/redball.png" height="40" width="40" style="vertical-align:middle"> ${self.siteHeader()}</a></div>
	<div id="menu">
		<ul class="menu">
			% if cherrypy.session.get("_cp_username"):
				% if 'Bot' in title and 'System Configuration' not in title:
				<a href="/"><li class="active">Bots</li></a>
				% else:
				<a href="/"><li>Bots</li></a>
				% endif
				% if user.check_privilege(cherrypy.session["_cp_username"], 'rb_config_ro'):
				% if 'System Configuration' in title:
				<a href="/config"><li class="active">System Config</li></a>
				% else:
				<a href="/config"><li>System Config</li></a>
				% endif
				% endif
				% if user.check_privilege(cherrypy.session["_cp_username"], 'rb_log_ro'):
				% if 'Logs' in title:
				<a href="/logs"><li class="active">Logs</li></a>
				% else:
				<a href="/logs"><li>Logs</li></a>
				% endif
				% endif
			% else:
				<a href="/login"><li><span class="ui-icon ui-icon-locked"></span>Login</li></a>
			% endif
		</ul>
	</div>
</header>
<div id="pageconainer">
	<div id="pageheader">
		<%block name="topright"></%block>
		<h2>${title}</h2>
	</div>
	<div id="errorcontainer" class="ui-widget ui-state-error ui-corner-all${errorcontainer_hide}" style="padding: 0 .7em;">
		% if errors != '':
			<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>${errors}<%block name="errormessage"></%block></p>
		% endif
	</div>
	<div id="infocontainer" class="ui-widget ui-state-highlight ui-corner-all${infocontainer_hide}" style="padding: 0 .7em;">
		% if info != '':
			<p><span class="ui-icon ui-icon-info" style="float: left; margin-right: .3em;"></span>${info}<%block name="infomessage"></%block></p>
		% endif
	</div>
	<div id="main">
		<%block name="content"></%block>
	</div>
</div>
<div id="footer">
	${redball.APP_NAME} v${redball.__version__}
	 | <a href="https://github.com/toddrob99/redball" target="_blank">Source/Issues</a>
	 | <a href="https://reddit.com/r/redball" target="_blank">Reddit</a>
	 | <a href="https://discord.gg/j5N8g4a" target="_blank">Discord</a>
	 | <a href="https://github.com/toddrob99/redball/blob/master/LICENSE" target="_blank">License</a>
	 | <span title="This website uses cookies for session management and to enhance your experience. By continuing to use this website, you agree to the use of cookies." class="ui-icon ui-icon-notice"></span>
	 | &copy; 2019-2024 Todd Roberts
</div>

</body>
</html>
