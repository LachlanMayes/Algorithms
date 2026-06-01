def bubble_sort(arr):
    n = len(arr)
    
    # Traverse through all array elements
    for i in range(n):
        # Track whether any swaps occur in this pass
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                
        # If no elements were swapped in the inner loop, the list is sorted
        if not swapped:
            break
            
    return arr




def insertion_sort(arr):
    # Traverse from the second element (index 1) to the end of the array
    for i in range(1, len(arr)):
        key = arr[i]
        
        # Move elements of arr[0..i-1] that are greater than the key
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            
        # Place the key at its correct position
        arr[j + 1] = key
        
    return arr


def selection_sort(arr, verbose=False):
    # Sorts a list in-place using the Selection Sort algorithm.
    n = len(arr)
    
    for i in range(n):
        # 1. Assume the first unsorted element is the minimum
        min_index = i
        
        # 2. Scan the rest of the unsorted elements to find the actual minimum
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        
        # 3. Swap the minimum element with the first unsorted element
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
            if verbose:
                print(f"Step {i+1}: Swapped index {min_index} and {i} -> {arr}")
        else:
            if verbose:
                print(f"Step {i+1}: Element {arr[i]} is already in position -> {arr}")
                
    return arr


def merge_sort(arr):
    # Base case: if the list has 1 or 0 elements, it is already sorted
    if len(arr) <= 1:
        return arr

    # Find the middle point and split the list
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # Merge the sorted halves and return the result
    return merge(left_half, right_half)


def merge(left, right):
    sorted_list = []
    i = j = 0

    # Compare elements from both lists and build the sorted list
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    # Append any leftover elements from the left or right list
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])

    return sorted_list



def quicksort(arr):
    # Base case: arrays with 0 or 1 element are already sorted
    if len(arr) <= 1:
        return arr
    
    # Choose a pivot (we will use the middle element here)
    pivot = arr[len(arr) // 2]
    
    # Partition the elements into three lists
    left = [x for x in arr if x < pivot]      # Elements smaller than pivot
    middle = [x for x in arr if x == pivot]   # Elements equal to pivot
    right = [x for x in arr if x > pivot]     # Elements greater than pivot
    
    # Recursively sort the left and right, and combine them
    return quicksort(left) + middle + quicksort(right)


def heapify(arr, n, i):
    """
    To heapify a subtree rooted with node i which is an index in arr[].
    n is size of heap.
    """
    largest = i          # Initialize largest as root
    left = 2 * i + 1     # left child index = 2*i + 1
    right = 2 * i + 2    # right child index = 2*i + 2

    # See if left child of root exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # See if right child of root exists and is greater than root
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # Swap

        # Recursively heapify the affected sub-tree
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    # Phase 1: Build a maxheap.
    # We start from the last non-leaf node and work backwards to the root.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Phase 2: One by one extract elements
    for i in range(n - 1, 0, -1):
        # Move current root to end (swap the largest element with the last element)
        arr[i], arr[0] = arr[0], arr[i]
        
        # Call max heapify on the reduced heap
        heapify(arr, i, 0)
