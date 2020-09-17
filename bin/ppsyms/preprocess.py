#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set autoindent smartindent softtabstop=4 tabstop=4 shiftwidth=4 expandtab:
import argparse
import os
import sys
import re
from os.path import dirname, realpath, join as pjoin

__all__ = ["refsym_names", "refsym_types", "objtypes", "objcounts", "bsp_addr", "bsp_syms", "matched_libsyms", "matched_objtypes", "read_combined", "show"]

re_refsym = re.compile(r"^([^\s])\s+([^\s]+)\n?$", re.IGNORECASE | re.MULTILINE)
re_bspsym = re.compile(r"^([0-9A-Fa-f]+)\s+?([^\s])\s+([^\s]+)\n?$", re.IGNORECASE | re.MULTILINE)
ignore_syms = {"__bss_start", "_dist_code", "_edata", "_end", "_fini", "_init", "_length_code", "_tr_align", "_tr_flush_block", "_tr_init", "_tr_stored_block", "_tr_tally"}
refsym_names = set()
refsym_types = {}

def read_reference_symbols(fname):
    with open(fname, "r") as f:
        for line in f:
            match = re_refsym.search(line)
            if not match:
                continue
            objtype, symname = match.group(1), match.group(2)
            # If it's on the ignore list
            if symname in ignore_syms:
                continue # skip
            # If it's a 1:1 dupe, ignore
            if symname in refsym_types and refsym_types[symname] == objtype:
                continue
            assert symname not in refsym_names, "Symbol name %s already exists (name list)." % (symname)
            assert symname not in refsym_types, "Symbol name %s already exists (type list)." % (symname)
            refsym_names.add(symname)
            refsym_types[symname] = objtype

objtypes = set()
objcounts = {}
# A/a = absolute
# B/b = in BSS data section
# D/d = initialized data section
# G/g = initialized data section (small global objects)
# S/s = uninitialized data section (small global objects)
# T/t = text (code section), usually functions
# V   = weak object
# W   = weak object (not tagged as such)
bsp_addr = {}
bsp_syms = {}
matched_libsyms = set()
matched_objtypes = {}

def read_bsp_symbols(fname):
    with open(fname, "r") as f:
        for line in f:
            match = re_bspsym.search(line)
            if not match:
                continue
            addr, objtype, symname = int(match.group(1), 16), match.group(2), match.group(3)
            # If it's on the ignore list
            if symname in ignore_syms:
                continue # skip
            # Adding object types
            objtypes.add(objtype)
            if objtype not in objcounts:
                objcounts[objtype] = 1
            else:
                objcounts[objtype] += 1
            # We count absolute objects, but we don't consider them (yet)
            if objtype in {"A", "a"}: # absolute symbols ... TODO: look into those
                continue # skip
            if addr not in bsp_addr:
                bsp_addr[addr] = []
            bsp_addr[addr].append((addr, objtype, symname,))
            if symname not in bsp_syms:
                bsp_syms[symname] = []
            bsp_syms[symname].append((addr, objtype, symname,))
            if symname in refsym_names:
                matched_libsyms.add(symname)
                if not objtype in matched_objtypes:
                    matched_objtypes[objtype] = 0
                matched_objtypes[objtype] += 1

def read_combined(thisdir):
    sym_ossl = pjoin(thisdir, "openssl-0.9.8l-symbols.txt")
    sym_zlib = pjoin(thisdir, "zlib-1.2.3-symbols.txt")
    sym_bsp = pjoin(thisdir, "5.43.A.R2", "symbols_bsp.txt")
    # Read reference symbols for third-party libraries
    read_reference_symbols(sym_ossl)
    read_reference_symbols(sym_zlib)
    # Read actual BSP symbols
    read_bsp_symbols(sym_bsp)

def show(thisdir):
    read_combined(thisdir)
    # Some statistics
    print("="*80)
    print("=== Addresses with more than a single symbol")
    for _, addrset in {x: y for x, y in bsp_addr.items() if len(y) > 1}.items():
        for symitem in addrset:
            print("0x%08X %s %s" % symitem)
    print("="*80)
    print("=== Symbols appearing more than once")
    for _, symset in {x: y for x, y in bsp_syms.items() if len(y) > 1}.items():
        for symitem in symset:
            print("0x%08X %s %s" % symitem)
    print("="*80)
    print("=== Number of objects by type")
    for k, v in objcounts.items():
        matched = "%d" % (v)
        if k in matched_objtypes and matched_objtypes[k] > 0:
            matched = "%s, matched: %d" % (matched, matched_objtypes[k])
        print(k, matched)
    unmatched_refsym = set(refsym_names) - matched_libsyms
    print("=== Matched library symbols: %d of %d (unmatched: %d)" % (len(matched_libsyms), len(refsym_names), len(unmatched_refsym)))
