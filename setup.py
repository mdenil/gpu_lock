#!/usr/bin/env python

from distutils.core import setup

setup(name="gpu_lock",
      version="0.0.1",
      description="Lock manager for GPUs",
      author="Misha Denil",
      author_email="misha.denil@gmail.com",
      packages=["gpu_lock"],
      scripts=[
          "bin/gpu_run",
          "bin/gpu_lock_info",
          "bin/gpu_lock_release_dead",
          ],
      )
