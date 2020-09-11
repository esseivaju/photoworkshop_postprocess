# photoworkshop_postprocess
Find a filename in image files in the input directory and rename each image file with the filename found in it using OCR

## Installation on macOS

This script requires tesseract. Follow the installation instruction [here](https://tesseract-ocr.github.io/tessdoc/Home.html#macos). The easiest way of installing it is to use Homebrew:
```bash
# if you don't already have Homebrew installed, execute the first line or check the homebrew website for up-to-date information on how to install it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# Install Tesseract
brew install tesseract
# Install zbar
brew install zbar
```
You'll then need to setup a virtual env to install the script and its dependencies. Download [Miniconda3 MacOSX 64-bit bash](https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh) on the [mininconda website](https://docs.conda.io/en/latest/miniconda.html) then open a terminal and execute the following commands:
```bash
# cd to another directory if you downloaded the file somewhere else
cd ~/Downloads
chmod +x Miniconda3-latest-MacOSX-x86_64.sh
./Miniconda3-latest-MacOSX-x86_64.sh -b

# !!IMPORTANT!! -> Close the current terminal window and reopen a new window for the changes to take effect otherwise you'll get errors when executing the next commands. Use the command 'exit' to close the current shell.
exit

# Reopen a new terminal window
conda create -y -nphotoworkshop python=3.7
conda activate photoworkshop
pip install git+https://github.com/esseivaju/photoworkshop_postprocess

# You can now use the photoworkshop script:
photoworkshop_postprocess --help
```

Whenever you want to use the script, you'll first need to activate the virtual env you created:
```bash
conda activate photoworkshop # Activate the virtualenv whenever you open a terminal window to use the photoworkshop script
photoworkshop_postprocess --help # You have access to cli command again
```

## Usage

### photoworkshop_postprocess
This script will process an input src dir (specified wih ```--src```) and recursively look for tif image files in the directory and each subdirectory. 
Each image will be analyzed using zbar and tesseract-ocr to try to find a filename in it. If a filename is found, it is moved to the dst folder using the new filename. 
If no filename is found in the image, no action is taken. The ```--move``` flag allows to move instead of copy files, deleting the original files.

In addition to src and dst, a project name needs to be specified. Only string found in the picture which start with the argument specified using ```--project``` will be considered as potential filenames.

```bash
# Example, create a copy of each tif file in the src directory, reading new image name using tesseract-ocr
photoworkshop_postprocess --src /path/to/data --dst /path/to/data --project SLA-MORF

# Same as previous example except that original files are deleted
photoworkshop_postprocess --src /path/to/data --dst /path/to/data --project SLA-MORF --move

# Copy images to another directory
photoworkshop_postprocess --src /disk1/path/to/data --dst /disk2/path/to/data --project SLA-MORF
```
A logfile called photoworkshop.log will be created in you working directory, containing all files that weren't copied because no new filename were found in the picture.

```
usage: photoworkshop_postprocess [-h] --src SRC [--dst DST] --project PROJECT
                                 [--copy] [--workers WORKERS]

optional arguments:
  -h, --help         show this help message and exit
  --src SRC          Source directory containing data toprocess
  --dst DST          Default to --src if not specified
  --project PROJECT  Prefix which must match barcode string
  --copy             Copy files if specified, default is to move files
  --workers WORKERS  Number of 
```
