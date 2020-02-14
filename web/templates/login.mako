<%inherit file="base.mako" />

<%block name="content">
	<form id="login" method="post" action="/login${'?r={}'.format(r) if r else ''}">
	<div class="login">
		<label for="login|userid">User ID:</label>
		<input type="text" id="login|userid" name="login|userid" value="" class="text ui-widget-content ui-corner-all" />
		<label for="login|password">Password:</label>
		<input type="password" id="login|password" name="login|password" value="" class="text ui-widget-content ui-corner-all" /><br />
		<button type="submit" name="action" value="login" class="button-key ui-button ui-corner-all ui-widget">Login</button>
	</div>
	</form>
</%block>
