#!/bin/bash
set -eEuo pipefail
IFS=$'\n\t'
d=$(dirname $0)

# The data type of the values being moved around in the tree
# Allowed values: 'int', 'float', 'str'
OPERATION_TYPE='int'

numops=$1

# The number of operations to perform for each character in the pattern.
# Allowed values: Any integer greater than 0
NUM_OPERATIONS=$numops

# The lowest value which will appear in the tree. Option will be ignored if
# the data type is string.
LOWEST_DATA_VALUE=0

# The highest value which will appear in the tree. Option will be ignored if
# the data type is string.
HIGHEST_DATA_VALUE=$numops

# The distribution of the values that the insert operations take.
# Allowed values: 'random', 'increasing', 'decreasing', 'balanced'
INSERT_OPERATION_DISTRIBUTION='random'
# INSERT_OPERATION_DISTRIBUTION='increasing'

# The distribution of the values that the search operations take.
# Allowed values: 'random', 'increasing', 'decreasing', 'balanced'
SEARCH_OPERATION_DISTRIBUTION='random'

# The distribution of the values that the delete operations take.
# Allowed values: 'random', 'increasing', 'decreasing', 'balanced'
DELETE_OPERATION_DISTRIBUTION='random'

# The pattern defining the way in which operations are printed out.
# For each character in this pattern, exactly NUM_OPERATIONS 
# operations will be generated. Capital letters denote that this
# section of operations should not be mixed with the ones around it;
# lowercase letters denote that all lowercase letters around this one
# should be treated as one field, such that 'isi' generates
# 3 * NUM_OPERATIONS operations with a ratio of two inserts to one search
# but with no guarantees on the exact number of either.
OPERATION_PATTERN='I'

# Whether to write to a file or not. Boolean value.
# Allowed values: 'True', 'False'
WRITE_TO_FILE='True'

# Whether to run the operations generated through a BST.
# Allowed values: 'True', 'False'
RUN_OPERATIONS='True'

# BST algorithm to run the operations on.
# Allowed values: 'simple', 'rb', 'splay', 'avl', 'wavl', 'tango', 'static'

# BST_ALGORITHM='splay'
# BST_ALGORITHM='simple'
BST_ALGORITHM='rb'

# Whether to display the output graph.
# Allowed values: 'True', 'False'
DISPLAY_OUTPUT_GRAPH='True'

# Whether to print debug information
# DEBUG='True'
DEBUG='True'

# Whether to create a multi-page PDF aninmating the results, or just a
# one page pdf of the final output.
# Allowed values: 'True', 'False'
# ANIMATE='True'
ANIMATE='False'

# Whether to include pictures of the tree in the output data. 
# Allowed values: 'True', 'False'
TREE_PICTURE='True'

cmd="python3 $d/src/input_gen.py -n $NUM_OPERATIONS -t $OPERATION_TYPE -l $LOWEST_DATA_VALUE -u $HIGHEST_DATA_VALUE -id $INSERT_OPERATION_DISTRIBUTION -sd $SEARCH_OPERATION_DISTRIBUTION -dd $DELETE_OPERATION_DISTRIBUTION -p $OPERATION_PATTERN"

write_cmd=" -w"

run_cmd=" | python3 $d/src/main.py - -a $BST_ALGORITHM"

debug_cmd=" -d"

animate_cmd=" -p"

treepic_cmd=" -g"

display_cmd=" && $d/display.sh"

if [[ "$WRITE_TO_FILE" == "True" ]]; then
	cmd="$cmd$write_cmd"
fi

if [[ "$RUN_OPERATIONS" == "True" ]]; then
        cmd="$cmd$run_cmd"
fi

if [[ "$DEBUG" == "True" ]]; then
        cmd="$cmd$debug_cmd"
fi

if [[ "$ANIMATE" == "True" ]]; then
	cmd="$cmd$animate_cmd"
fi

if [[ "$TREE_PICTURE" == "True" ]]; then
        cmd="$cmd$treepic_cmd"
fi

if [[ "$DISPLAY_OUTPUT_GRAPH" == "True" ]]; then
        cmd="$cmd$display_cmd"
fi

eval "$cmd"

exit


