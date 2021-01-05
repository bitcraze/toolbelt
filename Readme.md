# Toolbelt [![CI](https://github.com/bitcraze/toolbelt/workflows/CI/badge.svg)](https://github.com/bitcraze/toolbelt/actions?query=workflow%3ACI)

The toolbelt is a utility to run tools for testing and building of software modules.
The tools are run in an dockerized environment where toolchains and frameworks 
are installed, and thus removes the need to install  compilers and so on on your
local system.

## Prerequisites

The toolbelt requires Docker 1.12 or later. See [https://www.docker.com/](https://www.docker.com/) for more information and installation instructions. 

The toolbelt works on Linux, OSX and Windows.

### Windows

As the toolbelt uses a bash alias when launched a bash-like environment is required. The
easiest way to get this on Windows is to use Docker Toolbox (not Docker for Windows).

The toolbelt requires the line endings of the build scripts to be "unix style" (LF only
as opposed to Windows style CRLF).

* Git on Windows converts line endings for text files to CRLF when cloning a project. 
To turn it off permanently run ```git config --global core.autocrlf input```
* You should use an editor that supports unix line endings to avoid that the editor 
saves files in the Windows style. For instance Notepad++, Atom or IntelliJ can do this.

## Installation


The only installation required is to add an alias to your `.profile` or `.bashrc` file. For 
detailed instructions run 

        docker run --rm -it bitcraze/toolbelt        
        
### Windows

If you are using Docker Toolbox you can add this alias to ```/c/Users/MyUser/.bashrc```
This will be picked up by the Docker Quickstart Terminal when started and the 
tb alias will be available in the Docker Quickstart Terminal. The toolbelt will 
not be available in other command windows or terminals.

## Usage

Assuming the alias 'tb' is set up as described in the installation instruction.

        tb [command]

To get a list of commands, use

        tb help
        
To execute tools in a module, the toolbelt should always be executed from the
root of the module.

## Upgrading

You need to upgrade from time to time to get the latest version of the toolbelt
as well as the builders. The upgrade is as simple as a docker pull and the 
toolbelt can do it for you.

        tb update

# How it works

The toolbelt is designed to make it easy to modify, test and build Bitcraze projects.
The goal is to remove the need to install tool chains, languages and 
frameworks on the local computer. 

It requires virtually no installation, only an alias.

The toolbelt is implemented as a python3 program that is built into a Docker 
image. When the toolbelt is called, a Docker container is started (based
on the image) and the appropriate command (tool) is executed. The current 
directory is passed as a volume to the toolbelt to allow files to be read or 
modified by tools.
 
## Module
 
A module is a file tree that has a `module.json` file in the root, normally this 
corresponds to a project, for instance this repository. The `module.json` file
describes properties of the module and is read by the toolbelt to understand 
what to do.

### Module tools

The toolbelt can be executed anywhere, but if it is run in the root of a module,
tools specific to that module will be available in the toolbelt. Any file in 
tools/build will be considered to be a tool and is displayed when you type

        tb help
        
Module tools can be called as any other tool with

        tb <tool name>
        
### Environments

When a module tool is to be executed, the toobelt inspects the "environmentReq" parameter 
in the `module.json` file and matches it with the environments available in the 
`config.json` file to select an appropriate environment for the module. An environment
is a Docker image with one or more languages, compilers or frameworks installed.
When the tool is executed, the toolbelt starts a second Docker container and runs
the tool in that container.

For instance, when calling 

        tb flake8 
        
on this project, the tools/build/flake8 script is executed in a builder container 
with python3 (and flake8). 

## Extending the toolbelt

The toolbelt can be extended with your own tools if you like. Create a new 
Docker image based on bitcraze/toolbelt where you copy your tools into the image at 
`toolbelt/belt/` and replace the `toolbelt/util/extensions.py` with a file where
you register your tools.
