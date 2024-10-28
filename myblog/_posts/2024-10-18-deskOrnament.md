---
layout: post
title: "Desktop Telemetary"
subtitle: "Building a small form-factor desktop device for traffic updates, the weather, and more."
date: 2024-10-18
background: '/img/posts/nixie-time-module/nixie-header.jpg'
---
##### [The source and technical information about the project can be found in this github repository here](https://github.com/MaxHerbs/eta-ornament)

At the time of writing this, this work is still ongoing and incomplete.

---
## Motivation
This was originally supposed to be a cheap and cheerfull fix to a problem I have with commuting. I have a fairly significant commute right now, but my employer offers a flexi-time scheme which is a great way to avoid rush hour where possible. This however leads to my daily question and the motivation for this project; has the traffic cleared up yet?

I needed a simple desktop device that I could take an occasional glance at that would let me know how long it would take to get home, allowing me to work when suitable and head home when the traffic reached a reasonble level.

This was supposed to be the end of the scope of the project, but after v0.1 was finished, it seemed a shame to do so little with such flexible setup, and so functionality was developed to display weather information, a clock - and structured such that more could be easily added in future. 

The device has several distinct screens which it rotates through at a configured interval, showing some new metric on each screen.


## Prototyping
Using an ESP32 - a highly capable microprocessor with onboard WiFi and a large GPIO - I built a prototype on a breadboard.

<div class="image-container">
    <img src="/img/posts/desktop-telemetry/desktop-telemetry.jpg" alt="Early prototype of circuit with SD card module and screen" style="width: 100%; height: auto;">
</div>

The project incorporates a 1.28" 240x240 LCD screen, and an SD card module to hold configuration information and other http post request templates.


## Key Design Decisions
To get traffic, weather, and any other information from remote API, large post request bodies, header information, other generally static text data was needed. These sort of large strings would eat up the available RAM - which could causes issues later down the line as several API could eat up the small amount available in an embeded chip like this.

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

Then the provided configuration file can be deserialised with and template the placeholders by mapping with the same key.

```json
  "postParams": {
  	"start": "the start address",
  	"end": "the end address"
   },
```

Each new function - essentially each distinct screen - is then encapsulated into an object which maintains its own update frequency. `object.update()` is exposed to the top level of the code, and run every loop of the sketch. This function is present in all objects, and when its own update period is passed, refreshes all relevent values, which are then used to populate assets on screens when the device moves onto the next screen.


## Coming to Life
To turn the project from a mess of cables into a proper deliverable, it needs a case, and a PCB.

For a case, I used a piece of 135 degree pipe bend, and made a round PCB to mount the screen to. Also, a second rectangular PCB is made with the same header as the display. The idea is that the main module board will host the majority of the parts, and the round display board is primarily to mount the screen and forward the 7-pin header connector.

<div class="image-container">
    <img src="/img/posts/desktop-telemetry/multi-photo.png" alt="" style="width: 100%; height: auto;">
</div>


Testing cluster