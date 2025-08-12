#!/bin/bash

set -e 

# =============================
# Variables
# =============================
# It is recommended to use the same version of liboqs and liboqs-python
# Releases repositories
LIBOQS_TAG="0.12.0"
LIBOQS_PYTHON_TAG="0.12.0"

# =============================
# Dependencies
# =============================
echo "Installing system dependencies..."
sudo apt update -y
sudo apt install -y build-essential git cmake libssl-dev wget unzip python3 python3-venv python3-pip

# =============================
# Install liboqs
# =============================
echo "Cloning and building liboqs..."
# git clone --depth=1 --branch ${LIBOQS_TAG} https://github.com/open-quantum-safe/liboqs
git clone https://github.com/open-quantum-safe/liboqs
cd liboqs
git checkout tags/${LIBOQS_TAG}

# Sets the source and build directories 
# -DBUILD_SHARED_LIBS=ON
# Can be set to ON or OFF. When ON, liboqs is built as a shared library.
# Default: OFF.
# This means liboqs is built as a static library by default.
cmake -S . -B build -DBUILD_SHARED_LIBS=ON

# Build (--parellel optional)
cmake --build build --parallel 8

# Install
# sudo cmake --build build --target install
sudo cmake --install build

# Update LD_LIBRARY_PATH
# You may need to set the LD_LIBRARY_PATH, environment variable to point to the path to liboqs library directory
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
cd ..

# =============================
# Python Virtual Env
# =============================
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


# Ensure LD_LIBRARY_PATH is set in the venv activation script
if ! grep -q "LD_LIBRARY_PATH" venv/bin/activate; then
  echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> venv/bin/activate
fi

# =============================
# Install liboqs-python
# =============================
# Configure and install the wrapper
echo "Cloning and installing liboqs-python..."
# git clone --depth=1 --branch ${LIBOQS_PYTHON_TAG} https://github.com/open-quantum-safe/liboqs-python
git clone https://github.com/open-quantum-safe/liboqs-python
cd liboqs-python
git checkout tags/${LIBOQS_PYTHON_TAG}
pip install .

cd ..

echo "Installation completed successfully."
