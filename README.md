# OGI_Team — Samsung Innovation Campus Mini Project

> A mini project developed by Ahmed Gwely, Ibrahim Shnouda, and Omer Hany as part of the Samsung Innovation Campus.

## Table of Contents

- [Introduction](#introduction)  
- [Authors](#authors)  
- [Project Description](#project-description)  
- [Features](#features)  
- [Repository Structure](#repository-structure)  
- [Getting Started](#getting-started)  
  - [Requirements](#requirements)  
  - [Installation](#installation)  
  - [Usage](#usage)  
- [How It Works](#how-it-works)  
- [Screenshots](#screenshots)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)  

## Introduction

This repository contains a Python-based prototype project developed for the **Samsung Innovation Campus** program. The project explores sensor control and client-server communication using modules such as ultrasonic sensors, servo motors, and Raspberry Pi.

## Authors

- Ahmed Gwely  
- Ibrahim Shnouda  
- Omer Hany  

## Project Description

The goal of this mini project is to demonstrate a hardware + software interaction system where a microcontroller (e.g. Raspberry Pi) interacts with sensors (like ultrasonic) and actuators (e.g. servo) and communicates data to a client module (e.g. PC or mobile) via networking (socket communication).  

Typical use cases include:

- Obstacle detection and avoidance  
- Remote monitoring of sensor readings  
- Real-time control of servo motors based on sensor input  

## Features

- Ultrasonic distance measurement  
- Servo control  
- Real-time data transmission from “server” (Raspberry Pi) to “client”  
- Modular Python scripts for sensors, actuators, and networking  

## Repository Structure

OGI_Team/
│
├── Ultrasonic_01.py # Main ultrasonic sensor module
├── client1.py # Client side script (receiving data)
├── client_01.py # Alternative client script or variant
├── rasp.py # Raspberry Pi (server) script
├── servo.py # Servo motor control script
├── capture_*.jpg # Example images / captures / proof of concept
└── README.md # This file



You may add or rename files as needed; this is just the current structure.

## Getting Started

### Requirements

- Python 3.x  
- A Raspberry Pi (or any Linux board / microcontroller capable of Python)  
- An ultrasonic sensor (e.g. HC-SR04)  
- A servo motor  
- Network connectivity (e.g. via WiFi or Ethernet)  
- (Optional) GPIO library (e.g. `RPi.GPIO` or `gpiozero`)  

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ibrahemshenouda/OGI_Team.git
   cd OGI_Team
   ```
2. (Optional) Create and activate a virtual environment:

  ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install any Python dependencies (if you have a requirements.txt, otherwise manually):

  ```bash
   pip install <required-libraries>
   ```




