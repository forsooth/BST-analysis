# BST Vizualization & Analysis Toolkit
A toolkit for working with and reasoning about binary search trees, particularly their 2D geometric representation and the visual results of the time complexity of various BST operations. Visit [wikipedia](https://en.wikipedia.org/wiki/Geometry_of_binary_search_trees) for a quick summary of the problem of dynamic optimality and its relationship to 2D geometric plots, or read below.

![A Binary Search Tree](/img/example_rb.png?raw=true)

# Introduction

This project was started by Matt Asnes and Harrison Kaiser, for COMP-150-08: Topics on Algorithms, Graphs and Data Structures, in Spring 2017.

## Summary of 2D Geometric BST Interpretation

This utility provides a framework and a series of tools for analysis of various BST algorithms, and provides an interface for creating and testing others. The idea behind the project is as follows:

* BSTs perform a set of tasks (insert, search, delete) on a single input value; together, we term this task and argument an 'operations'
* Given a single operation, a given BST algorithm will travel a deterministic path from one permutation of the data structure state to another
* Given a static sequence of operations, a given BST algorithm will travel a deterministic path from one permutation of the data structure state to another
* The time complexity of any given operation is determined solely by the number of nodes in the tree which are traversed along the way
* Given the above, it follows that given a sequence of operations and some BST algorithm, we can reason about the time complexity of that sequence of operations — we simply assume that accessing each element takes some fixed time cost regardless of the element, and look at the frequency of accesses
* Furthermore, we can tell explicitly how much of that time is allocated to each operation — were some unusually slow or fast?
* We can also tell explicitly how much of the time is allocated to each element in the BST — were some accessed unusually frequently?
* Given the above, we know the distribution of the runtime across both the BST values and the operations being performed
* Since we know the time in terms of element accesses along two directions, it makes sense to plot this in two dimensions
* When plotting, we find that we have a set of points, and that the problem of dynamic BST optimality is cast into this realm
* Due to some clever geometric interpretation, the problem becomes to plot the operations in 2D, and minimize the number of additional points which must be inserted to create a set of points where, for any pair of points, no rectangle of nonzero area can be drawn with these points at its corners without having another point within it or on its boundaries
* This 2D grapical representation of a BST is the result we generate here

## Extract from Example Output

![Example BST analysis output for a red-black tree](/img/example_output.png?raw=true)

# Architecture

We attempt to represent the abstractions here in the structure of the project. As such the process of a tree performing operations goes as follows:

* Operations are sent to the program in a text file, containing a series of operation codes and arguments
* The operations are sent one at a time to the BST
* The BST algorithm interfaces with an API for common BST operations, and cannot modify the structure of the tree directly — the BST algorithm only has access to a single node at a time, in addition to the root, and must traverse the tree to perform any operations. This allows us to have the algorithm abstracted away from the rest of the process, such that writing an algorithm requires only meeting an interface and interacting with our API
* The tree completes its operations, and in the background the API logs which nodes have been accessed at each operation timestep
* The data from those logs are sent to a plotting system which generates diagrams and output files which can be viewed by the user

## Architecture Diagram

![Architecture diagram for the program](/img/arch.png?raw=true)


# Dependencies

## System dependencies:

| Tool              | Versions Tested                | Purpose
|-------------------|--------------------------------|-----------------------
| x64 Linux         | Fedora 25, Ubuntu 14.04.5 LTS  | Allows us to assume conventions of a UNIX environment
| Python 3          | 3.6.0, 3.4.3                   | Allows us to standardize our Python code
| bash              | 4.3.43, 3.3.11                 | Shell scripting for managing the many program settinga
| evince            | 3.22.1, 3.10.3                 | PDF/PS viewer to see output (assumed installed by display script, non-breaking if not present)

## Fonts:

The project will behave as expected without this font installed, but the PostScript files produced reference it.

| Font Name        |
|------------------|
| Input Mono       |

## External Python dependencies:

| Package     | Version  | Purpose                                  
|-------------|---------:|-------------------------------------------------------------
| numpy       | 1.12.1   | Keep track of vectors holding data, perform faster graphing operations
| matplotlib  | 2.0.0    | Plot and format our data
| graphviz    | 0.6      | Draw the diagram of our tree
| PyX         | 0.14.1   | Move and combine PS and EPS files for output

## Standard Python dependencies:

| Package     | Purpose
|-------------|-------------------------------------------------------------
| sys         | Print debug messages
| os          | Create and manage temporary files on disk
| argparse    | Parse command line arguments
| datetime    | Version output files
| shlex       | String parsing for operations files


# Operations File Format

The conventional file extension for our operations file input is `.ops`. The file can contain any number of lines; lines beginning with the character '#' are considered comments and are ignored. Lines containing only whitespace are ignored. 

A valid line consists of a single operation and a single argument. Valid operations are as follows:

| Operation | Meaning
|-----------|---------------------------------------------
| `ins`     | Insert the following element into the tree
| `sea`     | Search for the following element in the tree
| `del`     | Delete the following element from the tree

All operations take the same arguments. A valid argument is either a single integer, a single floating point number, or a single string wrapped in double quote characters (`"`). A valid string may contain whitespace, but may not contain double quote characters. 

The operation may be separated from its argument by any number of spaces.

An example `*.ops` file is as follows:

```
# Example operations
ins 8
ins 9
ins 15
ins 19
ins 8
ins 14
ins 13
sea 12
del 9
del 6
# Blank line:

sea 16
sea 19
sea 8
sea 2
ins 19
ins 2
sea 8
sea 2
``` 

Note that string arguments to operations can be generated by `input_gen`, but not plotted by `main` as of now.

# Program Execution

The project is split into two main components: `input_gen` and `main`. These two Python files are executable, and take command line arguments. They are detailed as follows:

## Input Generation

This program generates a list of operations in the format required by the main workflow. Several command line options exist to set constraints on and customize the generated operations. By default, however, the program generates 75 operations, beginning with 25 inserts followed by mixed searches and deletes. By default, the arguments to these operations are integers between 1 and 20, distributed randomly. The output is not written to disk by default, but rather is printed to standard output. By default, and in a way that cannot be disabled, the last run operations are written to the `inputs/last_run.ops` file, in case anything interesting occurs.

### Input Command-Line Options

| Flag or Option | Expanded Name               | Argument Type | Description
|----------------|-----------------------------|---------------| -----------------------
| `-h`             | `--help`                      | None          | Displays a summary of this information and exits.
| `-p`             | `--pattern`                   | `string`        | The pattern of operation types to generate. Each character in the string is interpreted as a set of operations of the desired type. Allowed characters are `i`, `I`, `s`, `S`, `d`, and `D`, corresponding to insert, search, and delete respectively. A capital letter denotes that these operations should appear in a discrete block at the current position in the operation chain, whereas a lowercase letter indicates that the operation can be mixed with other operation types. For example, the pattern `IidisiD` will perform `n` inserts, followed by `5n` operations which form a random mix of inserts, searches, and deletes with a 3:1 ratio of inserts to other operations, followed by `n` deletes. If an input distribution is specified, that distribution applies to all occurances of the operation class and limits are taken over all instances; that is, if the pattern is `ISI`, and the insertion distribution is `increasing`, the second band of inserts will pick up where the first left off.
| `-n`             | `--number`                    | `int` > 0       | The number of operations to generate for each character in the pattern argument. In a way this is the granularity of control present in the pattern of operations generated. 
| `-t`             | `--type`                      | `string`        | The type of input to generate. Allowed values correspond to the allowed types of input, and are as follows: `int`, `float`, `str`.
|`-u`              | `--max`                       | `int`           | The upper bound on the arguments being generated for the operations. No operation will be generated with an argument higher than this.
|`-l`              | `--min`                       | `int`           | The lower bound on the arguments being generated for the operations. No operation will be generated with an argument lower than this.
| `-id`            | `--ins_distribution`          | `string`        | The distribution of values to use for the insert operations being generated. Refer to the distribution table below for allowed values.
| `-sd`            | `--sea_distribution`          | `string`        | The distribution of values to use for the search operations being generated. Refer to the distribution table below for allowed values.
| `-dd`            | `--del_distribution`          | `string`        | The distribution of values to use for the delete operations being generated. Refer to the distribution table below for allowed values.
| `-w`             | `--write`                     | None          | If this flag is present, the input_gen program will write the generated operations to a file in the `inputs/` directory in addition to printing the operations to standard output. The file name of the new file will be a timestamp of the time at which the program began writing to file, with the extension `.ops`.


### Distributions

The following are allowed arguments to the distribution arguments:

| Distribution           | Description
|------------------------|--------------------------------------------
| random                 | Generates arguments with a uniform random distribution between the upper and lower limits
| increasing             | Generates arguments with monotonically increasing values, starting from the lower limit and increasing until the upper limit
| decreasing             | Generates arguments with monotonically decreasing values, starting from the lower limit and increasing until the upper limit
| gaussian               | Generates arguments with a gaussian random distribution between the upper and lower limits, with a mean of the average of the upper and lower limits and a standard deviation of the average of the upper and lower limits divided by 10. The upper and lower limits themselves will always be included in the output, halfway through the generated values. 
| balanced               | Generates arguments which create a perfectly balanced simple BST, i.e. the average of the upper and lower limits is inserted first, then the value halfway between the lower limit and the average, then the value halfway between the average and the upper limit, etc.
| nearly_increasing      | Generates arguments which are monotonically increasing, and applies some jitter such that the arguments end up increasing overall with high probability.
| nearly_decreasing      | Generates arguments which are monotonically decreasing, and applies some jitter such that the arguments end up decreasing overall with high probability.
| spider                 | Generates `n/5` arguments randomly distributed between the lower limit and `1/5` of the range (i.e. `upper limit – lower limit`), followed by `3n/5` arguments monotonically increasing values starting from `1/5` of the range and going until `4/5` of the range, followed by `n/5` arguments randomly distributed between `4/5` of the range and the upper limit. 


### Input Execution

Run `python3 input_gen.py` with the desired arguments.

## BST Analysis (Main)

This program generates a list of operations in the format required by the main workflow. Several command line options exist to set constraints on and customize the generated operations. By default, however, the program generates 75 operations, beginning with 25 inserts followed by mixed searches and deletes. By default, the arguments to these operations are integers between 1 and 20, distributed randomly. The output is not written to disk by default, but rather is printed to standard output.

### Main Command-Line Options

| Flag or Option | Expanded Name               | Argument Type | Description
|----------------|-----------------------------|---------------| -----------------------
| operations     | N/A                         | string        | **Required Field:** This argument is positional, and should contain the filename of the operations to run the algorithm on. If the input operations are sent to the program via standard input, the value `-` can be provided to inform the program that it should be reading from standard input. Multiple files can be specified, and will be concatenated before the program is executed.
| `-h`           | `--help`                    | None          | Displays a summary of this information and exits.
| `a`            | `--algorithm`               | `string`      | The BST algorithm to use. Refer to the algorithms table below for allowed values. The default algorithm to use is `simple`
| `-d`           | `--debug`                   | None          | Enable debugging mode with debug level `1`. If the `--debug_level` flag is also specified, that value takes precendence.
| `-l`           | `--debug-level`             | `int`         | The debugging level to use. Refer to the debug level table below for allowed values.
| `-p`           | `--pages`                   | None          | Enable generation of multi-page output. If this flag is enabled then instead of the basic plot, a page will be appended to the output PostScript file for each operation given as input, showing the tree as it was after that operation was executed, along with the plot as it was up until that point. Axes on the plot are scaled absolutely relative to the final output.
| `-g`           | `--graphs`                  | None          | Enable generation of graph diagrams of the trees in question; if `--pages` is enabled, the tree is drawn for every operation. Otherwise, only the final tree is drawn. 
| `-c`           | `--clean_off`                  | None          | Turn off the default behavior of cleaning up files in the `tmp/` folder, including EPS diagrams of each plot and tree, and DOT formatted graphs.

### Algorithms

| Algorithm Name       | Valid Strings Passed to the `-a` Option                                               | Description
|----------------------|--------------------------------------------------------------------------|-------------------
| Simple BST           | `simple`, `bst`, `simplebst`                                             | A simple binary search tree, which performs no auxillary operations other than the search, insert, or deletion required. The first node inserted will remain the root until it is deleted.
| Red Black Tree       | `rb`, `redblack`, `redblacktree`                                         | A balanced binary search tree where nodes are colored red or black such that the number of black nodes in any path from the root to a leaf is the same, and no red node has a red parent. The tree is balanced via rotations.
| Splay Tree           | `splay`, `splaytree`                                                     | A binary search tree where a node is brought to the root after it is accessed via search or insertion. The action of bringing a node to the root is known as 'splaying', and is performed by a series of action called 'splays', which are algorithmic sequences of rotations.
| AVL Tree             | `avl`, `avltree`                                                         | A strictly balanced binary search tree where for every node, the heights of both subtrees differ by no more than 1. 
| WAVL Tree            | `wavl`, `wavltree`, `weakavl`, `weakavltree`                             | A less strict variant of AVL trees, requiring that for every node, the heights of both subtrees differ by no more than 2. WAVL trees maintain the `1.44 log(n)` maximum height difference of an AVL tree (over the `2 log(n)` maximum height difference of a red-black tree) while performing only a constant number of rotations at most when structuring the tree, a number which could be linear for a regular AVL tree.
| Tango Tree           | `tango`, `tangotree`                                                     | A BST variant implemented as a tree of trees which achieves a competitve ratio with the optimal static BST.
| Optimal Static BST   | `static`, `osbst`, `optimalstatic`, `opt`, `optbst`, `optimalstaticbst`  | Given a set of insertions followed by a set of searches, this is (provably) the best possible orientation of the inserted values in a BST for that set of searches.


### Debugging Levels

| Debug Level | Name      | Description
|-------------|-----------|-------------------------------------
| 0           | NONE      | Debugging off, no text is printed to standard output or standard error.
| 1           | SIMPLE    | No text is printed to standard output. On standard error, initial debug mode confirmation text is printed, notification is printed on successful generation of DOT in memory for each graph if `-g` is enabled, if the total number of operations being performed is under 50, a representation of the tree is printed out upon the last operation's termination, information is printed when `tmp/` directory is being created, information is printed whenever a new matplotlib or graphviz EPS diagram is saved to disk, prints debug information when concatenating two pages, prints filename information when saving final file.
| 2          | VERBOSE    | No text is printed to standard output. On standard error, initial debug mode confirmation text is printed, notification is printed on successful generation of DOT in memory for each graph if `-g` is enabled, each operation's text is printed, each move left or more right is printed, a textual representation of the tree is printed after each operation, information is printed when `tmp/` directory is being created, each step of the plot generation process is printed, information is printed whenever a new matplotlib or graphviz EPS diagram is saved to disk, the bounding box for each read EPS file is printed, and the final file name is printed when saving to disk.
| 3          | VERIFY    | No text is printed to standard output. On standard error, initial debug mode confirmation text is printed, notification is printed on successful generation of DOT in memory for each graph if `-g` is enabled, each operation's text is printed, each move left or more right is printed, a textual representation of the tree is printed before *and* after each operation, the tree's BST and red-black properties are verified after each operation, information is printed when `tmp/` directory is being created, each step of the plot generation process is printed, information is printed whenever a new matplotlib or graphviz EPS diagram is saved to disk, the bounding box for each read EPS file is printed, invisible formatting nodes are shown in the output file in the tree diagrams, and the final file name is printed when saving to disk.

### Main Execution

Run `python3 main.py` with the desired arguments.

## Scripting

The above programs have many arguments, so we have made the process fairly easy by providing two bash scripts. The first, `run.sh`, contains variables in heavily-commented bash for each argument one might want to change, and then calls `input_gen.py` and pipes its output into `main.py`, producing the desired results. `run.sh` then calls our second script, `display.sh`, which simply displays the last output `*.ps` file in the `outputs/` directory in `evince`.

# Further (Wikipedia) Reading

* https://en.wikipedia.org/wiki/Geometry_of_binary_search_trees
* https://en.wikipedia.org/wiki/Binary_search_tree
* https://en.wikipedia.org/wiki/Red–black_tree
* https://en.wikipedia.org/wiki/Splay_tree
* https://en.wikipedia.org/wiki/AVL_tree
* https://en.wikipedia.org/wiki/WAVL_tree
* https://en.wikipedia.org/wiki/Tango_tree
* https://en.wikipedia.org/wiki/Optimal_binary_search_tree

# Further (Academic) Reading

* ["The Geometry of Binary Search Trees"](http://cseweb.ucsd.edu/~dakane/geometryofbst.pdf) — introduces the 2D geometric intepretation of BSTs
* ["Dynamic Optimality — Almost"](http://erikdemaine.org/papers/Tango_SICOMP/paper.pdf) — introduces tango trees 
* ["Optimum Binary Search Trees"](http://download.springer.com/static/pdf/947/art%253A10.1007%252FBF00264289.pdf?originUrl=http%3A%2F%2Flink.springer.com%2Farticle%2F10.1007%2FBF00264289&token2=exp=1493015864~acl=%2Fstatic%2Fpdf%2F947%2Fart%25253A10.1007%25252FBF00264289.pdf%3ForiginUrl%3Dhttp%253A%252F%252Flink.springer.com%252Farticle%252F10.1007%252FBF00264289*~hmac=6a864dba682590a7c44f3ba4239c412e4d96d10f5531a4eb6943ebf6535953c4) — Knuth's original introduction of optimal static BSTs
* ["In Pursuit of the Dynamic Optimality Conjecture"](https://link.springer.com/chapter/10.1007%2F978-3-642-40273-9_16) — summary of the dynamic optimality problem over the last 30 years


# TODO List

### Matt
* Fix formatting to pass PyLint
* Add percent completion to ongoing output in debug mode 0
* Stamp generated operation output with commented CLI flags & dates
* Add CLI option to track only ins/sea/del
* Add CLI option to track only after operation N
* Figure out how font embedding works in graphviz digrams
* Go through and improve code commenting and clarity

### Harrison
* Make AVL tree
* Make WAVL tree
* Go through and improve code commenting and clarity
* Re-factor RedBlack Tree
* Make verification and __str__ for be independent of BST type

### You
* Try out our code!
* If you find any issues, please file them through GitHub's issues system
