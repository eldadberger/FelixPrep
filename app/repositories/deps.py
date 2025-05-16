import requests
from typing import Generator


def get_requests_session(headers=None) -> Generator[requests.Session, None, None]:
    session = requests.Session()
    try:
        session.headers.update(headers)
        yield session
    finally:
        session.close()
