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

# Example usage:
if __name__ == "__main__":
    sample_list = [64, 34, 25, 12, 22, 11, 90]
    print("Original list:", sample_list)
    
    sorted_list = bubble_sort(sample_list)
    print("Sorted list:  ", sorted_list)




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

# Example usage:
if __name__ == "__main__":
    sample_list = [12, 11, 13, 5, 6]
    print("Original list:", sample_list)
    
    sorted_list = insertion_sort(sample_list)
    print("Sorted list:  ", sorted_list)
