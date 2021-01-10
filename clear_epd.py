#!/usr/bin/env python3

from waveshare_epd import epd7in5_V2

print("Clearing Epd display")
epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()
