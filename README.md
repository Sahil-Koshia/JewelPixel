# JewelPixel

**JewelPixel** is an AI-powered reverse image search engine tailored specifically for jewelry. It allows users to upload jewelry images or search by name to find similar designs using advanced AI algorithms.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Using GPU for Faster Processing](#using-gpu-for-faster-processing)
- [Switching Between GPU and CPU](#switching-between-gpu-and-cpu)
- [Updating the Project](#updating-the-project)
- [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Reverse Image Search**: Upload jewelry images to find similar designs.
- **Search by Name**: Enter the name of a jewelry piece to find similar images.
- **Download Options**: Download selected images individually or as a ZIP file.
- **Real-Time Updates**: See real-time progress when updating the image database.
- **User-Friendly Interface**: Simple and intuitive web interface with GPU support.

## Prerequisites

Before installing JewelPixel, ensure you have the following software installed on your system:

- **Python 3.8 or higher**: Download from [python.org](https://www.python.org/downloads/).
- **Git**: Download from [git-scm.com](https://git-scm.com/downloads).

### Optional:

- **Virtual Environment**: To isolate project dependencies.
- **NVIDIA GPU**: For faster image processing (optional but recommended).

## Installation

Follow these steps to install JewelPixel on your local machine:

### 1. Clone the Repository

First, clone the JewelPixel repository to your local machine:

```bash
git clone https://github.com/Sahil-Koshia/JewelPixel.git
cd JewelPixel


2. Set Up a Virtual Environment (Optional but Recommended)
Setting up a virtual environment helps keep dependencies isolated:

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:
bash
Copy code
venv\Scripts\activate
3. Install Dependencies
Install the required Python packages:

bash
Copy code
pip install -r requirements.txt
4. Configure GPU Support (Optional)
If you have an NVIDIA GPU, ensure that the CUDA Toolkit and cuDNN libraries are installed. TensorFlow will automatically detect and use the GPU for processing.

Running the Application
Start the Flask web server to run JewelPixel:

bash
Copy code
python app.py
After running the command, open your web browser and navigate to:

plaintext
Copy code
http://127.0.0.1:5000
From there, you can upload jewelry images, search by name, and explore similar designs.

Using GPU for Faster Processing
JewelPixel can utilize a GPU if available, which significantly speeds up image processing tasks. If you have a compatible NVIDIA GPU, follow these steps to enable GPU support:

Steps to Enable GPU Support:
Install CUDA Toolkit: Download and install the CUDA Toolkit from NVIDIA's CUDA Toolkit website.

Install cuDNN: Download and install cuDNN from NVIDIA's cuDNN website. Ensure that the cuDNN version matches your CUDA installation.

Verify GPU Setup: After installing CUDA and cuDNN, verify that TensorFlow detects your GPU:

python
Copy code
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
If this prints out a number greater than 0, TensorFlow has successfully detected your GPU.

Install TensorFlow with GPU Support: Ensure that your environment has TensorFlow with GPU support installed:

bash
Copy code
pip install tensorflow-gpu
GPU Tips:
Check GPU Usage: Use tools like NVIDIA’s nvidia-smi to monitor GPU usage.
Compatibility: Ensure that your GPU drivers, CUDA, and cuDNN versions are compatible with the installed TensorFlow version.
Switching Between GPU and CPU
Sometimes you might want to switch between using GPU and CPU for testing or performance reasons.

Force TensorFlow to Use CPU Only:
To force TensorFlow to use only the CPU, you can set the following environment variable before running your application:

On Windows (in Command Prompt or PowerShell):

bash
Copy code
set CUDA_VISIBLE_DEVICES=-1
python app.py
This command tells TensorFlow not to use any GPU, even if available.

Re-enable GPU Support:
Simply remove the CUDA_VISIBLE_DEVICES variable or set it back to your GPU device:

bash
Copy code
set CUDA_VISIBLE_DEVICES=0  # 0 indicates the first GPU
python app.py
