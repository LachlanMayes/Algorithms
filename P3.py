# ==========================================
# PROBLEM 3: SEARCHING SYSTEM (AVL TREE)
# ==========================================

class AVLNode:
    def __init__(self, weight, item_id):
        self.weight = weight
        self.item_id = item_id
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, weight, item_id):
        if not root:
            return AVLNode(weight, item_id)
        elif weight < root.weight:
            root.left = self.insert(root.left, weight, item_id)
        else:
            root.right = self.insert(root.right, weight, item_id)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Rotations to maintain O(log N) balance
        if balance > 1 and weight < root.left.weight:
            return self.right_rotate(root)
        if balance < -1 and weight > root.right.weight:
            return self.left_rotate(root)
        if balance > 1 and weight > root.left.weight:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and weight < root.right.weight:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_height(self, root):
        if not root: return 0
        return root.height

    def get_balance(self, root):
        if not root: return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def search_closest(self, root, target_weight):
        closest_node = None
        min_diff = float('inf')
        current = root

        while current:
            diff = abs(current.weight - target_weight)
            if diff < min_diff:
                min_diff = diff
                closest_node = current
            
            if current.weight == target_weight:
                break
            elif current.weight > target_weight:
                current = current.left
            else:
                current = current.right
                
        return closest_node