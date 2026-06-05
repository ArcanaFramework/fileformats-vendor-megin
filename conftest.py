import os
import logging
from pathlib import Path
import typing as ty
import pytest

import mne.datasets

# Set DEBUG logging for unittests

log_level = logging.WARNING

logger = logging.getLogger("fileformats")
logger.setLevel(log_level)

sch = logging.StreamHandler()
sch.setLevel(log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sch.setFormatter(formatter)
logger.addHandler(sch)


# For debugging in IDE's don't catch raised exceptions and let the IDE
# break at it
if os.getenv("_PYTEST_RAISE", "0") != "0":

    @pytest.hookimpl(tryfirst=True)
    def pytest_exception_interact(call: pytest.CallInfo[ty.Any]) -> None:
        if call.excinfo is not None:
            raise call.excinfo.value

    @pytest.hookimpl(tryfirst=True)
    def pytest_internalerror(excinfo: pytest.ExceptionInfo[BaseException]) -> None:
        raise excinfo.value


# ------------------------------
# Session-scoped fixtures
# ------------------------------


@pytest.fixture(scope="session")
def sample_data_path() -> Path:
    return Path(mne.datasets.sample.data_path())


@pytest.fixture(scope="session")
def testing_data_path() -> Path:
    return Path(mne.datasets.testing.data_path())


@pytest.fixture(scope="session")
def fif_path(sample_data_path: Path) -> Path:
    return sample_data_path / "MEG" / "sample" / "sample_audvis_raw.fif"
