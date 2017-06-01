# Plex-Scripts


##### Setting up a build environment
First install Xcode (free from Mac OS X App Store). After it's installed, install the Xcode command-line tools by executing `xcode-select --install` from a terminal.

The easiest way to install Comskip's dependencies is via Homebrew (http://brew.sh/):
```shell
brew install autoconf automake libtool pkgconfig argtable ffmpeg sdl
```

##### Setting up Comskip
Before you clone the Comskip repo make sure you navigate out of the current git repo to avoid conflict.

```
cd install/path
git clone git://github.com/erikkaashoek/Comskip
cd Comskip
./autogen.sh
./configure
make
```
*If you do not wish to use the default settings provided by the `comskip.ini` in this repo, you will be able to find more at http://www.kaashoek.com/comskip/*

###### FFMPEG vs Handbrake
FFMPEG was tested as faster and more efficient when running benchmarked tests for this application. If you wish to test and swap out FFMPEG in favor of Handbrake, please do the following:
1. Install Handbrake and Handbrake CLI with brew.
```shell
brew install handbrake
```
2. Test Handbrake using the `ffmpeg-vs-handbreak.py` file and manually compare the results.
```shell
python <path_to_repo>/Plex-Scripts/ffmpeg-vs-handbreak.py> <path_to_video>
```
3. Swap out relevant code between `script.py` and `ffmpeg-vs-handbreak.py` based on your compression preference
