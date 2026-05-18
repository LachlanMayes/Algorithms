# ==========================================
# PROBLEM 2: SORTING ALGORITHMS & BENCHMARK
# ==========================================
import random
import time
# import matplotlib.pyplot as plt # Uncomment to generate graphs

def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right =[x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- Optimized QuickSort ---
def insertion_sort_sub(arr, low, high):
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def optimized_quicksort(arr, low, high):
    while low < high:
        if high - low < 10: # Switch to insertion sort for small sublists
            insertion_sort_sub(arr, low, high)
            break
        else:
            # Median of three pivot
            mid = (low + high) // 2
            if arr[low] > arr[mid]: arr[low], arr[mid] = arr[mid], arr[low]
            if arr[low] > arr[high]: arr[low], arr[high] = arr[high], arr[low]
            if arr[mid] > arr[high]: arr[mid], arr[high] = arr[high], arr[mid]
            
            arr[mid], arr[high] = arr[high], arr[mid]
            pivot = arr[high]
            
            i = low - 1
            for j in range(low, high):
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            pi = i + 1
            
            if pi - low < high - pi:
                optimized_quicksort(arr, low, pi - 1)
                low = pi + 1
            else:
                optimized_quicksort(arr, pi + 1, high)
                high = pi - 1

# Note: MergeSort, HeapSort, Standard InsertionSort, and SelectionSort 
# should be implemented similarly here.

def benchmark():
    sizes =[1000, 5000, 10000] # Truncated for example
    for size in sizes:
        test_data =[random.randint(1, 100000) for _ in range(size)]
        
        start = time.time()
        quick_sort(test_data.copy())
        print(f"QuickSort {size}: {time.time() - start} sec")
        
        # Test Optimized
        opt_data = test_data.copy()
        start = time.time()
        optimized_quicksort(opt_data, 0, len(opt_data)-1)
        print(f"Optimized QuickSort {size}: {time.time() - start} sec")

benchmark()