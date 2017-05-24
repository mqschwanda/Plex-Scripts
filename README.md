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

####### Ini file
You can find ini files at:
http://www.kaashoek.com/comskip/
