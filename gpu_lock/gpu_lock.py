import os
import re
import sys
import pwd
import glob
import shutil
import errno

LOCK_ROOT="/var/lock/gpu"

# ensure the lock dir exists and is writeable 
# ... nothing will work at all if this is not the case
if not os.path.isdir(LOCK_ROOT):
    raise RuntimeError("{} does not exist".format(LOCK_ROOT))
if not os.access(LOCK_ROOT, os.W_OK):
    raise RuntimeError("{} is not writeable".format(LOCK_ROOT))

def _enumerate_gpu_ids():
    device_files = glob.glob("/dev/nvidia[0-9]")
    return sorted(
        int(re.sub(r".*([0-9]+)$", r"\1", device))
        for device in device_files)

def _lock_dir_name(gpu_id):
    return os.path.join(LOCK_ROOT, "gpu{}.lock".format(gpu_id))

def enumerate_gpus():
    for gpu_id in _enumerate_gpu_ids():
        yield Gpu(gpu_id)

class Gpu(object):
    """
    A GPU device.  Keeps track of ownership.
    """
    def __init__(self, gpu_id):
        self.gpu_id = gpu_id
        self.lock_dir = _lock_dir_name(self.gpu_id)

    def acquire(self):
        try:
            os.mkdir(self.lock_dir)

            with open(self._pid_file_name(), 'w') as pid_file:
                pid_file.write(str(os.getpid()))

            return True

        except OSError:
            return False

    def release(self):
        shutil.rmtree(self.lock_dir)

    def _pid_file_name(self):
        return os.path.join(self.lock_dir, "pid")

    @property
    def is_owned(self):
        return os.path.exists(self.lock_dir)

    @property
    def is_mine(self):
        return self.owner_id == os.geteuid()

    @property
    def owner_id(self):
        if not self.is_owned:
            return None
        return os.stat(self.lock_dir).st_uid

    @property
    def owner_name(self):
        if not self.is_owned:
            return None
        return pwd.getpwuid(self.owner_id).pw_name

    @property
    def owning_process(self):
        if not self.is_owned:
            return None

        with open(self._pid_file_name()) as pid_file:
            return int(pid_file.read())


class GpuManager(object):
    """
    A context manager that acquires and holds the next available GPU.
    """

    def __enter__(self):
        self.gpu = self._lock_next_available_gpu()
        return self

    def __exit__(self, type, value, traceback):
        self.gpu.release()

    def _lock_next_available_gpu(self):
        for gpu in enumerate_gpus():
            if gpu.acquire():
                return gpu
        else:
            raise RuntimeError("No GPUs available")

