#!/bin/bash
d=$(dirname $0)
python $d/../main.py $d/../inputs/ins_1_2_3.ops $d/../inputs/sea_1_2_3.ops $d/../inputs/del_1_2_3.ops
