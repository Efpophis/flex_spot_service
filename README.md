# Flex Spot Repeater

A python script that can be run interactively or as a service on a raspberry pi to feed spots to a Flex 6000 series 
radio. It should work with the new 8000 series as well, but I am too cheap to buy one of those, so I won't be testing 
it any time soon.

If you don't have a Flex 6000 or 8000 series, then .. well .. why are you here???

## Installation as a Service (Binary for Raspberry Pi running Ubuntu)

See the [Releases](https://github.com/Efpophis/flex_spot_service/releases) page for the latest releases.

### Install Pre-requisites

Your linux system must support `systemd` and you must be able to execute the `systemctl` command via `sudo`.

### Instructions

Each release has a .tar.gz file attached which contains:
* install.sh - installs the program and sets up the service on a raspberry pi
   * this should work with any linux, but I've only tested it on my Pi that runs on Debian Bullseye. YMMV.
* uninstall.sh - removes the service
* dist/spot_rpt - executable script that does the things
* dist/net-efpophis-spots.service - systemd service file
* dist/flex_spots.conf - configuration file (see below)

To install this version, just run the `install.sh` script. You will be prompted for the following:
* your call sign [REQUIRED] - this is so the script can log you into the specified cluster node.
* cluster host [default is dxusa.net] - hostname of the cluster node you want to use. This should be a node that you
  only use for this service, and nothing else.
* cluster port [default is 7300] - most clusters operate on this port. you should be able to leave the default value
  unless you know the node you want to use is on a different IP port.

The information you enter will be populated in a config file which is installed to `/usr/local/etc/flex_spots.conf`. You can override this on the command-line using the `--config` argument if you want.

#### flex_spots.conf File Format

The `flex_spots.conf` is a yaml file format with 2 sections. The `cluster` section configures your connection to the cluster. The `perma-spots` section configures permanent spots you want to send to the radio and show on the pan-adapter. These don't have to be DX call signs. They can be band edges, or 6m and 10m FM repeater frequencies, or net frequencies, or whatever. I have pre-populated the file with the USA band edges and CW/SSB portion boundaries for 160m - 6m (not including 60m). The should be easy to extend to add or remove whatever you like. Just make sure to include all the fields in your new perma-spots.

### Uninstalling
  
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
$ pip install pyyaml
```

Your Linux machine must also support the `systemctl` command for managing services in `/etc/systemd/system`

### Instructions

1. git clone https://github.com/Efpophis/flex_spot_service.git
2. cd flex_spot_service

If you just want to build, and not install, then run the `build.sh` file. That will create the `spot_rpt.tar.gz` file
and the binary under a new `dist` subfolder. You can even run the script directly to try it out.

If you want to build and install at the same time, just run the install script directly from the `flex_spot_service`
folder. It will find `build.sh` and invoke it on its own before installing everything.

## Running Interactively (on Windows or whatever)

To run the program interactively, either as the .py script (for which you need a python environment) or the binary,
just pass the appropriate command-line args:

For example, after building on Windows:
```
# displays help message and exits
$ ./spot_rpt.exe -h 

# starts the service - ctrl-c to stop
$ ./spot_rpt.exe --call=YOURCALL --host=DX.CLUSTER.HOST --port=[DX Cluster Port Number]
or
$ ./spot_rpt.ext --config=c:\path\to\flex_spots.conf
```

Command-line arguments always override the same information specified in the config file. So you can use the CLI to
test your new configuration wihtout mucking up the file.

## Troubleshooting and Support

Feel free to create an issue in this project if you run into trouble. Also, if you run into trouble and find a solution
yourself, please still create an issue and share your findings.  We're all in this together if we're in it at all.

73 and maybe see you on the air,

Bill WK2X