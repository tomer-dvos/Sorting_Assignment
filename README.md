# Sorting_Assignment

## Student Names
Tomer Dvoskin  
Maya Mashiah

## Selected Algorithms
- Bubble Sort (ID 1)
- Selection Sort (ID 2)
- Merge Sort (ID 4)


## Figure 1: Random Arrays (`result1.png`)
![result1](result1.png)

This figure compares running times on random arrays as input size increases.
Merge Sort grows more slowly than Bubble Sort and Selection Sort, which is consistent with expected complexity.

## Figure 2: Nearly Sorted Arrays (`result2.png`)
![result2](result2.png)

In the nearly sorted experiment (`-e 1` for 5% noise or `-e 2` for 20% noise), running times change because the input is closer to sorted order.
Bubble Sort usually improves due to early stopping, Selection Sort changes less because it still scans for the minimum each pass, and Merge Sort stays efficient.
