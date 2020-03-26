import datetime
import os
from random import sample
from shutil import copyfile, copytree, rmtree
from unittest import TestCase

from asterism import file_helpers


class TestFileHelpers(TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(
            os.getcwd(), 'asterism', 'fixtures',)
        self.file_path = os.path.join(self.fixtures_dir, 'file.txt')
        self.dir_path = os.path.join(self.fixtures_dir, 'directory')
        self.tmp_dir = os.path.join(self.fixtures_dir, 'tmp')
        for dir in [self.dir_path, self.tmp_dir]:
            if os.path.isdir(dir):
                rmtree(dir)
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        copytree(
            os.path.join(self.fixtures_dir, 'file_helpers', 'directory'),
            self.dir_path)
        copyfile(
            os.path.join(self.fixtures_dir, 'file_helpers', 'file.txt'),
            self.file_path)
        os.makedirs(self.tmp_dir)

    def test_file_attributes(self):
        owner = file_helpers.file_owner(self.file_path)
        self.assertIsNot(False, owner)

        mtime = file_helpers.file_modified_time(self.file_path)
        self.assertTrue(isinstance(mtime, datetime.datetime))

        size = file_helpers.get_dir_size(self.dir_path)
        self.assertIsNot(False, size)
        self.assertTrue(size > 0)

    def test_file_actions(self):
        for path in [self.dir_path, self.file_path]:
            p = file_helpers.is_dir_or_file(path)
            self.assertTrue(p)

        for path in [self.dir_path, self.file_path]:
            moved = file_helpers.move_file_or_dir(path, self.tmp_dir)
            self.assertTrue(moved)

        for path in [
                os.path.join(self.tmp_dir, "file.txt"),
                os.path.join(self.tmp_dir, "directory")]:
            removed = file_helpers.remove_file_or_dir(path)
            self.assertTrue(removed)

    def test_make_tarfile(self):
        for fp, compressed in [("archive.tar", False), ("archive.tar.gz", True)]:
            tarfile = file_helpers.make_tarfile(os.path.join(self.tmp_dir, fp), self.dir_path, compressed=compressed)
            self.assertTrue(os.path.isfile(os.path.join(self.tmp_dir, fp)))

    def test_extract_serialized(self):
        for f in [
                "directory", "directory.zip",
                "directory.tar", "directory.tar.gz"]:
            extracted = file_helpers.anon_extract_all(
                os.path.join(self.fixtures_dir, "file_helpers", f), self.tmp_dir)
            self.assertTrue(extracted)

    def tearDown(self):
        for dir in [self.dir_path, self.tmp_dir]:
            if os.path.isdir(dir):
                rmtree(dir)
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
