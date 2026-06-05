"""
Pytest tests for EEG/MEG file format validation and metadata reading.

Test data is downloaded via MNE's dataset utilities and cached for the session.

Authors:
- Miao Cao

Email:
- miaocao@swin.edu.au
"""

from fileformats.biosig import Fif

# ------------------------------
# MEG: MEGIN
# ------------------------------


def test_fif_instantiate(fif_path):
    Fif(fif_path)
