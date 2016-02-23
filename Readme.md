# Toolbelt

The toolbelt is a utility to run tools for testing and building of software modules.
The tools are run in an dockerized environment where toolchains and frameworks 
are installed, and thus removes the need to install  compilers and so on on your
local system.

## Prerequsites

The toolbelt requires docker 1.9 or later. 

## Installation

The toolbelt works on linux and OSX.

For installation instructions run 

        docker run --rm -it bitcraze/toolbelt        
        
It is probably possible to use it on Windows as well but has not been tested. Please share if you do!

        TODO Windows

## Usage

Assuming the alias 'tb' is set up as described in the installation instruction.

        tb [command]

To get a list of commands, use

        tb help

## Upgrading

You need to upgrade from time to time to get the latest version. The upgrade is
 as simple as a docker pull and the toolbelt can do it for you.

See the help for details.

        tb help

# How it works

The toolbelt is designed to make it easy to modify, test and build Bitcraze projects.
It is designed to remove the need to install tool chains, languages and 
frameworks on the local computer. 

It requires virtually no installation, only an alias.

The toolbelt is implemented as a python3 program that is built into a docker 
image. When the toolbelt is called, a docker container is started (based
on the image) and the appropriate command (tool) is executed. The current 
directory is passed as a volume to the toolbelt to allow files to be read or 
modified by tools.
 
## Module
 
A module is a file tree that has a module.json file in the root, normally this 
corresponds to a project, for instance this repository. The module.json file
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
in the module.json file and matches it with the environments available in the 
config.json file to select an appropriate environment for the module. An environment
is a docker image with one or more languages, compilers or frameworks installed.
When the tool is executed, the toolbelt starts a second docker container and runs
the tool in that container.

For instance, when calling 

        tb pep8 
        
on this project, the tools/build/pep8 script is executed in a builder container 
with python3 (and pep8). 

## Extending the toolbelt

The toolbelt can be extended with your own tools if you like. Create a new 
docker image based on bitcraze/toolbelt where you copy your tools into the image at 
toolbelt/belt/ and replace the toolbelt/util/extensions.py with a file where
you register your tools.
