from __future__ import absolute_import

import os
import os.path as osp

from bench.hub.config import Config, get_config, set_config
from bench.hub.bench  import Bench
from bench.hub.util   import assign_if_empty, which
from bench.hub.setup  import setup_procfile

def init(bench = None, group = None, validate = False, reinit = False):
    benches = [Bench(path) for path in bench if check_bench(path, raise_err = validate)]
    group   = assign_if_empty(group, os.getcwd())

    for path in os.listdir(group):
        abspath = osp.join(group, path)
        if check_bench(abspath, raise_err = validate):
            bench = Bench(abspath)
            benches.append(bench)
            
    if not benches:
        raise ValueError('No benches found at {path}'.format(path = group))

    paths = list()
    for bench in benches:
        if not bench.has_app('erpnext', installed = True) and validate:
            raise ValueError('{bench} does not have erpnext for hub installed.'.format(
                bench = bench
            ))
        else:
            # TODO: Check if site has Hub enabled.
            paths.append(bench.path)
            
    set_config('benches', paths)

    setup_procfile(reinit = reinit)

def migrate():
    benches = [Bench(path) for path in get_config('benches')]


def start(daemonize = False):
    if daemonize:
        pass
    else:
        procfile = setup_procfile()
        honcho   = which('honcho')

        args     = [honcho, 'start',
            '-f', procfile
        ]

        os.execv(honcho, args)