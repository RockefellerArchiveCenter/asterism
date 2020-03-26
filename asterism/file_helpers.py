import datetime
import re
import tarfile
import zipfile
import pwd

from os import remove, stat, walk
from os.path import basename, isdir, isfile, join, getmtime, getsize, splitext
from shutil import rmtree, move, copytree


def file_owner(file_path):
    return pwd.getpwuid(stat(file_path).st_uid).pw_name


def file_modified_time(file_path):
    return datetime.datetime.fromtimestamp(getmtime(file_path))


def get_dir_size(start_path):
    """Returns the total size of a directory.

    See https://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
    """
    total_size = 0
    for dirpath, dirnames, filenames in walk(start_path):
        for f in filenames:
            fp = join(dirpath, f)
            total_size += getsize(fp)
        for d in dirnames:
            dp = join(dirpath, d)
            total_size += getsize(dp)
    return total_size if total_size else False


def remove_file_or_dir(file_path):
    if isfile(file_path):
        try:
            remove(file_path)
        except Exception as e:
            print(e)
            return False
    elif isdir(file_path):
        try:
            rmtree(file_path)
        except Exception as e:
            print(e)
            return False
    return True


def move_file_or_dir(src, dest):
    try:
        move(src, dest)
        return True
    except Exception as e:
        print(e)
        return False


def is_dir_or_file(file_path):
    if isdir(file_path):
        return True
    if isfile(file_path):
        return True
    return False


def make_tarfile(output_filename, source_dir, compressed=True):
    """Creates a TAR file.

    Args:
        output_filename (str): file path for TAR file to be created.
        source_dir (str): directory to serialize
    """
    file_mode = "w:gz" if compressed else "w"
    with tarfile.open(output_filename, file_mode) as tar:
        tar.add(source_dir, arcname=basename(source_dir))


def anon_extract_all(file_path, tmp_dir):
    """Extracts the contents of a serialized file.

    Handles directories, ZIP and TAR files.

    Args:
        file_path (str): file path for a serialized file.
        tmp_dir (str): file path of the location in which to extract the file.
    """
    if isdir(file_path):
        return dir_extract_all(file_path, tmp_dir)
    else:
        if file_path.endswith("tar.gz") or file_path.endswith(".tar"):
            return tar_extract_all(file_path, tmp_dir)
        if file_path.endswith(".zip"):
            return zip_extract_all(file_path, tmp_dir)
    return False


def zip_extract_all(file_path, tmp_dir):
    """Extracts the contents of a ZIP file."""
    extracted = False
    try:
        zf = zipfile.ZipFile(file_path, "r")
        zf.extractall(tmp_dir)
        zf.close()
        extracted = True
    except Exception as e:
        print("Error extracting ZIP file: {}".format(e))
    return extracted


def tar_extract_all(file_path, tmp_dir):
    """Extracts the contents of a TAR file."""
    extracted = False
    try:
        tf = tarfile.open(file_path, "r:*")
        tf.extractall(tmp_dir)
        tf.close()
        extracted = True
    except Exception as e:
        print("Error extracting TAR file: {}".format(e))
    return extracted


def dir_extract_all(file_path, tmp_dir):
    """Extracts the contents of a directory."""
    extracted = False
    try:
        # notice forward slash missing
        if is_dir_or_file("{}{}".format(tmp_dir, file_path.split("/")[-1])):
            rmtree("{}{}".format(tmp_dir, file_path.split("/")[-1]))
        copytree(file_path, "{}{}".format(tmp_dir, file_path.split("/")[-1]))
        extracted = True
    except Exception as e:
        print("Error extracting a directory: {}".format(e))
    return extracted
