import os
import errno

def process_exists(pid):
    if not pid:
        return False

    # http://stackoverflow.com/questions/568271/how-to-check-if-there-exists-a-process-with-a-given-pid
    try:
        os.kill(pid, 0)
    except OSError as e:
        # ESRCH means no process found, we get EPERM if the process exists but
        # we don't have permission to signal it.
        if e.errno == errno.ESRCH:
            return False

    return True

