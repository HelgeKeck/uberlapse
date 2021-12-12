## Installing the component
To install Uberlapse you need to connect to your Raspberrypi via ssh and
run following commands:

```
cd ~/
git clone https://github.com/HelgeKeck/uberlapse.git
bash ~/uberlapse/install.sh
```

This will clone the repository and execute the installer script.

The script assumes that Klipper is also in your home directory under
"klipper": `${HOME}/klipper` and "moonraker": `${HOME}\moonraker`.

## Enable updating with moonraker update manager

This repo can be updated with the update manager of moonraker. To do so 
add following to your 'moonraker.conf' 

```
# moonraker.conf

[update_manager uberlapse]
type: git_repo
primary_branch: main
path: ~/uberlapse
origin: https://github.com/HelgeKeck/uberlapse.git
```

# Configuration

Please see [configuration.md](configuration.md) for details on how to
configure the timelapse component.
