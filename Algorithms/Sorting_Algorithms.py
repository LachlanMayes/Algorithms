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


def optimized_bubble_sort(ratings: list[float]) -> list[float]:
    """
    Sorts a list using an optimized Bubble Sort.
    If no swaps occur during a pass, the list is sorted and the algorithm terminates.
    """
    arr = ratings.copy()
    n = len(arr)
    print("Initial ratings:", arr, "\n")
    
    for i in range(n):
        swapped = False
        print(f"--- Pass {i + 1} ---")
        
        # We can ignore the last 'i' elements as they are already in place
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                print(f"  Swapping {arr[j]} and {arr[j+1]}")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                
        print(f"State after pass {i + 1}: {arr}\n")
        
        # Optimization: break early if the array is already sorted
        if not swapped:
            print("No swaps occurred. The list is sorted. Early exit!")
            break
            
    return arr

# Given Data
ratings =[4.5, 3.2, 5.0, 2.8, 4.0, 3.8]
optimized_bubble_sort(ratings)

def merge_sort_orders(orders: list[dict]) -> list[dict]:
    """
    Sorts a list of order dictionaries by total purchase amount.
    Guarantees O(n log n) complexity.
    """
    if len(orders) <= 1:
        return orders
        
    # 1. Divide
    mid = len(orders) // 2
    left_half = merge_sort_orders(orders[:mid])
    right_half = merge_sort_orders(orders[mid:])
    
    # 2. Conquer & Merge
    return merge(left_half, right_half)

def merge(left: list[dict], right: list[dict]) -> list[dict]:
    sorted_list =[]
    i, j = 0, 0
    
    # Compare elements from left and right halves
    while i < len(left) and j < len(right):
        if left[i]["amount"] <= right[j]["amount"]:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
            
    # Append any remaining elements
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    
    return sorted_list
