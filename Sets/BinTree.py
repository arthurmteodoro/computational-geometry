class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.insertInLeft = True
        self.height = 0

    def __iter__(self):
        if self.left:
            yield from self.left
        yield self.value
        if self.right:
            yield from self.right


class BinTree(object):
    def __init__(self):
        self.__root = None
        self.__isOrder = True
        self.__len = 0

    @staticmethod
    def __get_height(root):
        if root is None:
            return 0
        else:
            return root.height

    @staticmethod
    def __get_balance(root):
        if root is None:
            return 0
        else:
            return BinTree.__get_height(root.left) - BinTree.__get_height(root.right)

    @staticmethod
    def __right_rotate(root):
        node1 = root.left
        node2 = node1.right

        node1.right = root
        root.left = node2

        root.height = max(BinTree.__get_height(root.left), BinTree.__get_height(root.right)) + 1
        node1.height = max(BinTree.__get_height(node1.left), BinTree.__get_height(node1.right)) + 1

        return node1

    @staticmethod
    def __left_rotate(root):
        node1 = root.right
        node2 = node1.left

        node1.left = root
        root.right = node2

        root.height = max(BinTree.__get_height(root.left), BinTree.__get_height(root.right)) + 1
        node1.height = max(BinTree.__get_height(node1.left), BinTree.__get_height(node1.right)) + 1

        return node1

    @staticmethod
    def __insert_with_function(root, value, func):
        if root is None:
            root = Node(value)
            root.height = 1
            return root

        if func(value, root.value) < 0:
            root.left = BinTree.__insert_with_function(root.left, value, func)
        elif func(value, root.value) > 0:
            root.right = BinTree.__insert_with_function(root.right, value, func)
        else:
            return root

        root.height = 1 + max(BinTree.__get_height(root.left), BinTree.__get_height(root.right))

        balance = BinTree.__get_balance(root)

        if balance > 1 and func(value, root.left.value) < 0:
            return BinTree.__right_rotate(root)
        if balance < -1 and func(value, root.right.value) > 0:
            return BinTree.__left_rotate(root)
        if balance > 1 and func(value, root.left.value) > 0:
            root.left = BinTree.__left_rotate(root.left)
            return BinTree.__right_rotate(root)
        if balance < -1 and func(value, root.right.value) < 0:
            root.right = BinTree.__right_rotate(root.right)
            return BinTree.__left_rotate(root)
        return root

    @staticmethod
    def __insert_without_function(root, value):
        if root is None:
            root = Node(value)
            root.height = 1
            return root

        if root.insertInLeft:
            if root.left is None:
                root.left = Node(value)
                root.insertInLeft = False
            else:
                root.left = BinTree.__insert_without_function(root.left, value)
                root.insertInLeft = False
        else:
            if root.right is None:
                root.right = Node(value)
                root.insertInLeft = True
            else:
                root.right = BinTree.__insert_without_function(root.right, value)
                root.insertInLeft = True

        return root

    def insert(self, value, func=None):
        if self.search(value, func) is None:
            if func is not None:
                self.__root = BinTree.__insert_with_function(self.__root, value, func)
                self.__isOrder = True
            else:
                self.__root = BinTree.__insert_without_function(self.__root, value)
                self.__isOrder = False
            self.__len += 1

    @staticmethod
    def __search_in_avl(root, value, func):
        if root is None:
            return None

        if func(root.value, value) > 0:
            return BinTree.__search_in_avl(root.left, value, func)
        if func(root.value, value) < 0:
            return BinTree.__search_in_avl(root.right, value, func)
        return root

    @staticmethod
    def __search_in_binary_tree(root, value, func):
        if root is None:
            return None

        if func(value, root.value) == 0:
            return root
        else:
            return BinTree.__search_in_binary_tree(root.left, value, func) or \
                   BinTree.__search_in_binary_tree(root.right, value, func)

    @staticmethod
    def __search_without_function(root, value):
        if root is None:
            return None

        if root.value == value:
            return root
        else:
            return BinTree.__search_without_function(root.left, value) or \
                   BinTree.__search_without_function(root.right, value)

    def search(self, value, func=None):
        if func is not None:
            if self.__isOrder:
                return BinTree.__search_in_avl(self.__root, value, func)
            else:
                return BinTree.__search_in_binary_tree(self.__root, value, func)
        else:
            return BinTree.__search_without_function(self.__root, value)

    @staticmethod
    def __get_min_value_node(root):
        if root is None or root.left is None:
            return root

        return BinTree.__get_min_value_node(root.left)

    @staticmethod
    def __delete_in_avl_tree(root, value, func):
        if root is None:
            return None

        if func(value, root.value) < 0:
            root.left = BinTree.__delete_in_avl_tree(root.left, value, func)
        elif func(value, root.value) > 0:
            root.right = BinTree.__delete_in_avl_tree(root.right, value, func)
        else:
            if root.left is None or root.right is None:
                if root.left is None and root.right is None:
                    root = None
                else:
                    if root.left is not None:
                        root = root.left
                    else:
                        root = root.right
            else:
                root.value = BinTree.__get_min_value_node(root.right).value
                root.right = BinTree.__delete_in_avl_tree(root.right, root.value, func)

        if root is None:
            return None

        root.height = 1 + max(BinTree.__get_height(root.left), BinTree.__get_height(root.right))

        balance = BinTree.__get_balance(root)

        if balance > 1 and BinTree.__get_balance(root.left) >= 0:
            return BinTree.__right_rotate(root)
        if balance < -1 and BinTree.__get_balance(root.right) <= 0:
            return BinTree.__left_rotate(root)
        if balance > 1 and BinTree.__get_balance(root.left) < 0:
            root.left = BinTree.__left_rotate(root.left)
            return BinTree.__right_rotate(root)
        if balance < -1 and BinTree.__get_balance(root.right) > 0:
            root.right = BinTree.__right_rotate(root.right)
            return BinTree.__left_rotate(root)
        return root

    @staticmethod
    def __delete_in_binary_tree(root, value, func):
        if root is None:
            return None

        root.left = BinTree.__delete_in_binary_tree(root.left, value, func)
        root.right = BinTree.__delete_in_binary_tree(root.right, value, func)
        if func(root.value, value) == 0:
            if root.left is None or root.right is None:
                if root.left is None and root.right is None:
                    root = None
                else:
                    if root.left is not None:
                        root = root.left
                    else:
                        root = root.right
            else:
                root.value = BinTree.__get_min_value_node(root.right).value
                root.right = BinTree.__delete_in_binary_tree(root.right, root.value, func)

        return root

    @staticmethod
    def __delete_without_function(root, value):
        if root is None:
            return None

        root.left = BinTree.__delete_without_function(root.left, value)
        root.right = BinTree.__delete_without_function(root.right, value)
        if root.value == value:
            if root.left is None or root.right is None:
                if root.left is None and root.right is None:
                    root = None
                else:
                    if root.left is not None:
                        root = root.left
                    else:
                        root = root.right
            else:
                root.value = BinTree.__get_min_value_node(root.right).value
                root.right = BinTree.__delete_without_function(root.right, root.value)

        return root

    def delete(self, value, func=None):
        if func is not None:
            if self.__isOrder:
                self.__root = BinTree.__delete_in_avl_tree(self.__root, value, func)
            else:
                self.__root = BinTree.__delete_in_binary_tree(self.__root, value, func)
        else:
            self.__root = BinTree.__delete_without_function(self.__root, value)
        self.__len -= 1

    def get_root(self):
        return self.__root

    def get_is_order(self):
        return self.__isOrder

    def __len__(self):
        return self.__len


def comp(n1, n2):
    if n1 < n2:
        return -1
    elif n1 == n2:
        return 0
    else:
        return 1


if __name__ == '__main__':
    tree = BinTree()
    tree2 = BinTree()

    for i in range(0, 8):
        tree.insert(i)
        tree2.insert(i, comp)

    for i in tree2.get_root():
        print(i.value, end=' ')

    print()

    print(tree2.search(3, comp).value)
    print(tree.search(5, comp).value)

    tree2.delete(3, comp)
    tree.delete(1, comp)
