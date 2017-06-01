#!/usr/bin/python

import ConfigParser
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

# Configure process from file
config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.conf')
if not os.path.exists(config_file_path): # check for config file and exit process if ti does not exist
  print 'Config file not found: %s' % config_file_path
  print 'Make a copy of config.conf.example named config.conf, modify as necessary, and place in the same directory as this script.'
  sys.exit(1)

config = ConfigParser.SafeConfigParser({'comskip-ini-path' : os.path.join(os.path.dirname(os.path.realpath(__file__)), 'comskip.ini'), 'temp-root' : tempfile.gettempdir(), 'nice-level' : '0'})
config.read(config_file_path) # read the file into configuration

COMSKIP_PATH = os.path.expandvars(os.path.expanduser(config.get('Helper Apps', 'comskip-path')))
COMSKIP_INI_PATH = os.path.expandvars(os.path.expanduser(config.get('Helper Apps', 'comskip-ini-path')))
FFMPEG_PATH = os.path.expandvars(os.path.expanduser(config.get('Helper Apps', 'ffmpeg-path')))
LOG_FILE_PATH = os.path.expandvars(os.path.expanduser(config.get('Logging', 'logfile-path')))
CONSOLE_LOGGING = config.getboolean('Logging', 'console-logging')
TEMP_ROOT = os.path.expandvars(os.path.expanduser(config.get('File Manipulation', 'temp-root')))
COPY_ORIGINAL = config.getboolean('File Manipulation', 'copy-original')
SAVE_ALWAYS = config.getboolean('File Manipulation', 'save-always')
SAVE_FORENSICS = config.getboolean('File Manipulation', 'save-forensics')
NICE_LEVEL = config.get('Helper Apps', 'nice-level')

# Logging.
session_uuid = str(uuid.uuid4())
fmt = '%%(asctime)-15s [%s] %%(message)s' % session_uuid[:6]
if not os.path.exists(os.path.dirname(LOG_FILE_PATH)):
  os.makedirs(os.path.dirname(LOG_FILE_PATH))
logging.basicConfig(level=logging.INFO, format=fmt, filename=LOG_FILE_PATH)
if CONSOLE_LOGGING:
  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  formatter = logging.Formatter('%(message)s')
  console.setFormatter(formatter)
  logging.getLogger('').addHandler(console)

# Set our own nice level and tee up some args for subprocesses (unix-like OSes only).
NICE_ARGS = []
if sys.platform != 'win32':
  try:
    nice_int = max(min(int(NICE_LEVEL), 20), 0)
    if nice_int > 0:
      os.nice(nice_int)
      NICE_ARGS = ['nice', '-n', str(nice_int)]
  except Exception, e:
    logging.error('Couldn\'t set nice level to %s: %s' % (NICE_LEVEL, e))

# On to the actual work.
try:
  video_path = sys.argv[1]
  logging.info('Using input file: %s' % video_path)

  original_video_dir = os.path.dirname(video_path)
  video_basename = os.path.basename(video_path)
  video_name, video_ext = os.path.splitext(video_basename)

except Exception, e:
  logging.error('Something went wrong setting up temp paths and working files: %s' % e)
  sys.exit(0)

# Compress with FFMPEG.
try:
  logging.info('Starting video compression!')
  ffmpeg_output = os.path.join(original_video_dir, '.'.join(['ffmpeg','mp4']))
  FFMPEG_ARGS = [FFMPEG_PATH, '-y', '-i', video_path, '-preset', 'slow', ffmpeg_output]
  video_format = ['-vcodec', 'h264', '-r', '30', '-crf', '20', '-vf', "scale=min'(1920,iw)':-2", '-movflags', 'faststart']
  audio_format = ['-acodec', 'aac','-ab','128k']
  cmd = NICE_ARGS + FFMPEG_ARGS + video_format + audio_format
  logging.info('[ffmpeg] Command: %s' % cmd)
  subprocess.call(cmd)
  logging.info('Done compressing!')
except Exception, e:
  logging.error('Problem compressing file: %s' % ffmpeg_input)
  logging.error(str(e))
