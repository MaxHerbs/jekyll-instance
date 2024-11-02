---
layout: post
title: "Desktop Telemetry"
subtitle: "Building a small form-factor desktop device for traffic updates, monitoring the weather, and more."
date: 2024-10-18
background: '/img/posts/desktop-telemetry/grafana-dash.jpg'
---
##### [The source and technical information about the project can be found in this github repository here](https://github.com/MaxHerbs/desktop-telemetry)

---
## Motivation
This was originally supposed to be a cheap and cheerful fix to a problem I have with commuting. I have a fairly significant commute right now, but my employer offers a flexi-time scheme which is a great way to avoid rush hour where possible. This however leads to my daily question and the motivation for this project; has the traffic cleared up yet?

I needed a simple desktop device that I could take an occasional glance at that would let me know how long it would take to get home, allowing me to work when suitable and head home when the traffic reached a reasonable level.

This was supposed to be the end of the scope of the project, but after v0.1 was finished, it seemed a shame to do so little with such flexible setup, and so I started to develop support for a weather screen and a clock - structured to leave the door open to more in future.

The device has several distinct screens, one for each metric, which it rotates through at a configured interval.

---
## Prototyping
Using an ESP32 - a highly capable microprocessor with onboard WiFi and a large GPIO - I built a prototype on a breadboard.

<div class="image-container">
    <img src="/img/posts/desktop-telemetry/esp-breadboard.jpg" alt="Early prototype of circuit with SD card module and screen" style="width: 100%; height: auto;">
</div>

The project incorporates a 1.28" 240x240 LCD screen, and an SD card module to hold configuration information and other http post request templates.

The screen is very primitive at this stage as it was thrown together quickly as a proof of concept, but a UI will be built with [squareline studio](https://squareline.io/), which provides a drag-and-drop editor with stylised widgets to provide a nicer look later.

---
## Key Design Decisions
To get traffic, weather, and any other information from remote API, large post request bodies, header information, other generally static text data was needed. These sort of large strings would eat up the available RAM - which could causes issues later down the line as several API could eat up the small amount available in an embedded chip like this.

Instead of being written straight into the sketch where they would persist and fragment the RAM, a combination of config files and templates was used to build large strings on the fly, and release the RAM when they're no longer needed. 

A section of the google maps API interface is provided to demonstrate this.

The post request body should follow the following format, where jinja-like placeholders are used to signal areas to be templated.
```json
{% raw %}
{
  "origin": {
    "address": "{{ start }}"
  },
  "destination": {
    "address": "{{ end }}"
  },
  ...
{% endraw %}
```

Then the provided configuration file can be deserialized with and template the placeholders by mapping with the same key.

```json
  "postParams": {
  	"start": "the start address",
  	"end": "the end address"
   },
```

Each new function - essentially each distinct screen - is then encapsulated into an object which maintains its own update frequency. `object.update()` is exposed to the top level of the code, and run every loop of the sketch. This function is present in all objects, and when its own update period is passed, refreshes all relevant values, which are then used to populate assets on screens when the device moves onto the next screen.

---
## Coming to Life
To turn the project from a mess of cables into a proper deliverable, it needs a case, and a PCB.

For a case, I used a piece of 135 degree pipe bend, and made a round PCB to mount the screen to. Also, a second rectangular PCB is made with the same header as the display. The idea is that the main module board will host the majority of the parts, and the round display board will primarily be used to mount the screen and forward the 7-pin header connector for the LCD.

<div class="image-container">
    <img src="/img/posts/desktop-telemetry/multi-photo.png" alt="The case and two PCB's" style="width: 100%; height: auto;">
</div>

---
## Building the Module
With the PCB here, its time to put together the first model, and check the circuit is correct.

<div class="image-container">
    <img src="/img/posts/desktop-telemetry/realPcb.jpg" alt="The real PCB" style="width: 100%; height: auto;">
</div>

The parts are the board PCB, the display mount, and the bezel to hide the internals
After some soldering, the design materialises. For this dev build I have opted to use headers rather than mounting the parts straight to the board - so if any parts are damaged during testing they can be easily replaced.

<div style="display: flex; align-items: flex-start; width: 100%;">
  <div style="flex: 1; padding: 10px;">
    <figure style="margin: 0;">
      <img src="/img/posts/desktop-telemetry/parts.jpg" alt="Breakout cable to upload code to the ESP01" style="width: 100%;">
      <figcaption style="text-align: center; margin-top: 8px; font-style: italic;">The main board. The esp is mounted to the PCB, with an SD card on the opposite side. There is also connection points for a 5V DC supply so that a full USB isn't needed.</figcaption>
    </figure>
  </div>

  <div style="flex: 1; padding: 10px;">
    <figure style="margin: 0;">
      <img src="/img/posts/desktop-telemetry/parts-togethr.jpg" alt="The whole module plugged in" style="width: 100%;">
      <figcaption style="text-align: center; margin-top: 8px; font-style: italic;">The whole module. The daughter board with the screen is mounted at an angle to the main board and provides the holes to align the screen properly. </figcaption>
    </figure>
  </div>
</div>

The wiring and and general structure has worked out nicely and the module fits perfectly in the shell! 

<div style="display: flex; align-items: flex-start; width: 100%;">
  <div style="flex: 1; padding: 10px;">
    <figure style="margin: 0;">
      <img src="/img/posts/desktop-telemetry/screen-on.jpg" alt="Breakout cable to upload code to the ESP01" style="width: 100%;">
      <figcaption style="text-align: center; margin-top: 8px; font-style: italic;">The module works just as it did on the breadboard. The main board can be mounted to three separate headers to compensate for miss-alignments.</figcaption>
    </figure>
  </div>

  <div style="flex: 1; padding: 10px;">
    <figure style="margin: 0;">
      <img src="/img/posts/desktop-telemetry/both.jpg" alt="The whole module plugged in" style="width: 100%;">
      <figcaption style="text-align: center; margin-top: 8px; font-style: italic;">Two sets of PCB, one in and one out of the shell. The screen and mounting for the bezel are missing to make the internals clearer.</figcaption>
    </figure>
  </div>
</div>