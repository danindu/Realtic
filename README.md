
[![Reinforsec](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://github.com/Sohan245/Realtic)


# Realtic - vulnerability assessment tool

Realtic, is a versatile cybersecurity tool designed with a PyQt based graphical user interface. It streamlines cryptographic operations and vulnerability assessments by integrating multiple specialized tools into a single, cohesive application. The design prioritizes simplicity and efficiency, making it ideal for security professionals and enthusiasts looking to conduct quick scans and analyses without the hassle of managing several disparate command-line tools.


## Features

- Tool Selection 
    There are 4 types of Tools you could Select
     - Linear Trails
    -   SHA1 Collision Detection
    - Break OTS
    - RSA CTF Tool
    - S-Box Gates


- File Input Support
    Realtic tool supports the following File types
    - PDF
    - XML
    - PUB

    

- Real-Time Graphical Output Display
   - Shows tool outputs live within the application for quick review

- Terminal Display
   - Shows tool outputs live within the application for quick review


## Demo


[https://drive.google.com/file/d/1-p6qru6LUAYRosSGClemTEHBdw1oOn9G/view?usp=drive_link]
## Installation

Clone the repository:

```bash
git clone https://github.com/Sohan245/Realtic.git
cd realtic
```

### Dependencies

Update your package list and install required libraries:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-pyqt5 -y
pip3 install pyqt5 rsa rsactftool
```

### Run

Launch the application by executing:

```bash
python realtic.py
```


