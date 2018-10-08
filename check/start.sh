#!/bin/bash
rm output.txt
bash check.sh& stdbuf -oL python start.py | tee output.txt
wait
echo "DONE!"
