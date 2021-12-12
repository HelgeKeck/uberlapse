# Uberlapse

Klipper Makros to create timelapse of 3D prints.

# Installation

## Installation
On your Raspberry pi run:

```
cd ~/
git clone https://github.com/HelgeKeck/uberlapse.git
bash ~/uberlapse/install.sh
```

## Configure Moonraker update manager

```
# moonraker.conf

[update_manager uberlapse]
type: git_repo
primary_branch: main
path: ~/uberlapse
origin: https://github.com/HelgeKeck/uberlapse.git
```

# Configuration

### Define the Gcode Macro
Include the macro file to your Klipper printer.cfg
```ini
# printer.cfg

[include uberlapse.cfg]

```

## Slicer Setup
To use the Uberlapse you need to add some Klipper macros to your slicer configuration.

### Prusa Slicer / Super Slicer
Printer Settings -> Custom G-code -> Start Gcode -><br />
``START_UBERLAPSE LAYER_COUNT={total_layer_count} PRINT_MIN_X={bounding_box[0]} PRINT_MIN_Y={bounding_box[1]} PRINT_MAX_X={bounding_box[2]} PRINT_MAX_Y={bounding_box[3]}``

Printer Settings -> Custom G-code -> End Gcode -><br />
``END_UBERLAPSE``

Printer Settings -> Custom G-code -> Before layer change Gcode -><br />
``BEFORE_LAYER_UBERLAPSE``

Printer Settings -> Custom G-code -> After layer change Gcode -><br />
``AFTER_LAYER_UBERLAPSE``