import struct

from fileformats.core import BinaryFile, validated_property
from fileformats.core.exceptions import FormatMismatchError

from fileformats.biosig import Meg


# ------------------------------
# Implementation of Specific EEG Formats
# ------------------------------
class Fif(BinaryFile, Meg):
    """
    MNE FIF format (standard format for NeuroMag/MEGIN MEG/EEG devices)
    Most commonly used binary format, supports compression (.fif.gz)
    """

    ext = ".fif"

    @validated_property
    def fiff_header(self) -> None:
        # FIFF files begin with a tag stream; the first tag must be FIFF_FILE_ID (kind=100)
        # with data type FIFFT_ID_STRUCT (dtype=31), encoded as big-endian uint32 pairs.
        data = self.read_contents(8)
        if len(data) < 8:
            raise FormatMismatchError(f"File too short to be a valid FIFF file: {self}")
        kind, dtype = struct.unpack(">II", data)
        if kind != 100 or dtype != 31:
            raise FormatMismatchError(
                f"First FIFF tag has kind={kind}, dtype={dtype}; expected kind=100 "
                f"(FIFF_FILE_ID) and dtype=31 (FIFFT_ID_STRUCT) in {self}"
            )
