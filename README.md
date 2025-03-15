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
    Shows tool outputs live within the application for quick review

- Terminal Display
    Shows tool outputs live within the application for quick review


## Demo

<a href="https://drive.google.com/file/d/1DZ_Gc6PCG-RoFeZj3NeeNwJ4Y7q-gR2t/view?usp=sharing">
  <img src="https://drive.google.com/thumbnail?id=1DZ_Gc6PCG-RoFeZj3NeeNwJ4Y7q-gR2t" alt="Watch the video" width="800">
</a>

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





## Deployment

To deploy this application:

Ensure all dependencies are installed.
Package the application using a tool like PyInstaller.
```bash
pyinstaller --onefile app.py
```
Distribute the generated executable to users.




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


## Acknowledgements

 - [Python Documentation](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [](https://github.com/matiassingers/awesome-readme)
 - [](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)


## Authors
- Samarth Bhat 
- Sohan Simhar Prabakar [@Sohan245](https://github.com/Sohan245/)
- Danindu Gammanpilage [@Danindu](https://github.com/danindu)
