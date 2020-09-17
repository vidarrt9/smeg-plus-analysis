The interesting parts from the SMEG+ upgrade package.

## Preparations

* `pip3 install --user ghidra_bridge`
* `python3 -m ghidra_bridge.install_server ~/ghidra_scripts`

## Steps performed in Ghidra

* Create new project
* Import `vxworks.bin` into it
    * During import make sure to load it at address 0x200000!
* Open the CodeBrowser
* Let the auto-analysis run
* Apply the `VxWorksSymTab_Finder.java` script from <kbd>Window</kbd> <kbd>Script Manager</kbd> in the CodeBrowser
    * This takes a while, but should yield a number of functions named according to their original name
    * This doesn't cover _all_ functions for which we know symbols, though

