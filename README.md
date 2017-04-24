# BST Vizualization & Analysis Toolkit
A toolkit for working with and reasoning about binary search trees, particularly their 2D geometric representation and the visual results of the time complexity of various BST operations

![Example BST analysis output for a red-black tree](/img/example.png?raw=true)

## Introduction

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
* This 2D grapical representation of a BST is the result we generate here

