## Game Highlights
<%
    sortedHighlights = []
    if not data[gamePk]['schedule']['content'].get('highlights',{}).get('highlights') or data[gamePk]['schedule']['content'].get('highlights',{}).get('highlights',{}).get('items'):
        return
    else:
        unorderedHighlights = {}
        for i in (x for x in data[gamePk]['schedule']['content']['highlights']['highlights']['items'] if isinstance(x,dict) and x['type']=='video'):
            unorderedHighlights.update({i['date'] : i})

        for x in sorted(unorderedHighlights):
            sortedHighlights.append(unorderedHighlights[x])
%>
% if len(sortedHighlights) > 0:
|Team|Highlight|
|:--|:--|
% for p in sortedHighlights:
<%
    team_id = int(next((t.get('value') for t in p.get('keywordsAll',{}) if t.get('type')=='team_id'),0))
    team_abbrev = next((b['team']['abbreviation'] for a,b in data[gamePk]['schedule']['teams'].items() if b['team']['id']==team_id),'')
    hdLink = next((v.get('url') for v in p.get('playbacks',{}) if v.get('name')=='mp4Avc'),'')
%>\
|[${team_abbrev}](${data[0]['teamSubs'].get(team_id, '')})\
|[${p['headline']} (${p.get('duration', '?:??')})](${hdLink})|
##|[${p['description']} (${p['duration']})](${hdLink})|
% endfor
% endif
