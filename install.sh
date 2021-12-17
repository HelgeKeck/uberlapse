#!/bin/bash
# Uberlapse Macro installer
#
# taken from https://github.com/mainsail-crew/moonraker-timelapse and modified
# below comments are original
#
# Copyright (C) 2021 Christoph Frei <fryakatkop@gmail.com>
# Slightly modified by Stephan Wendel aka KwadFan <me@stephanwe.de>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
#
# Note:
# this installer script is heavily inspired by 
# https://github.com/protoloft/klipper_z_calibration/blob/master/install.sh

# Prevent running as root.
if [ ${UID} == 0 ]; then
    echo -e "DO NOT RUN THIS SCRIPT AS 'root' !"
    echo -e "If 'root' privileges needed, you will prompted for sudo password."
    exit 1
fi

# Force script to exit if an error occurs
set -e

# Find SRCDIR from the pathname of this script
SRCDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/ && pwd )"

# Default Parameters
KLIPPER_CONFIG_DIR="${HOME}/klipper_config"
KLIPPY_EXTRAS="${HOME}/klipper/klippy/extras"
UBERLAPSE_CONFIG_DIR="${HOME}/klipper_config/uberlapse"

function stop_klipper {
    if [ "$(sudo systemctl list-units --full -all -t service --no-legend | grep -F "klipper.service")" ]; then
        echo "Klipper service found! Stopping during Install."
        sudo systemctl stop klipper
    else
        echo "Klipper service not found, please install Klipper first"
        exit 1
    fi
}

function start_klipper {
    echo "Restarting Klipper service!"
    sudo systemctl restart klipper
}

function create_uberlapse_dir {
    if [ -d "${KLIPPER_CONFIG_DIR}" ]; then
        echo "Creating uberlapse folder..."
        mkdir "${UBERLAPSE_CONFIG_DIR}"
    else
        echo -e "ERROR: ${KLIPPER_CONFIG_DIR} not found."
        exit 1
    fi
}

function link_uberlapse_macros {
    if [ -d "${KLIPPER_CONFIG_DIR}" ]; then
        if [ -d "${UBERLAPSE_CONFIG_DIR}" ]; then
            echo "Linking uberlapse macro file..."
            ln -sf "${SRCDIR}/klipper_macro/config.cfg" "${UBERLAPSE_CONFIG_DIR}/config.cfg"
            echo "Linking uberlapse macro file..."
            ln -sf "${SRCDIR}/klipper_macro/control.cfg" "${UBERLAPSE_CONFIG_DIR}/control.cfg"
            echo "Linking move macro file..."
            ln -sf "${SRCDIR}/klipper_macro/move.cfg" "${UBERLAPSE_CONFIG_DIR}/move.cfg"
            echo "Linking light macro file..."
            ln -sf "${SRCDIR}/klipper_macro/light.cfg" "${UBERLAPSE_CONFIG_DIR}/light.cfg"
            echo "Linking frame macro file..."
            ln -sf "${SRCDIR}/klipper_macro/frame.cfg" "${UBERLAPSE_CONFIG_DIR}/frame.cfg"
            echo "Linking retraction macro file..."
            ln -sf "${SRCDIR}/klipper_macro/retraction.cfg" "${UBERLAPSE_CONFIG_DIR}/retraction.cfg"
            echo "Linking parking macro file..."
            ln -sf "${SRCDIR}/klipper_macro/parking.cfg" "${UBERLAPSE_CONFIG_DIR}/parking.cfg"
        else
            echo -e "ERROR: ${UBERLAPSE_CONFIG_DIR} not found."
            exit 1
        fi
    else
        echo -e "ERROR: ${KLIPPER_CONFIG_DIR} not found."
        exit 1
    fi
}

function link_uberlapse_extras {
    if [ -d "${KLIPPY_EXTRAS}" ]; then
        echo "Linking extra file..."
        ln -sf "${SRCDIR}/klipper_extra/ul_snapshot.py" "${KLIPPY_EXTRAS}/ul_snapshot.py"
    else
        echo -e "ERROR: ${KLIPPY_EXTRAS} not found."
        exit 1
    fi
}

### MAIN

# Parse command line arguments
while getopts "c:h" arg; do
    if [ -n "${arg}" ]; then
        case $arg in
            c)
                KLIPPER_CONFIG_DIR=$OPTARG
                break
            ;;
            [?]|h)
                echo -e "\nUsage: ${0} -c /path/to/klipper_config"
                exit 1
            ;;
        esac
    fi
    break
done

# Run steps
stop_klipper
create_uberlapse_dir
link_uberlapse_macros
#link_uberlapse_extras
start_klipper

# If something checks status of install
exit 0
