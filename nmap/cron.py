import subprocess
import os
import re
import json
import time
from django.conf import settings


CDIR = os.path.dirname(os.path.realpath(__file__))
SCHEDFILES = os.listdir('{}/schedule/'.format(CDIR))

def gethours(schedule):
    return {
        '1h': 3600,
        '1d': 86400,
        '1w': 604800,
        '1m': 2592000,
    }[schedule]

for i in SCHEDFILES:
    if re.search(r'^[a-f0-9]{32,32}\.json$', i.strip()) is not None:
        with open('{}/schedule/{}'.format(CDIR, i)) as fp:
            s = json.load(fp)
        p = s['params']
        n = s['number']

        nextrun = s['lastrun'] + gethours(p['frequency'])
        if nextrun <= time.time():
            n += 1
            print("[RUN]   scan:{} id:{} (nextrun:{} / now:{})".format(
                p['filename'],
                n,
                nextrun,
                time.time(),
                ))
            lastrun = time.time()

            subprocess.run([
                'nmap',
                p['params'],
                '--script={}/nse/'.format(CDIR),
                '-oX',
                '/tmp/{}_{}.active'.format(n, p['filename']),
                p['target'],
                ])
            time.sleep(5)
            os.rename(
                '/tmp/{}_{}.active'.format(n, p['filename']),
                '/opt/xml/webmapsched_{}_{}'.format(lastrun, p['filename']),
                )
            print(
                subprocess.check_output([
                    'ls', '-lart',
                    '/opt/xml/webmapsched_{}_{}'.format(lastrun, p['filename']),
                    ])
                )
            print(
                subprocess.check_output([
                    'python3', '{}/cve.py'.format(CDIR),
                    'webmapsched_{}_{}'.format(lastrun, p['filename'])
                    ])
                )

            with open('{}/schedule/{}'.format(CDIR, i), 'w') as fp:
                fp.write(json.dumps(s, indent=4))

            time.sleep(10)
        else:
            print("[SKIP]  scan:{} id:{} (nextrun:{} / now:{})".format(
                p['filename'],
                n,
                nextrun,
                time.time(),
                ))
