import json
import os
import subprocess

import click

from key import KEY

def query_ip(ip: str='check'):
    api = 'http://api.ipstack.com/'
    url = f'{api}{ip}?access_key={KEY}'
    cmd_lst = ['curl', url]
    env_cp = os.environ.copy()
    proc = subprocess.Popen(cmd_lst,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env_cp)
    try:
        outs, errors = proc.communicate(timeout=60)
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errors = None, None
        print(f"Time out when exec {' '.join(cmd_lst)}")
    if outs is not None:
        outs_js = json.loads(outs)
        for key, value in outs_js.items():
            print(f"{key}: {value}")

@click.command()
@click.argument('ip', default='check')
def main(ip):
    query_ip(ip)

if __name__ == "__main__":
    main()
