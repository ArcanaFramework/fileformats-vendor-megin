import os
import typing as ty
from pathlib import Path
import tempfile

import mne.io

from fileformats.core import extra_implementation, FileSet
from fileformats.biosig.base import Biosig
from fileformats.vendor.megin.biosig import Fif

from fileformats.extras.biosig.utils import mne_deidentify


@extra_implementation(FileSet.read_metadata)
def fif_read_metadata(fif: Fif, **kwargs: ty.Any) -> ty.Mapping[str, ty.Any]:
    return mne.io.read_raw_fif(fif, preload=False, verbose=False).info.to_json_dict()  # type: ignore[no-any-return]


@extra_implementation(Biosig.deidentify)
def fif_deidentify(
    fif: Fif,
    spec: ty.Any = None,
    out_dir: os.PathLike[str] | None = None,
) -> tuple[Fif, dict[str, ty.Any]]:
    out_dir = Path(tempfile.mkdtemp() if out_dir is None else out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = mne.io.read_raw_fif(fif, preload=True, verbose=False)
    deidentified_info, reid = mne_deidentify(raw, spec)
    raw.info = deidentified_info
    deid_fspath = out_dir / "meg-signals.fif"
    raw.save(deid_fspath, overwrite=True)
    return Fif(deid_fspath), reid
