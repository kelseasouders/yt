import os
import tempfile
from pathlib import Path

from yt.data_objects.time_series import DatasetSeries, get_filenames_from_glob_pattern
from yt.testing import assert_raises
from yt.utilities.exceptions import YTOutputNotIdentified


def test_pattern_expansion():
    file_list = [f"fake_data_file_{str(i).zfill(4)}" for i in range(10)]

    with tempfile.TemporaryDirectory() as tmpdir:
        for file in file_list:
            (Path(tmpdir) / file).touch()

        pattern = os.path.join(tmpdir, "fake_data_file_*")
        found = get_filenames_from_glob_pattern(pattern)
        assert found == [os.path.join(tmpdir, file) for file in file_list]

        found2 = get_filenames_from_glob_pattern(Path(pattern))
        assert found2 == found


def test_no_match_pattern():
    with tempfile.TemporaryDirectory() as tmpdir:
        pattern = os.path.join(tmpdir, "fake_data_file_*")
        assert_raises(OSError, get_filenames_from_glob_pattern, pattern)

def test_init_fake_dataseries():

    file_list = ["fake_data_file_{}".format(str(i).zfill(4)) for i in range(10)]
    with tempfile.TemporaryDirectory() as tmpdir:
        pfile_list = [Path(tmpdir) / file for file in file_list]
        sfile_list = [os.path.join(tmpdir, f) for f in file_list]
        for file in pfile_list:
            file.touch()
        pattern = os.path.join(tmpdir, "fake_data_file_*")

        # init from str pattern
        ts = DatasetSeries(pattern)
        assert ts._pre_outputs == sfile_list

        # init from Path pattern
        ppattern = Path(pattern)
        ts = DatasetSeries(ppattern)
        assert ts._pre_outputs == sfile_list

        # init form str list
        ts = DatasetSeries(sfile_list)
        assert ts._pre_outputs == sfile_list

        # init form Path list
        ts = DatasetSeries(pfile_list)
        assert ts._pre_outputs == pfile_list

        # rejected input type (str repr of a list) "[file1, file2, ...]"
        assert_raises(OSError, DatasetSeries, str(file_list))

        # finally, check that ts[0] fails to actually load
        assert_raises(YTOutputNotIdentified, ts.__getitem__, 0)
