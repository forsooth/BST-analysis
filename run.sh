#!/bin/bash
set -eEuo pipefail
IFS=$'\n\t'
d=$(dirname $0)

# The data type of the values being moved around in the tree
# Allowed values: 'int', 'float', 'str'
OPERATION_TYPE='int'

# The number of operations to perform for each character in the pattern.
# Allowed values: Any integer greater than 0
NUM_OPERATIONS=30

# The lowest value which will appear in the tree. Option will be ignored if
# the data type is string.
LOWEST_DATA_VALUE=0

# The highest value which will appear in the tree. Option will be ignored if
# the data type is string.
HIGHEST_DATA_VALUE=100

# The distribution of the values that the insert operations take.
# Allowed values: 'random', 'increasing', 'decreasing', 'balanced'
INSERT_OPERATION_DISTRIBUTION='decreasing'

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
WRITE_TO_FILE='False'

# Whether to run the operations generated through a BST.
# Allowed values: 'True', 'False'
RUN_OPERATIONS='True'

# BST algorithm to run the operations on.
# Allowed values: 'simple', 'rb', 'splay', 'avl', 'wavl', 'tango', 'static'
BST_ALGORITHM='simple'

# Whether to display the output graph.
# Allowed values: 'True', 'False'
DISPLAY_OUTPUT_GRAPH='True'

write_run_display="python3 $d/input_gen.py -n $NUM_OPERATIONS -t $OPERATION_TYPE -l $LOWEST_DATA_VALUE -u $HIGHEST_DATA_VALUE -id $INSERT_OPERATION_DISTRIBUTION -sd $SEARCH_OPERATION_DISTRIBUTION -dd $DELETE_OPERATION_DISTRIBUTION -p $OPERATION_PATTERN -w | python3 $d/main.py - -a $BST_ALGORITHM && $d/display.sh"
write_run="python3 $d/input_gen.py -n $NUM_OPERATIONS -t $OPERATION_TYPE -l $LOWEST_DATA_VALUE -u $HIGHEST_DATA_VALUE -id $INSERT_OPERATION_DISTRIBUTION -sd $SEARCH_OPERATION_DISTRIBUTION -dd $DELETE_OPERATION_DISTRIBUTION -p $OPERATION_PATTERN -w | python3 $d/main.py - -a $BST_ALGORITHM"
write="python3 $d/input_gen.py -n $NUM_OPERATIONS -t $OPERATION_TYPE -l $LOWEST_DATA_VALUE -u $HIGHEST_DATA_VALUE -id $INSERT_OPERATION_DISTRIBUTION -sd $SEARCH_OPERATION_DISTRIBUTION -dd $DELETE_OPERATION_DISTRIBUTION -p $OPERATION_PATTERN -w"
run_display="python3 $d/input_gen.py -n $NUM_OPERATIONS -t $OPERATION_TYPE -l $LOWEST_DATA_VALUE -u $HIGHEST_DATA_VALUE -id $INSERT_OPERATION_DISTRIBUTION -sd $SEARCH_OPERATION_DISTRIBUTION -dd $DELETE_OPERATION_DISTRIBUTION -p $OPERATION_PATTERN | python3 $d/main.py - -a $BST_ALGORITHM && $d/display.sh"
run="python3 $d/input_gen.py -n $NUM_OPERATIONS -t $OPERATION_TYPE -l $LOWEST_DATA_VALUE -u $HIGHEST_DATA_VALUE -id $INSERT_OPERATION_DISTRIBUTION -sd $SEARCH_OPERATION_DISTRIBUTION -dd $DELETE_OPERATION_DISTRIBUTION -p $OPERATION_PATTERN | python3 $d/main.py - -a $BST_ALGORITHM"

if [[ "$WRITE_TO_FILE" == "True" ]]; then
	if [[ "$RUN_OPERATIONS" == "True" ]]; then
		if [[ "$DISPLAY_OUTPUT_GRAPH" == "True" ]]; then
			eval "$write_run_display"
		else
			eval "$write_run"
		fi
	else
		if [[ "$DISPLAY_OUTPUT_GRAPH" == "True" ]]; then
			eval "$write_display"
                else
			eval "$write"
                fi
	fi
else
        if [[ "$RUN_OPERATIONS" == "True" ]]; then
                if [[ "$DISPLAY_OUTPUT_GRAPH" == "True" ]]; then
                        eval "$run_display"
		else
			eval "$run"
                fi	
        fi

fi

