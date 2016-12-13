import click
from requests_futures.sessions import FuturesSession
import logging
import json
from collections import defaultdict

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)

MACHINES = defaultdict(int)
COOKIES = defaultdict(int)

def echo_out(sess, resp):
    j = json.loads(resp.text)
    machine_id = j["debug"]["machine_id"]
    log.info(machine_id)
    MACHINES[machine_id] +=1
    for c in resp.cookies:
        COOKIES[c.value] +=1

@click.command()
@click.option('-u', '--url', help='http(s) request to make', prompt=True)
@click.option('-t', '--tries', default=1, help='number of tries to make')
@click.option('-c', '--concurrency', default=1, help='num of concurrent reqs' )
def make_requests(url, tries, concurrency):

    # Cookie
    cookies = {"X-Mapping-rrsqbjcb": "06a13f0a788e803fcc56e78802891a26"}


    log.info("=== Starting Run with params ================================")
    log.info("url: {}".format(url))
    log.info("tries: {}".format(tries))
    log.info("concurrency: {}".format(concurrency))
    log.info("cookies: {}".format(cookies))
    log.info("=============================================================")

    # Create  a request session
    session = FuturesSession(max_workers=concurrency)

    # Generate request tasks
    tasks = [
        session.get(
            url,
            cookies=cookies,
            background_callback=echo_out
            )
        for i in range(0, tries)
        ]

    # Wait for all tasks to finish
    responses = [r.result() for r in tasks]
    print(dict(MACHINES))
    print(dict(COOKIES))

if __name__ == "__main__":
    make_requests()
