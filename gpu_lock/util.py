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

def gpu_run_process_info(pid):
    """
    Returns the name of a running program launched with gpu_run.

    This is accomplished by reading the cmd line that gpu_run was invoked with
    and dropping the first two elements.  We drop the first two because they
    should always be "python" and "gpu_run".
    """

    if not pid:
        return ""

    with open("/proc/{}/cmdline".format(pid)) as cmdline_file:
        cmdline = cmdline_file.read().split('\0')

    # ignore any path prefixing the command
    cmdline[2] = os.path.basename(cmdline[2])

    return " ".join(cmdline[2:])
        
