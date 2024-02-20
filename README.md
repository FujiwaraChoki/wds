# WDS - War Drone System

This is a project aimed at simulating the software and behaviour of a drone, specifically built for war purposes.

## Features

- [x] Detect movement
- [x] Detect sound

## How it works

The software is entirely built in Python, and it uses the OpenCV library to detect movement and the PyAudio library to detect sound.

## Installation

To install the project, you need to have Python 3.7 or higher installed. Then, you can install the required libraries by running the following command:

```bash
git clone https://github.com/FujiwaraChoki/wds.git
cd wds
python -m venv venv

# Windows
venv\Scripts\activate

# Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Usage

To use the project, you need to run the following command:

```bash
python src/main.py
```

## FAQ

If the program crashes, make sure to adjust the amount of concurrently allowed open files in your system. You can do this by running the following command:

```bash
ulimit -n 2048
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
