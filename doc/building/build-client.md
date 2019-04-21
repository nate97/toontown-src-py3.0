Building the Client
===================
The first step in building a distributable Toontown Infinite client is building ```GameData.bin```. ```GameData.bin``` is an encrypted blob of frozen Python code. It contains all of the code necessary to run the game. There are three steps to building this file:

* [Prepare for building](prepare-client.md)
* **Build the frozen Python module**
* [Encrypt the frozen Python module](encrypt-client.md)

This document outlines how to accomplish the second task.

- - -

After preparing the client using the ```prepare_client.py``` utility, you're all set to build! Simply use the ```build_client.py``` utility through the _Visual Studio 2008 Command Prompt_. This will create a frozen Python module named ```GameData.pyd```.

## Usage ##

    usage: build_client.py [-h] [--panda3d-dir PANDA3D_DIR]
                           [--build-dir BUILD_DIR] [--main-module MAIN_MODULE]
                           [modules [modules ...]]
    
    positional arguments:
      modules               The Toontown Infinite modules to be included in the
                            build.
    
    optional arguments:
      -h, --help            show this help message and exit
      --panda3d-dir PANDA3D_DIR
                            The path to the Panda3D build to use for this
                            distribution.
      --build-dir BUILD_DIR
                            The directory of which the build was prepared.
      --main-module MAIN_MODULE
                            The path to the instantiation module.

## Example ##

    ppython -m build_client --panda3d-dir C:/Panda3D-1.9.0 --build-dir build
                            --main-module toontown.toonbase.ToontownStartDist
                            otp toontown
