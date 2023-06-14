<%page args="include_wc=False,wc_num=5" />
## Standings for myTeam's division only:
|${data[0]['myTeam']['division']['abbreviation']} Rank|Team|W|L|GB (E#)|WC Rank|WC GB (E#)|
|:--|:--|:--|:--|:--|:--|:--|
% for t in data[0]['standings'][data[0]['myTeam']['division']['id']]['teams']:
% if t['team_id'] == data[0]['myTeam']['id']:
|**${t['div_rank']}**|**[${t['name']}](${data[0]['teamSubs'][t['team_id']]})**|**${t['w']}**|**${t['l']}**|**${t['gb']} (${t['elim_num']})**|**${t['wc_rank']}**|**${t['wc_gb']} (${t['wc_elim_num']})**|
% else:
|${t['div_rank']}|[${t['name']}](${data[0]['teamSubs'][t['team_id']]})|${t['w']}|${t['l']}|${t['gb']} (${t['elim_num']})|${t['wc_rank']}|${t['wc_gb']} (${t['wc_elim_num']})|
% endif
% endfor
% if include_wc:
## Wild Card standings for myTeam's league
<%
    wc_standings = []
    for div_id, div_standings in data[0]['standings'].items():
        if div_standings.get("div_name").split()[0] == data[0]['myTeam']['league']['nameShort']:
            for div_st in div_standings.get("teams", []):
                if div_st.get("wc_rank") != "-" and int(div_st.get("wc_rank", 0)) <= wc_num:
                    wc_standings.append(div_st)
    wc_standings = sorted(wc_standings, key=lambda t: int(t["wc_rank"]))
%>\
%   if len(wc_standings):

|WC Rank|Team|W|L|WC GB (E#)|
|:--|:--|:--|:--|:--|
%       for t in wc_standings:
%           if t['team_id'] == data[0]['myTeam']['id']:
|**${t['wc_rank']}**|**[${t['name']}](${data[0]['teamSubs'][t['team_id']]})**|**${t['w']}**|**${t['l']}**|**${t['wc_gb']} (${t['wc_elim_num']})**|
%           else:
|${t['wc_rank']}|[${t['name']}](${data[0]['teamSubs'][t['team_id']]})|${t['w']}|${t['l']}|${t['wc_gb']} (${t['wc_elim_num']})|
%           endif
%       endfor
%   endif
% endif
## Remove %doc tag and corresponding /%doc tag below to uncomment
<%doc>
## Standings for other divisions in myTeam's league
% for div in (data[0]['standings'][x] for x in data[0]['standings'] if data[0]['standings'][x]['div_name'].split()[0] == data[0]['myTeam']['league']['nameShort'] and data[0]['standings'][x]['div_name'] != data[0]['myTeam']['division']['name']):

|${''.join([w[0] for w in div['div_name'].split()])} Rank|Team|W|L|GB (E#)|WC Rank|WC GB (E#)|
|:--|:--|:--|:--|:--|:--|:--|:--|
% for t in div['teams']:
|${t['div_rank']}|[${t['name']}](${data[0]['teamSubs'][t['team_id']]})|${t['w']}|${t['l']}|${t['gb']} (${t['elim_num']})|${t['wc_rank']}|${t['wc_gb']} (${t['wc_elim_num']})|
% endfor
% endfor
</%doc>
## Remove %doc tag and corresponding /%doc tag below to uncomment
<%doc>
## Standings for other league
% for div in (data[0]['standings'][x] for x in data[0]['standings'] if data[0]['standings'][x]['div_name'].split()[0] != data[0]['myTeam']['league']['nameShort']):

|${''.join([w[0] for w in div['div_name'].split()])} Rank|Team|W|L|GB (E#)|WC Rank|WC GB (E#)|
|:--|:--|:--|:--|:--|:--|:--|:--|
% for t in div['teams']:
|${t['div_rank']}|[${t['name']}](${data[0]['teamSubs'][t['team_id']]})|${t['w']}|${t['l']}|${t['gb']} (${t['elim_num']})|${t['wc_rank']}|${t['wc_gb']} (${t['wc_elim_num']})|
% endfor
% endfor
</%doc>