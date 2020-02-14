<%inherit file="base.mako" />
<%!
	import redball
%>
<%block name="errorcontainer_hide"></%block>
<%block name="errors">
	${self.errors}
</%block>
<%def name="get_traceback()">
	<blockquote>
		${traceback}
	</blockquote>
</%def>
<%block name="content">
	${get_traceback() if redball.DEV else ''}
</%block>