
import os
import platform
import sys


def get_installed_packes():
    dist, dist_version, dist_name = platform.dist()

    if dist == "fedora":
        import yum
        yb = yum.YumBase()
        pkgs = yb.rpmdb.returnPackages()
        #pl = yb.pkgSack.returnNewestByNameArch(patterns=sys.argv[1:])
        # print dir(pl)
        data = []
        for it in pkgs:
            data.append(
                {"name": it.name, "version": it.version,
                 "rel": it.rel, "arch": it.arch})
        return data

    if dist == "debian":
        import apt
        c = apt.Cache()
        data = []
        for it in c:
            if it.is_installed:
                for itt in it.versions:
                    data.append(
                        {"name": it.name,
                         })
        return data


print get_installed_packes()
