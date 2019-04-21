Encrypting the Client
=====================
The first step in building a distributable Toontown Infinite client is building ```GameData.bin```. ```GameData.bin``` is an encrypted blob of frozen Python code. It contains all of the code necessary to run the game. There are three steps to building this file:

* [Prepare for building](prepare-client.md)
* [Build the frozen Python module](build-client.md)
* **Encrypt the frozen Python module**

This document outlines how to accomplish the third and final task.

- - -

By now, you should have a file named ```GameData.pyd``` in your build directory. The last step is to encrypt this file, and rename it to ```GameData.bin```! To do this, we use a utility called ```infinitecipher```. To get this utility, ask one of the lead developers.

## Usage ##

    Usage: infinitecipher [-h] [-o OUTPUT] [INPUT]
    
    Positional arguments:
      INPUT         The file that needs to be encrypted.
    
    Optional arguments:
      -h, --help    Print this dialog and exit.
      -o, --output  The encrypted outputile.

## Example ##

    infinitecipher -o GameData.bin GameData.pyd
