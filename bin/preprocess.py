#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set autoindent smartindent softtabstop=4 tabstop=4 shiftwidth=4 expandtab:
import os
from ppsyms import show
from os.path import dirname, realpath, join as pjoin

if __name__ == "__main__":
    mapdir = pjoin(dirname(realpath(__file__)), "..", "mapfiles")
    show(mapdir)
