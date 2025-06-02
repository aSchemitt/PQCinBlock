#!/bin/bash

set -e 

# Install sig-python
cd sig-python/
chmod +x ./install.sh
./install.sh
cd ..

# Install/Run sig-java