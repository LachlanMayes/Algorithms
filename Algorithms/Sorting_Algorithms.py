def insertion_sort_descending(students: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    Sorts a list of students by score in descending order using Insertion Sort.
    Maintains stability (equal scores retain original relative order).
    """
    arr = students.copy()
    print("Initial State:", arr, "\n")
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        print(f"--- Iteration {i}: Inserting {key} ---")
        
        # Shift elements to the right if their score is strictly LESS than the key's score.
        # Strict inequality (<) ensures stability for equal scores.
        while j >= 0 and arr[j][1] < key[1]:
            print(f"  Comparison: {arr[j][1]} < {key[1]} -> True (Shifting {arr[j]} right)")
            arr[j + 1] = arr[j]
            j -= 1
            
        if j >= 0:
            print(f"  Comparison: {arr[j][1]} < {key[1]} -> False (Stopping)")
            
        # Insert the key into its correct position
        arr[j + 1] = key
        print(f"  Action: Inserted {key} at index {j + 1}")
        print(f"  State after pass {i}: {arr}\n")
        
    return arr

# Given Data
students_list =[("Alice", 85), ("Bob", 90), ("Charlie", 85), ("David", 92), ("Eve", 90)]
insertion_sort_descending(students_list)


def k_cheapest_selection_sort(prices: list[int], k: int) -> list[int]:
    """
    Finds the K smallest elements in a list using Selection Sort logic.
    Stops after K iterations for efficiency.
    """
    arr = prices.copy()
    print("Initial list:", arr, "\n")
    
    for i in range(k):
        min_idx = i
        # Find the minimum element in the remaining unsorted portion
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
                
        # Swap the found minimum with the first unsorted position
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        
        print(f"Iteration {i + 1}: Found minimum {arr[i]}. Swapped with index {min_idx}.")
        print(f"List state: {arr}\n")
        
    return arr[:k]

# Given Data
prices =[299, 150, 89, 199, 49, 120]
k_cheapest_selection_sort(prices, k=3)