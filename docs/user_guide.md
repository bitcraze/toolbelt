---
title: User guide
page_id: userguide
---

The Toolbelt should be executed from the root of a Bitcraze repository. You can run tools (commands) in the toolbelt
with the extra spice that they run in the required environment, for instance when building the firmware the correct
compiler is automatically available.

To run the Toolbelt, simply type `tb`. This will display a brief help and a list of the tools that are available.

An example:

``` bash
$ tb
Usage:  tb [-d] tool [arguments]
The toolbelt is used to develop, test and build Bitcraze modules. When the toolbelt is called, it will first try to find the tool in the belt, after that it will try the tools in the module if the working directory is the root of a module. Module tools are executed in the context of a docker container based on the module requirements configured in the module.json config file.

-d:  print the docker call that executes the tool

Tools in the belt:
  help, -h, --help - Help
  update - Update tool belt to latest version
  version, -V, --version - Display version of the tool belt
  ghrn - Generate release notes from github milestone
  docs - Serve docs locally

Tools in the current module:
  build
  test
  compile
  check_elf
  make
  test_python
  clean
  build-docs
```

Some tools are implemented in the Toolbelt (the first section) while some tools are implemented in the repository (the
second section). In the example above the `build`, `test` and so on are scripts implemented in the repository.

To use the make tool in the example above, one would do
``` bash
$ tb make
Running script tools/build/make in a container based on the bitcraze/builder docker image as uid 1000
Using default tag: latest
latest: Pulling from bitcraze/builder
Digest: sha256:bee591d94db757465b88338c69be847cdf527698f0270ea1a86a2ccaa3c9845d
Status: Image is up to date for bitcraze/builder:latest
docker.io/bitcraze/builder:latest
make: Entering directory '/module'
  CLEAN_VERSION
  CC    stm32f4xx_dma.o
  CC    stm32f4xx_exti.o
  CC    stm32f4xx_flash.o
  CC    stm32f4xx_gpio.o
...
```

### -d - Show docker command

Sometimes it is useful to see the exact docker command the Toolbelt is using to run a tool,
for instance when debugging a tool or developing builder docker images. Simply run the Toolbelt with the -d flag,
something like:

        tb -d flake8

## Built in tools

### help

```
tb help
```

Display help.

You can also get help on a specific tool (only works for built in tools), for instance `tb help ghrn`

### update

Update the Toolbelt to the latest version by pulling the docker image from Docker hub

```tb update```

### version

Display the current version of the Toolbelt

```tb version```

### ghrn

Generate release notes based on a milestone in a github repository. Extracts all issues from the milestone and lists them.

For instance, to generated release notes for the `crazyflie-firmware` repository, using the `2017.04` milestone

```tb ghrn bitcraze/crazyflie-firmware 2017.04```

### docs

Start a local web server and serve the documentation in the `docs` folder of a repository.

Use when writing documentation to render a basic version of the documentation. Changes in the source code triggers a
rebuild of the web content to make it easy to see the result of a change

```tb docs```

## Repository tools

Tools that are implemented in a repository should be located in the `tools/build` or `tools/build-docs` directories by
convention. A tool is usually just a bash or python script and often they can also be executed without the toolbelt
provided you have the appropriate software installed on your system.
