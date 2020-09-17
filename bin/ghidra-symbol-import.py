#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set autoindent smartindent softtabstop=4 tabstop=4 shiftwidth=4 expandtab:
import os
import ghidra_bridge
from ppsyms import *
from os.path import dirname, realpath, join as pjoin

def main(mapdir):
    read_combined(mapdir)
    with ghidra_bridge.GhidraBridge(namespace=globals()) as b:
        print(hex(getState().getCurrentAddress().getOffset()))
        # Find all the functions whose name is a default name, i.e. FUN_BAADF00D (where BAADF00D is an 8-digit hexadecimal address)
        name_list = b.remote_eval("[(f.getName(), int(str(f.getEntryPoint()), 16),) for f in currentProgram.getFunctionManager().getFunctionsNoStubs(True) if f.getName()[0:4] in ['FUN_', 'LAB_'] and f.getName().endswith(str(f.getEntryPoint()))]")
        print(len(name_list))
        newnames = []
        count_addr, count_syms = 0, 0
        for _, addr in name_list: # symbol name is "garbage" anyway
            if addr in bsp_addr:
                count_addr += 1
        print("addr: ", count_addr)

#    #boolean  addTag(java.lang.String name)
#    #java.lang.String  getComment()
#    #java.lang.String    getName()
#    #java.util.Set<FunctionTag>  getTags()
#    #void    setComment(java.lang.String comment)
#    #void    setName(java.lang.String name, SourceType source)
#    #SourceType  getSignatureSource()
#    #Address     getEntryPoint()

if __name__ == "__main__":
    mapdir = pjoin(dirname(realpath(__file__)), "..", "mapfiles")
    main(mapdir)
