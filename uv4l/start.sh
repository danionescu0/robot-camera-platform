#!/bin/bash

uv4l -nopreview --auto-video_nr --driver raspicam --encoding mjpeg --width 480 --height 360 --framerate 10 \
--server-option '--port=9090' --server-option '--max-queued-connections=5' \
--server-option '--max-streams=3' --server-option '--max-threads=29' \
--server-option '--user-password=your_password' \