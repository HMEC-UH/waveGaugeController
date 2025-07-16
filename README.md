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



# Developer Notes

I'm Charlie Koh. At the time of this development, I am a rising Junior at Punahou High School. This project was developed in collaboration with the lab of Dr. Troy Heitmann.