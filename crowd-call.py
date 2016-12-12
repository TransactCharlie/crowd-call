import click
from requests_futures.sessions import FuturesSession
import logging

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)


def echo_out(sess, resp):
    log.info(resp)
    log.info(resp.text)


@click.command()
@click.option('-u', '--url', help='http(s) request to make', prompt=True)
@click.option('-t', '--tries', default=1, help='number of tries to make')
@click.option('-c', '--concurrency', default=1, help='num of concurrent reqs' )
def make_requests(url, tries, concurrency):
    print(url, tries, concurrency)

    # Create  a request session
    session = FuturesSession(max_workers=concurrency)

    # Generate request tasks
    tasks = [session.get(url, background_callback=echo_out) for i in range(0, tries)]

    # Wait for all tasks to finish
    responses = [r.result() for r in tasks]

    print(responses)

if __name__ == "__main__":
    make_requests()
