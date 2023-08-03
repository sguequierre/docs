---
title: "How Linear Velocity is Measured in Viam"
linkTitle: "Linear Velocity"
weight: 10
type: "docs"
description: "How Viam reads and utilizes the linear velocity measurements reported by some models of movement sensor."
---

How Viam's platform reads and utilizes the linear velocity measurements reported as `Readings` by the following {{< glossary_tooltip term_id="model" text="models" >}} of movement sensor components:

- [gps-nmea](/components/movement-sensor/gps/gps-nmea/)

An `Linear Velocity` reading...

An example of a `Linear Velocity` reading:

``` go
sensors.Readings{Name: movementsensor.Named("gps"), Readings: map[string]interface{}{"a": 4.5, "b": 5.6, "c": 6.7}}
```

<!-- TODO: add terminal output or short code snippet -->

Use linear velocity readings to...