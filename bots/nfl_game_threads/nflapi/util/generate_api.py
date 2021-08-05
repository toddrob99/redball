import json
import sys

from sgqlc.introspection import variables, query

from nflapi.nfl import NFL


def main():
    nfl = NFL(ua=('nflapi schema generator'))
    data = nfl.endpoint(query, variables())
    with open(sys.argv[1], 'w') as fp:
        json.dump(data, fp)


if __name__ == '__main__':
    main()
