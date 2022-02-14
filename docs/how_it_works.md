---
title: How it works
page_id: howitworks
---

The Toolbelt uses [Docker](https://docker.com) and it is implemented as a python script that runs in a container. When executing a tool, the
Toolbelt starts a second container where the tool runs. This second container is called a builder and it contains all
the software required to execute the tool. There are a few different builders with tool-chains that are appropriate for
various languages, CPUs and so on, luckily the Toolbelt picks the correct one automatically.

The directory that the tool is executed from is mapped into the docker containers and this is how the tools access the
files, for instance when compiling.

When running the Toolbelt you can see that it is first pulling the latest version of a builder image (for instance
bitcraze/builder) from docker hub to have the latest and greatest builder when running the tool.

It will take a while to download the builder image the first time (or when it has been updated) but usually the version
that is cached in the system can be used and starting a tool takes only around 1 second.

The builder images are also used by our build servers for CI and release builds, this means that building with the
Toolbelt replicates the exact same environment as on our builder servers.

## The module.json file

There is a `module.json` file in the root of repositories that supports the toolbelt. This file describes the
environmental requirements for the tools, which enables the Toolbelt to pick the appropriate builder image when running
a tool.

The `module.json` file also contains build information that is used by other Bitcraze build tools.

### Tool directories

In the `tools` directory one or more sub-directories may contain tools. The most
common location is `tools/build` and by convention there should be one tool
called `build` that builds the source code. The `module.json` file contains a
configuration that tells the Toolbelt which directories that contains tools.

There may be more than one directory with tools in the `tools` directory if needed,
but all directories in the tools folder may not contain tools.

Note: since tools are identified by their name (and not the full path) there
must not be two tools with the same name in different directories.

### Environments

When a module tool is to be executed it must run in a docker container with an
appropriate environment, that is languages, compilers or frameworks that the tool
uses. The `environmentReqs` member of `module.json` describes the environment
required for the tools of a specific directory in `tools`.

The Toobelt inspects the `"environmentReqs"` parameter
in the `module.json` file and matches it with the environments available in the
`config.json` file to select an appropriate environment for the tool.
When the tool is executed, the Toolbelt starts a second Docker container and runs
the tool in that container.

For instance, when calling

        tb flake8

on this project, the tools/build/flake8 script is executed in a builder container
with python3 (and flake8).

All tools located in one directory share the same environment requirements and
they can call each other. Tools should not call tools in other directories if they
have other environment requirements since they all will run in the same container.
