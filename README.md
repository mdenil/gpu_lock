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

Install with pip

```
pip install git+https://github.com/mdenil/gpu_lock
```

so you can uninstall later with `pip uninstall gpu_lock` or clone the repo and run `python setup.py install`.

Create `/var/lock/gpu` and make sure it is writeable by everyone who will be locking gpus (you need to be root to do this).

```
sudo mkdir /var/lock/gpu
sudo chmod a+w /var/lock/gpu
```

Create a file `/etc/profile.d/gpu_lock.sh` with the following line:

```
export CUDA_VISIBLE_DEVICES=""
```

(or add it to `/etc/bashrc`).  This will stop people from accidentally running on an unlocked gpu.  Nothing will stop a malicious person from working around this.

