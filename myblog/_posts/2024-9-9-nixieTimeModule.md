---
layout: post
title: "Nixie Clock Time Module"
subtitle: "Building a consumer-focused NTP time module for nixie clocks"
date: 2024-9-9
background: '/img/posts/nixie-time-module/nixie-header.jpg'
---
##### [The source and technical information about the project can be found in this github repository here](https://github.com/MaxHerbs/esp-time-controller/tree/main)

---
## Motivation
[Nixie tube clocks](https://www.pvelectronics.co.uk/) are popular with hobbyists for their unique look and nostalgic value. Modern implementations typically use an STM32 microprocessor, or something similar - a basic IC similar to those used in arduino's. Although capable of keeping time accurately, setting the time is rather unintuitive - using a set of five buttons to navigate a menu of over 20 options illustrated through just the clock numbers themselves.

The clock does however support a GPS standard - [The NMEA standard](https://en.wikipedia.org/wiki/NMEA_0183).

```
$GNRMC,181908.00,A,3404.7041778,N,07044.3966270,W,0.0,0.0,271023,0.0,E*6C
```
Most of this is useless to us, except for the time and date!
This specific NMEA list `181908.00`, which translates 18:19:08 , and `271023` which corresponds to 27/10/23. The clock reads in a message of this format through a 3.5mm jack - traditionally from a gps device. 

Within this project, the GPS is replaced with an ESP01, using a network time protocol (NTP) time library to fetch the time over wifi, as well as a webserver designed to allow user friendly configuring the wifi credentials, and the timezone. This provides two benefits over the GPS approach

1. As the user can configure the location of their clock, the device is able to handle daylight savings and the likes
2. The web interface provides a user friendly way to configure their time piece without any technical knowledge.  

The clock provides power via the 3.5mm cable so all I needed was a way to connect the serial of the microprocessor to the clock itself!

<div style="display: flex; align-items: center; width: 100%;">
  <div style="flex: 1; padding: 10px;">
    <img src="/img/posts/nixie-time-module/esp-and-pcb.jpg" alt="ESP and custom PCB" style="width: 100%;">
  </div>

  <div style="flex: 1; padding: 10px;">
    <img src="/img/posts/nixie-time-module/early-ui.png" alt="Early UI" style="width: 100%;">
  </div>
</div>

---
## Getting Technical 
The microprocessor used here ESP01, a small form-factor implementation of the ESP8266. The ESP01 was originally designed to serve as a purely a wifi interface for other microprocessors, but as it developed it became a far more capable chip and is used as the main processor in this project. Usually I would opt for the more powerful successor of the ESP8266; the ESP32, but the ESP01 is capable enough for this project, and offers a smaller form factor and a lower cost - coming in at about 65p each!

<div style="display: flex; align-items: flex-start; width: 100%;">
  <div style="flex: 1; padding: 10px;">
    <figure style="margin: 0;">
      <img src="/img/posts/nixie-time-module/35mm-breakout.jpg" alt="Breakout cable to upload code to the ESP01" style="width: 100%;">
      <figcaption style="text-align: center; margin-top: 8px; font-style: italic;">Breakout cable to upload code to the ESP01. The cable has 4 connectors to support serial communication.</figcaption>
    </figure>
  </div>

  <div style="flex: 1; padding: 10px;">
    <figure style="margin: 0;">
      <img src="/img/posts/nixie-time-module/esp-plugged-in.jpg" alt="The whole module plugged in" style="width: 100%;">
      <figcaption style="text-align: center; margin-top: 8px; font-style: italic;">The whole module plugged in. Replicating the setup with a clock while monitoring the serial-out via a USB-to-serial adaptor.</figcaption>
    </figure>
  </div>
</div>




The ESP01 offers everything needed for this project; onboard wifi, a large flash memory to store wifi credentials and timezone configuration, and just enough GPIO (pins to interface with buttons) for to enable the config webserver.

To match the 3.5mm jack required to interface with the clock, I designed a PCB to serve both the 3-connector output for the serial port, as well as a 4-connector input to the ESP01 - enabling me to upload the sketch through the same port, and removing the need for a USB header that would only ever be used once; when writing the code to the chip!

TODO: The PCB design etc

<div style="display: flex; align-items: center; width: 100%;">
  <!-- Image section -->
  <div style="flex: 1; padding: 10px;">
    <img src="/img/posts/nixie-time-module/pcb.jpg" alt="The PCB without the ESP01 attached" style="width: 100%;">
  </div>

  <!-- Text section -->
  <div style="flex: 1; padding: 10px;">
    The PCB is fairly simple. It provides protection from the 5V output from the clock as the ESP01 has 3v logic, a restart button, and a wifi button to enable the configuration webserver. When functioning normally, the device outputs the correct NMEA message every 10 seconds, but can be put into config-mode by holding the wifi button on boot.
  </div>
</div>

When in config mode, it hosts its own wifi access-point. From here, the user can set WiFi credentials and their timezone - both of which are stored in the ESP01's flash, allowing it to persist power cycles. 

The WiFi SSID is populated automatically by the ESP01 on boot by scanning the available WiFi - which can be manually refreshed with a button on the webpage - and also allows users to `verify` their credentials at the click of a button.

---
## The Future of this Project
The project is essentially complete. There are a few bugs and stability issues to iron out still, but no significant issues unless you're doing something really bizzare to the config screen. Also, since the start of this project, daylight savings haven't changed so I'm also hoping to see that to verify the time piece will deal with the time change correctly. 

Proper documentation and guide to reproduce this is yet to be completed. As it stands, the only step necessary to reproduce this at home is to solder a 3.5mm wire to a standard development ESP8266 board such as [this one](https://store.arduino.cc/products/nodemcu-esp8266), or order a copy of the PCB and simply plug in. The code is all open source so reproducing the project shouldn't be too difficult.

For the source code, and more technical information, see the [github repository](https://github.com/MaxHerbs/esp-time-controller). There is also a branch containing the same project, designed for an ESP32 - this branch is deprecated as the project has been ported to an ESP8266.