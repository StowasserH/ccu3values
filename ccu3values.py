#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import time
import urllib.request
import xml.etree.ElementTree as ET

whitelist = ["ACTUAL_TEMPERATURE", "LOW_BAT", "OPERATING_VOLTAGE", "UNREACH", "SET_POINT_TEMPERATURE", "VALVE_STATE",
             "WINDOW_STATE", "HUMIDITY", "OPERATING_VOLTAGE_STATUS", "BOOST_MODE", "BOOST_MODE"]


def get_values(params):
    response = urllib.request.urlopen(params.xmlapi + "statelist.cgi", timeout=5)
    return response.read().decode("ISO-8859-1")


def get_values_and_cache(params):
    if params.verbose:
        print("build new cache in " + params.cache_file)
    device_list = get_values(params)
    text_file = open(params.cache_file, "w")
    text_file.write(device_list)
    text_file.close()
    return device_list


def main(params):
    device_list = None
    if params.cache_use:
        if os.path.exists(params.cache_file):
            if time.time() < os.path.getmtime(params.cache_file) + params.cache_time:
                if params.verbose:
                    print("Using cached ccu result")
                file = open(params.cache_file)
                device_list = file.read()
                file.close()
            else:
                device_list = get_values_and_cache(params)
        else:
            device_list = get_values_and_cache(params)
    else:
        if params.verbose:
            print("pull list")
        device_list = get_values(params)
    device_list_tree = ET.ElementTree(ET.fromstring(device_list))
    values = {"ccu_devices": []}
    for device in device_list_tree.getroot():
        dev_name = device.attrib['name']
        values["ccu_devices"].append(dev_name)
        values[dev_name] = {}
        for channel in device:
            # name = channel.attrib['name']
            for datapoint in channel:
                type = datapoint.attrib['type']
                value = datapoint.attrib['value']
                if type in whitelist:
                    values[dev_name][type] = value
    if params.command == "devices.number":
        print(len(values["ccu_devices"]))
    elif params.command == "devices":
        devs = []
        for device in values["ccu_devices"]:
            devs.append("{\"device_name\":\"" + device + "\"}")
        print("[" + ",".join(devs) + "]")
    elif params.command.upper() in whitelist:
        if params.device in values:
            print(values[params.device][params.command.upper()])
        else:
            raise Exception("Device not found")
    else:
        raise Exception("Command not allowed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reads operating data from a CCU with XMLRPC plugin.')
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-c", "--cache-use",
                        help="Uses a cache file so that not too many requests are sent to the ccu.",
                        action="store_true")
    # On a rasperypi put the cache file in a ramdisk. This keeps the SD healthy
    parser.add_argument("-f", "--cache-file", help="The file used as cache.", type=str, default="/tmp/ccu.cache")
    parser.add_argument("-t", "--cache-time", help="The length of time the cache file is valid.", type=float,
                        default=60.0)
    parser.add_argument("-x", "--xmlapi", help="Url to the ccu xmlapi.", type=str,
                        default="http://ccu3-webui/addons/xmlapi/")
    parser.add_argument('command', type=str, nargs='?', help='command', default="devices.number")
    parser.add_argument('device', type=str, nargs='?', help='The device name', default="")
    args = parser.parse_args()
    if args.verbose:
        print("verbosity turned on")
        print("params:")
        print(args)
    main(args)
