#!/bin/bash
set -eEuo pipefail
IFS=$'\n\t'
goodc="\033[38;5;10m"
qc="\033[38;5;222m"
badc="\033[38;5;09m"
noc="\033[38;5;15m"
d=$(dirname "$0")

evince "outputs/$(ls -tr -1 outputs/ | tail -1)" 2>/dev/null &

