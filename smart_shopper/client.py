"""Client requests."""

import httpx

import structlog

import tenacity
from dataclasses import dataclass
logger = structlog.get_logger()

@tenacity.retry(
    retry=tenacity.retry_if_exception_type(httpx.HTTPError),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    stop=tenacity.stop_after_attempt(3),
    before_sleep=lambda retry_state: logger.warning(
        "Request failed, retrying",
        attempt=retry_state.attempt_number,
        next_attempt_in=retry_state.next_action.sleep,
    ),
)
def retry_client(func):
    return func


@dataclass
class Client:
    """A client for making HTTP requests."""

    def __post_init__(self):
        self.client = httpx.Client(
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"},
            verify=False,
            timeout=30,
        )

    @retry_client
    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Make a request."""
        return self.client.request(method, url, **kwargs)



client = Client()