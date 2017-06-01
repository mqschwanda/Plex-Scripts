#!/usr/bin/python

import ConfigParser
import logging
import os
import subprocess
import sys
import tempfile
import uuid

# Configure process from file
config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.conf')
if not os.path.exists(config_file_path): # check for config file and exit process if ti does not exist
  print 'Config file not found: %s' % config_file_path
  print 'Make a copy of config.conf.example named config.conf, modify as necessary, and place in the same directory as this script.'
  sys.exit(1)
# read the file into configuration
config = ConfigParser.SafeConfigParser({'comskip-ini-path' : os.path.join(os.path.dirname(os.path.realpath(__file__)), 'comskip.ini'), 'temp-root' : tempfile.gettempdir(), 'nice-level' : '0'})
config.read(config_file_path)
# global variable config
FFMPEG_PATH = os.path.expandvars(os.path.expanduser(config.get('Helper Apps', 'ffmpeg-path')))
LOG_FILE_PATH = os.path.expandvars(os.path.expanduser(config.get('Logging', 'logfile-path')))
CONSOLE_LOGGING = config.getboolean('Logging', 'console-logging')
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
# On to the actual work....
try:
  video_path = sys.argv[1]
  logging.info('Using input file: %s' % video_path)
  original_video_dir = os.path.dirname(video_path)
  video_basename = os.path.basename(video_path)
  video_name, video_ext = os.path.splitext(video_basename)
except Exception, e:
  logging.error('Something went wrong setting up temp paths and working files: %s' % e)
  sys.exit(0)
# Compress with Handbreak.
try:
  logging.info('Starting video compression!')
  handbreak_output = os.path.join(original_video_dir, '.'.join(['handbreak','mp4']))

  HandBreakCLI = ['HandBrakeCLI', '--input', video_path, '--output', handbreak_output, '--optimize']
  video_format = ['--format', 'mp4', '--encoder', 'x264', '--quality', '20.0', '--maxWidth', '1920', '--maxHeight', '1080', '--rate', '30']
  audio_format = ['--aencoder', 'av_aac', '--ab', '128', '--mixdown', 'stereo']
  cmd = HandBreakCLI + video_format + audio_format
  logging.info('[HandBreakCLI] Command: %s' % cmd)
  subprocess.call(cmd)
  logging.info('Done compressing!')
except Exception, e:
  logging.error('Problem compressing file: %s' % video_path)
  logging.error(str(e))
# Compress with FFMPEG.
try:
  logging.info('Starting video compression!')
  ffmpeg_output = os.path.join(original_video_dir, '.'.join(['ffmpeg','mp4']))
  FFMPEG_ARGS = [FFMPEG_PATH, '-y', '-i', video_path, ffmpeg_output]
  video_format = ['-vcodec', 'h264', '-r', '30', '-crf', '20', '-vf', "scale=min'(1920,iw)':-2", '-movflags', 'faststart']
  audio_format = ['-acodec', 'aac','-ab','128k']
  cmd = FFMPEG_ARGS + video_format + audio_format
  logging.info('[ffmpeg] Command: %s' % cmd)
  subprocess.call(cmd)
  logging.info('Done compressing!')
except Exception, e:
  logging.error('Problem compressing file: %s' % ffmpeg_input)
  logging.error(str(e))
