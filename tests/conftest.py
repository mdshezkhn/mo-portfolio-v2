import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--snapshot-update", action="store_true", default=False, help="Update snapshot fixtures"
    )
