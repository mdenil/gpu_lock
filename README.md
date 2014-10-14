# GPU Lock

A small library for locking gpus on a single machine.

# Usage

To run a program on the gpu use:

```
gpu_run my_program my_args
```

To see who has locked which gpu run

```
gpu_lock_info
```

If somehow your process dies without releasing its lock (`gpu_lock_info` will tell you if this has happened) then

```
gpu_lock_release_dead
```

will release all of your locks where the owning process is no longer running.

If all else fails, go muck about in `/var/lock/gpu/`, but be careful :)

# Installation

Run `python setup.py install` to install.

Create `/var/lock/gpu` and make sure it is writeable by everyone who will be locking gpus.

Create a file `/etc/profile.d/gpu_lock.sh` with the following line:

```
export CUDA_VISIBLE_DEVICES=""
```

(or add it to `/etc/bashrc`).  Nothing will stop malicious people from undoing this, this tool relies on everyone cooperating.

