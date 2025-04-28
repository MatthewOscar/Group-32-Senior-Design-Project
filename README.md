# Group 47 Senior Design Project: Multiple Drones Coordination System (MDCS)

![Our poster describes the Multiple Drones Coordination System](https://www.fau.edu/engineering/senior-design/images/47.jpg)

---
## Team Members: 

 - [Tutku Gizem Guder](mailto:tguder2021@fau.edu)
 - [Tarek Kayali](mailto:tkayali2023@fau.edu)
 - [Brenden Martins](mailto:bmartins2013@fau.edu)
 - [Matthew Paternoster](mailto:mpaternoster2022@fau.edu)
 - [Matthew Wyatt](mailto:mwyatt2023@fau.edu)
---
## Folder Structure
### [README](README.md)
### [Deliverables](Deliverables)
- [Documents and Presentations](Deliverables/Documents%20and%20Presentations/)
  - [Design Documents (EGN 4950C)](Deliverables/Documents%20and%20Presentations/Design%20Documents%20(EGN%204950C)/)
  - [Presentations](Deliverables/Documents%20and%20Presentations/Presentations/)
  - [Product Documents (EGN 4952C)](Deliverables/Documents%20and%20Presentations/Product%20Documents%20(EGN%204952C)/)
  - [Progress Reports](Deliverables/Documents%20and%20Presentations/Progress%20Reports/)
    - [EGN 4950C Meeting Reports](Deliverables/Documents%20and%20Presentations/Progress%20Reports/EGN%204950C%20Meeting%20Reports/)
    - [EGN 4952C Progress Reports](Deliverables/Documents%20and%20Presentations/Progress%20Reports/EGN%204950C%20Meeting%20Reports/)
- [Senior Design Project (MDCS)](Deliverables/Senior%20Design%20Project%20(MDCS)/)
  - [MDCS Communications and Data Management (Matthew Wyatt)](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20Communications%20and%20Data%20Management%20(Matthew%20Wyatt)/)
    - [Communications](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20Communications%20and%20Data%20Management%20(Matthew%20Wyatt)/Communications)
    - [Data Management](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20Communications%20and%20Data%20Management%20(Matthew%20Wyatt)/Data%20Management)
  - [MDCS Drone Control (Tarek Kayali)](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20Drone%20Control%20(Tarek%20Kayali)/)
  - [MDCS Simulation Environment (Brenden Martins)](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20Simulation%20Environment%20(Brenden%20Martins)/)
    - [AirSim](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20Simulation%20Environment%20(Brenden%20Martins)/AirSim)
    - [Blocks](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20Simulation%20Environment%20(Brenden%20Martins)/Blocks)
  - [MDCS Target Detection (Tutku Gizem Guder)](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20Target%20Detection%20(Tutku%20Gizem%20Guder)/)
  - [MDCS User Interface (Matthew Paternoster)](Deliverables/Senior%20Design%20Project%20(MDCS)/MDCS%20User%20Interface%20(Matthew%20Paternoster)/)

Note: The folder "Deliverables/Senior Design Project (MDCS)/MDCS Simulation Environment (Brenden Martins)/AirSim" would be located in the Documents folder at C:\Users\username\Documents once AirSim is built on the device. The "AirSim/settings.json" file needs to be configured to the way it is set up here to allow for multiple drones.
___
## Required Programs
The core of our project, the Multiple Drones Coordination System, runs on Microsoft AirSim. For more general information about AirSim, visit https://microsoft.github.io/AirSim/.

Our group presented this project during the Senior Design Showcase by having AirSim installed on a Windows 11 device. To build AirSim, we used the following older software versions as AirSim had been archived by Microsoft:
- [Unreal Engine 4.27](https://www.unrealengine.com/download) via the Epic Games Launcher
- [Python 3.10](https://www.python.org/downloads/)
  - There are required Python dependencies for the MDCS which need to be installed such as airsim, flask, flask-cors, opencv-python, keyboard, and numpy.

## License

    Copyright 2025 Matthew Wyatt, Matthew Paternoster, Brenden Martins, Tarek Kayali, Tutku Gizem Guder

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
