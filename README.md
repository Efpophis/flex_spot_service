# Flex Spot Service

A python script that can be run as a service on a raspberry pi to feed spots to a Flex 6000 series radio. It should work
with the new 8000 series as well, but I am too cheap to buy one of those, so I won't be testing it any time soon.

If you don't have a Flex 6000 or 8000 series, then .. well .. why are you here???

## Installation (binary for Raspberry Pi running Ubuntu)

See the [Releases](https://github.com/Efpophis/flex_spot_service/releases) page for the latest releases.

### Install Pre-requisites

Your linux system must support `systemd` and you must be able to execute the `systemctl` command via `sudo`.

### Instructions

Each release has a .tar.gz file attached which contains:
* install.sh - installs the program and sets up the service on a raspberry pi
   * this should work with any linux, but I've only tested it on my Pi that runs on Debian Bullseye. YMMV.
* uninstall.sh - removes the service
* dist/spot_rpt - executable script that does the things

To install this version, just run the `install.sh` script. You will be prompted for the following:
* your call sign [REQUIRED] - this is so the script can log you into the specified cluster node.
* cluster host [default is dxusa.net] - hostname of the cluster node you want to use. This should be a node that you
  only use for this service, and nothing else.
* cluster port [default is 7300] - most clusters operate on this port. you should be able to leave the default value
  unless you know the node you want to use is on a different IP port.
  
If you don't like this, you can uninstall it by running:
```
$ ./uninstall.sh
```

## Building From Source

You can also build the service binary from source. This should work on any linux or even Windows. Installing this as
a service on Windows, however, is a huge PITA and I'm not going to even try.  Feel free to figure it out yourself
if you want to, or you can just run it at will from a command prompt or shortcut. These instructions are for building
and installing from source on your raspberry pi or other linux machine

### Pre-requisites

You need to have a sane python environment to build and install the service.
The following modules are also needed:

```
$ pip install pyinstaller
$ pip install pyhamtools
```

Your Linux machine must also support the `systemctl` command for managing services in `/etc/systemd/system`

### Instructions

1. git clone https://github.com/Efpophis/flex_spot_service.git
2. cd flex_spot_service

If you just want to build, and not install, then run the `build.sh` file. That will create the `spot_rpt.tar.gz` file
and the binary under a new `dist` subfolder. You can even run the script directly to try it out.

If you want to build and install at the same time, just run the install script directly from the `flex_spot_service`
folder. It will find `build.sh` and invoke it on its own before installing everything.

## Troubleshooting and Support

Feel free to create an issue in this project if you run into trouble. Also, if you run into trouble and find a solution
yourself, please still create an issue and share your findings.  We're all in this together if we're in it at all.

73 and maybe see you on the air,

Bill WK2X