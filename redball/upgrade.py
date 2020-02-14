#!/usr/bin/env python

from redball import database, logger
import time

log = logger.get_logger(
    logger_name="redball.upgrade", log_level="DEBUG", propagate=True
)


def upgrade_database(toVer=None):
    # toVer = database version to upgrade to
    # returns True if version is satisfactory, False if error
    toVer = toVer if toVer else max(upgradeScripts.keys())
    fromVer = database.get_database_version(logg=log)

    if fromVer == toVer:
        log.info("Database is up to date (version: {})!".format(fromVer))
        return True
    elif fromVer > toVer:
        log.warning(
            "Current version ({}) is higher than requested version ({}). Someting's wrong but there's nothing to upgrade...".format(
                fromVer, toVer
            )
        )
        return True
    else:
        log.info(
            "Current database version {}; desired version: {}.".format(fromVer, toVer)
        )
        log.info("Creating a backup of the database...")
        database.backup_database(logg=log, manual=False)

        con = database.get_con(logg=log)
        cur = database.get_cur(con=con, logg=log)
        while fromVer < toVer:
            # Apply upgrade scripts one version at a time until the database is up-to-date
            log.info(
                "Upgrading database from version {} to version {}...".format(
                    fromVer, fromVer + 1
                )
            )
            if len(upgradeScripts.get(fromVer + 1, [])) > 0:
                results = database.db_qry(
                    query=upgradeScripts[fromVer + 1],
                    con=con,
                    cur=cur,
                    commit=False,
                    closeAfter=False,
                    logg=log,
                )
                if None in results:
                    log.error(
                        "One or more database upgrade queries failed: {}".format(
                            results
                        )
                    )
                    # Upgrade scripts failed. Do not commit and do not continue.
                    return False
                else:
                    con.commit()
                    fromVer += 1
                    log.debug("Database upgraded to version {}.".format(fromVer))

        con.close()
        log.debug("Database upgrade process is complete.")
        return True


upgradeScripts = {
    1: [
        "UPDATE rb_meta SET val='1', lastUpdate='{}' WHERE key='dbVersion';".format(
            time.time()
        ),
    ]
}
