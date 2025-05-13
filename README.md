# Realtic - vulnerability assessment tool

Realtic, is a versatile cybersecurity tool designed with a PyQt based graphical user interface. It streamlines cryptographic operations and vulnerability assessments by integrating multiple specialized tools into a single, cohesive application. The design prioritizes simplicity and efficiency, making it ideal for security professionals and enthusiasts looking to conduct quick scans and analyses without the hassle of managing several disparate command-line tools.


## Features

- Tool Selection 
    There are 5 types of Tools you could Select
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
    Shows tool outputs live within the application for quick review

- Terminal Display
    Shows tool outputs live within the application for quick review


## Demo

[![TUTORIAL VIDEO](https://img.youtube.com/vi/Q6xYT5xk0I0/0.jpg)](https://www.youtube.com/watch?v=Q6xYT5xk0I0)

## Installation

Clone the repository:

```bash
git clone https://github.com/danindu/Realtic.git
cd realtic
```

### Dependencies

Update your package list and install required libraries:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-pyqt5 -y
pip3 install pyqt5 rsa rsactftool
```

### Usage

Launch the application by executing:

```bash
python realtic.py
```

### Configuration

#### Tool Parameters

Customize parameters for each selected tool (e.g., hash threshold or maximum
rounds) based on your analysis needs, allowing for tailored execution

#### File Type Selection

Ensure correct file formats are selected per tool requirement, such as “.pdf” files for
SHA1CollisionDetection and “.txt” files for BreakOTS, to facilitate accurate
processing


## Contributing

Contributions are always welcome!

Realtic welcomes contributions from the community. Here’s a detailed guide on how to get involved:

### Fork the Repository

Click the Fork button on the GitHub repository to create your own copy.

### Create a Feature Branch

Create a new branch for your feature

```bash
git checkout -b feature/your-feature-name
```
### Commit Your Changes

```bash
git commit -m "Add detailed feature description"
```

### Push the Branch

```bash
git push origin feature/your-feature-name
```

### Create a Pull Request
Once pushed, open a pull request (PR) on GitHub to merge your changes into the main repository.

### Acknowledgements

We sincerely thank all open-source developers and contributors for their invaluable contributions, which make tools like Realtic possible.

## Authors
- Samarth Bhat (Samarth@reinfosec.com)
- Sohan Simhar Prabakar ([@Sohan245](https://github.com/Sohan245/))
- Danindu Gammanpilage ([@Danindu](https://github.com/danindu))
