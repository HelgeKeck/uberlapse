# Uberlapse
Klipper Makros to create timelapse of 3D prints.

## Uberlapse Example 
[![Video Example](https://img.youtube.com/vi/6Ex2qVkM0Ds/0.jpg)](https://www.youtube.com/watch?v=6Ex2qVkM0Ds)    

# V-Core Camera Slider
Uberlapse can also make use of the V-Core Camera Slider to create moving timelapses.   
V-Core Camera Slider: https://github.com/HelgeKeck/vcore-slider/  

## Uberlapse Camera slider example
[![Video Example](https://img.youtube.com/vi/hdajsakze78/0.jpg)](https://www.youtube.com/watch?v=hdajsakze78)    

## Uberlapse Camera slider example
[![Video Example](https://img.youtube.com/vi/H-ifAT6w3YU/0.jpg)](https://www.youtube.com/watch?v=H-ifAT6w3YU)    

## Uberlapse Camera slider example
[![Video Example](https://img.youtube.com/vi/HQpCxaaxgOE/0.jpg)](https://www.youtube.com/watch?v=HQpCxaaxgOE)    

# Installation

## On your Raspberry
```
cd ~/
git clone https://github.com/HelgeKeck/uberlapse.git
bash ~/uberlapse/install.sh
```

## Configure Moonraker update manager
```ini
# moonraker.conf

[update_manager uberlapse]
type: git_repo
primary_branch: main
path: ~/uberlapse
origin: https://github.com/HelgeKeck/uberlapse.git
```

## Define the Gcode Macro
```ini
# printer.cfg

[include uberlapse.cfg]

```

## Prusa Slicer / Super Slicer
Printer Settings -> Custom G-code -> Start Gcode -><br />
``START_UBERLAPSE LAYER_COUNT={total_layer_count} PRINT_MIN_X={bounding_box[0]} PRINT_MIN_Y={bounding_box[1]} PRINT_MAX_X={bounding_box[2]} PRINT_MAX_Y={bounding_box[3]}``

Printer Settings -> Custom G-code -> End Gcode -><br />
``END_UBERLAPSE``

Printer Settings -> Custom G-code -> Before layer change Gcode -><br />
``BEFORE_LAYER_UBERLAPSE``

Printer Settings -> Custom G-code -> After layer change Gcode -><br />
``AFTER_LAYER_UBERLAPSE``