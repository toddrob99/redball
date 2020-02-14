## Standings for myTeam's division only:
|${data[0]['myTeam']['division']['abbreviation']} Rank|Team|W|L|GB (E#)|WC Rank|WC GB (E#)|
|:--|:--|:--|:--|:--|:--|:--|:--|
% for t in data[0]['standings'][data[0]['myTeam']['division']['id']]['teams']:
% if t['team_id'] == data[0]['myTeam']['id']:
|**${t['div_rank']}**|**[${t['name']}](${data[0]['teamSubs'][t['team_id']]})**|**${t['w']}**|**${t['l']}**|**${t['gb']} (${t['elim_num']})**|**${t['wc_rank']}**|**${t['wc_gb']} (${t['wc_elim_num']})**|
% else:
|${t['div_rank']}|[${t['name']}](${data[0]['teamSubs'][t['team_id']]})|${t['w']}|${t['l']}|${t['gb']} (${t['elim_num']})|${t['wc_rank']}|${t['wc_gb']} (${t['wc_elim_num']})|
% endif
% endfor
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