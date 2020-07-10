# photoworkshop_postprocess
Find a filename in image files in the input directory and rename each image file with the filename found

## Installtion on macOS

This script requires tesseract. Follow the installation instruction [here](https://tesseract-ocr.github.io/tessdoc/Home.html#macos). The easiest way of installing it is to use Homebrew:
```bash
# if you don't already have Homebrew installed, execute the first line or check homebrew website for up-to-date information on how to install it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# Install Tesseract
brew install tesseract
```
You'll then need to setup a virtual env to install the script dependencies. Download [Miniconda3 MacOSX 64-bit bash](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh) on the [mininconda website](https://docs.conda.io/en/latest/miniconda.html).
Then open a terminal and run the following commands:
```bash
# cd to another directory if you downloaded the file to another location
cd ~/Downloads
chmod +x Miniconda3-latest-MacOSX-x86_64.sh
./Miniconda3-latest-MacOSX-x86_64.sh -b

# !!IMPORTANT!! -> Close the current terminal window and reopen a new one for the changes to take effect or you'll get errors on the folowing commands.

conda create -y -nphotoworkshop python=3.7
conda activate photoworkshop
pip install git+https://github.com/esseivaju/photoworkshop_postprocess

# You can now use the photoworkshop tools:
photoworkshop_postprocess --help
```

Whenever you want to use the tool, you'll first need to activate the virtual env you created:
```bash
conda activate photoworkshop # Activate the virtualenv whenever oyu open a terminal window and ant to use the photoworkshop tools
photoworkshop_postprocess --help # You have access to cli tools again
```

## Usage

### photoworkshop_postprocess
This script will process an input src dir (specified wih --src) and recursively looks for tif image files in the directory and each subdirectory. 
Each image will be analyzed using tesseract-ocr to try to find a filename in it. If a filename is found, it is moved to the dst folder. 
If no filename is found in the image, no action is taken. The --move flag allows to move instead of copy files, deleting the original.

```bash
# Example, create a copy of each tif file in the src directory, reading new image name using tesseract-ocr
photoworkshop_postprocess --src /path/to/data --dst /path/to/data 

# Same as previous example except that original files are deleted
photoworkshop_postprocess --src /path/to/data --dst /path/to/data --move

# Copy images to another directory
photoworkshop_postprocess --src /disk1/path/to/data --dst /disk2/path/to/data 


