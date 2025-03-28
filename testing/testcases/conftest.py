import logging
import pytest
from reportportal_client import RPLogger


def pytest_addoption(parser):
    parser.addoption(
        "--case_num", action="store_true", default="all", help="run tests api"
    )

@pytest.fixture(scope="session")
def get_case_num(pytestconfig):
    return pytestconfig.getoption("--case_num")



@pytest.fixture(scope="session")
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)
    return logger