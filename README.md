# Introduction/General Project Overview

This project was created in conjunction with Dr. Troy Heitmann's Wave Energy Research lab. In their lab, they use "Wave Gauges" to take the required measurements for their work. However, the calibration and movement of these gauges is an important part of the setup and usage: often this process is manual, imprecise, and frustrating for Dr. Heitmann and his fellow researchers. The purpose of this project was to create an automated process for the calibration and movement of these "Wave Gauges." 

## Project Breakdown

This project can be broken down into the following segments:

1. Physical design of calibration setup
2. Fabrication of calibration setup
3. Design of electrical systems
4. Fabrication of electrical systems
5. TCP Socket Connection (Information Transfer)
6. Clear User Interface (GUI)

## Physical Design of Calibration Setup

The design for the physical movement of the wave gauge is relatively minimalistic and simple. Using an internally outputting cycloidal gearbox to actuate a T12x3mm pitch lead screw and a close loop Nema 23 (along with the CL57T-V4.1 stepper driver), this system has +-0.5mm of control over the vertical actuation of the gauge (which is attached via screw clamping mechanism). There is a parallel "backbone" in the form of 8020 1010 extrusion. The carrier and lower reciever for the lead screw use offset 8020 1010 extrusion profiles (0.15mm) to achieve proper tolerance when mounting, and use t-nuts to properly clamp and attach onto the 8020 back rail. 

## Design of Electrical Systems

Again, the design of the electrical systems for this project is relatively simple. Using an Arduino Uno WiFi REV2 wired to a CL57T-V4.1 stepper driver (all powered by a 24V variable power supply), this system is able to be controlled over local WiFi.

## Programming

The code for this project was aimed to allow for a python-based GUI (with active feedback) that could send desired movement over local WiFi. It was a challenge using the WiFiNINA Arduino library to properly parse incoming requests from the Python GUI, but using the available "requests" library and PyQt5 (for GUI design), developing these two components was not extremely complex.

# Using Posted Resources

## Posted Resources

This GitHub page has all of the .STEP files (editable geometry) for the entire system posted. Additionally, it has the python and accompanying Arduino code to implement and use the project.

## Notes on Code

Prior to usage, the user will have to import the following libraries on their computer (using a virtual environment and "pip" or "pipx"):

1. PyQt5
2. MatPlotLib
3. requests

All code for this project was develoed in Visual Studios Code, and should be fully understandable through the provided comments. 

Additionally, there is Arduino code posted for both Platform IO and the Arduino IDE. Just ensure that you are using the correct version. 

## Bill of Materials (BOM)

The bill of materials for this project are posted as a .csv file in the repository. 

# Assembly Overview

The assembly for this project is simple and straightforward, as is displayed throughout a few steps below.

### Step 1: Carrier Assembly

Assemble the carrier as displayed below. Use heat set inserts on the topside of the cycloidal output carrier.

![Carrier Assembly](https://github.com/HMEC-UH/waveGaugeController/blob/main/Assembly%20Image%20Diagrams/outputCarrier.png)

### Step 2: Housing Assembly

Assemble the housing as shown below (insert the 50mmx6mm stainless steel dowels into the lower housing)

![Housing Assembly](https://github.com/HMEC-UH/waveGaugeController/blob/main/Assembly%20Image%20Diagrams/housingAssembly.png)

### Step 3: Motor Mounting

Screw the motor to the upper housing using M4x20mm bolts and M4 lock nuts.

### Step 4: Carrier Insertion and Upper Housing Mounting

Place the cycloidal disks into the housing as shown below, and screw on the upper housing (ensure that the D-Shaft bore of the eccentric bearing and the D-shaft of the motor are aligned. It should fit snugly). It will take some gentle pressure to ease the upper housing onto the gearbox. 

![Carrier Insertion](https://github.com/HMEC-UH/waveGaugeController/blob/main/Assembly%20Image%20Diagrams/fullHousingAssembly.png)

### Lead Screw Mounting

Screw the lead screw into the negative T12 thread on the output side of the cycloidal gearbox. 

# Developer Notes

I'm Charlie Koh. At the time of this development, I am a rising Junior at Punahou High School. This project was developed in collaboration with the lab of Dr. Troy Heitmann.