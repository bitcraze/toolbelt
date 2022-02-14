---
title: Installation
page_id: installation
---


## Prerequisites

The toolbelt requires Docker, see [https://www.docker.com/](https://www.docker.com/) for more information and installation instructions.

## Platforms

The Toolbelt works on Linux, OSX and Windows.

### Linux

Usage on Linux is fairly straight forward. One issue that sometimes pops up is that code in a docker container runs
as root which means that files written to a mapped files system from a process in the container, will be owned by root.
The Toolbelt tries to handle this by running the tools in the builder containers with the user id of the current
user. In most cases this works out but there are some edge cases where there might be some issues. If you have problems
with access rights, this might be the reason.

### OSX

Docker on Mac runs in a (hidden) virtual machine and when mapping a file system into a container, some special handling
is done for file access from within the container. Unfortunately this leads to slower file access which might be a
problem when compiling many files for instance.

### Windows

The Toolbelt can be run from WSL (Windows Subsystem for Linux) on a Windows platform.

It is possible that it also can work in a Windows Command window but it probably requires some tweaking.


## Installation

The only installation required is to add an alias to your `.profile` or `.bashrc` file.

For detailed instructions run

        docker run --rm -it bitcraze/toolbelt


## Updating

To update the Toolbelt to the latest version, run

```
tb update
```

Builders are automatically downloaded when used and there is no need to explicitly update to the latest version.
