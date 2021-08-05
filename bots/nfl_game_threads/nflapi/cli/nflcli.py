#!/usr/bin/env python
import logging
from functools import update_wrapper

import click
import pendulum

from nflapi import NFL
from nflapi.const import DIVISION_NAMES
from nflapi.__version__ import __version__ as VERSION

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def nflobj(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        ctx.invoke(f, ctx.obj['nfl'], *args, **kwargs)

    return update_wrapper(new_func, f)


@click.version_option(version=VERSION)
@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--verbose/--quiet', default=False)
@click.pass_context
def nflcli(ctx, verbose):
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.WARN
    logging.basicConfig(level=level)
    ctx.obj['nfl'] = NFL(ua=('nflapi cli'))


@nflcli.command(short_help="Display the current week")
@nflobj
def current_week(nfl: NFL):
    cw = nfl.schedule.current_week()
    logging.debug("Current week: %r", cw)
    print("{w.current_season[default]} {w.current_season_type[default]} {w.current_week[default]}".format(w=cw))


@nflcli.command(short_help="Show schedule for a given week")
@nflobj
def schedule(nfl: NFL):
    cw = nfl.schedule.current_week()
    print("{w.season_value} {w.season_type} {w.week_value}".format(w=cw))

    games = nfl.game.week_games(cw.week_value, cw.season_type,
                                cw.season_value)
    tz = pendulum.tz.local_timezone()
    for game in sorted(games, key=lambda g: g.game_time):
        localtime = pendulum.instance(game.game_time).astimezone(tz)
        print(("{t:%Y-%m-%d %H:%M %Z} "
               "{g.away_team.abbreviation:3s} "
               "@ "
               "{g.home_team.abbreviation:3s}").format(
            g=game, t=localtime))


@nflcli.command(short_help="List standings")
@nflobj
def standings(nfl: NFL):
    team_records = nfl.standings.current()

    groups = {}
    for team, team_record in team_records:
        group = team.division
        if group not in groups:
            groups[group] = []
        groups[group].append((team, team_record))
    for group, teams in sorted(groups.items(), key=lambda g: g[0]):
        group_name = DIVISION_NAMES.get(group, group)
        print(group_name + "\n" + ("=" * len(group_name)))
        print("Team            W  L  T  PCT")
        for team, team_record in sorted(teams, key=lambda t: t[1].division_rank):
            print(("{t.nick_name:14} {tr.overall_win:2d} {tr.overall_loss:2d} "
                   "{tr.overall_tie:2d}  {tr.overall_pct:1.3f}")
                  .format(t=team, tr=team_record))
        print()


@nflcli.command(short_help="Team info")
@click.argument('abbr')
@nflobj
def team(nfl: NFL, abbr):
    def selector(team):
        team.full_name()
        team.venues().display_name()
        team.division()
        team.conference()

    team = nfl.team.lookup(abbr, select_fun=selector)
    print(team.full_name)
    print(team.conference)
    print(team.division)
    print(team.venues[0].display_name)


def main():
    nflcli(obj={})


if __name__ == "__main__":
    main()
