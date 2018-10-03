#!/bin/bash
killall -s SIGKILL python
killall -s SIGKILL gzserver
killall -s SIGKILL run-analyzer
killall -s SIGKILL body-analyzer
killall -s SIGKILL gazebo
