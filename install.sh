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
UBERLAPSE_CONFIG_DIR="${HOME}/klipper_config/uberlapse"


function create_uberlapse_dir {
    if [ -d "${KLIPPER_CONFIG_DIR}" ]; then
        echo "Creating uberlapse folder..."
        mkdir "${UBERLAPSE_CONFIG_DIR}"
    else
        echo -e "ERROR: ${KLIPPER_CONFIG_DIR} not found."
        echo -e "Try:\nUsage: ${0} -c /path/to/klipper_config\nExiting..."
        exit 1
    fi
}

function link_uberlapse {
    if [ -d "${KLIPPER_CONFIG_DIR}" ]; then
        echo "Linking macro file..."
        ln -sf "${SRCDIR}/klipper_macro/uberlapse.cfg" "${KLIPPER_CONFIG_DIR}/uberlapse.cfg"
        if [ -d "${UBERLAPSE_CONFIG_DIR}" ]; then
            echo "Linking uberlapse macro file..."
            ln -sf "${SRCDIR}/klipper_macro/uberlapse/uberlapse.cfg" "${UBERLAPSE_CONFIG_DIR}/uberlapse.cfg"
            echo "Linking move macro file..."
            ln -sf "${SRCDIR}/klipper_macro/uberlapse/move.cfg" "${UBERLAPSE_CONFIG_DIR}/move.cfg"
            echo "Linking light macro file..."
            ln -sf "${SRCDIR}/klipper_macro/uberlapse/light.cfg" "${UBERLAPSE_CONFIG_DIR}/light.cfg"
            echo "Linking frame macro file..."
            ln -sf "${SRCDIR}/klipper_macro/uberlapse/frame.cfg" "${UBERLAPSE_CONFIG_DIR}/frame.cfg"
            echo "Linking retraction macro file..."
            ln -sf "${SRCDIR}/klipper_macro/uberlapse/retraction.cfg" "${UBERLAPSE_CONFIG_DIR}/retraction.cfg"
            echo "Linking parking macro file..."
            ln -sf "${SRCDIR}/klipper_macro/uberlapse/parking.cfg" "${UBERLAPSE_CONFIG_DIR}/parking.cfg"
        else
            echo -e "ERROR: ${UBERLAPSE_CONFIG_DIR} not found."
            echo -e "Try:\nUsage: ${0} -c /path/to/klipper_config\nExiting..."
            exit 1
        fi
    else
        echo -e "ERROR: ${KLIPPER_CONFIG_DIR} not found."
        echo -e "Try:\nUsage: ${0} -c /path/to/klipper_config\nExiting..."
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
create_uberlapse_dir
link_uberlapse

# If something checks status of install
exit 0
