# Name: Daniel Kim
# Description: Class definition for HashMap with single chain implementation and function definition for find_mode

from a6_include import DynamicArray, LinkedList, hash_function_1, hash_function_2, SLNode


class HashMap:
    def __init__(self, capacity: int = 11, function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hash map or adds new key/value pair if pair does not exist in hash map

        Input: Key (string), Value (object)
        """
        load_factor = self.table_load()

        # Double capacity if load factor is greater or equal to 1
        if load_factor >= 1:
            self.resize_table(self._capacity * 2)

        # Calculate array index for input storage location
        index = self._hash_function(key) % self._capacity

        # Get the linked list at specified index in array
        linked_list = self._buckets.get_at_index(index)

        # Traverse through linked list and get the node with specified key
        node = linked_list.contains(key)

        # If node is none, key/value doesn't exist, insert new pair into list and increment size
        if node is None:
            linked_list.insert(key, value)
            self._size += 1

        # Key/value pair does exist, update value
        else:
            node.value = value

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in hash table

        Output: Number of empty buckets (int)
        """
        empty_bucket_count = 0

        # Iterate array and check length of linked list, increment counter if linked list length is zero
        for i in range(self._buckets.length()):
            linked_list = self._buckets[i]
            if linked_list.length() == 0:
                empty_bucket_count += 1

        return empty_bucket_count

    def table_load(self) -> float:
        """
        Returns hash table's current load factor

        Output: Load factor (float)
        """
        number_of_elements = self._size
        number_of_buckets = self._capacity
        return number_of_elements / number_of_buckets

    def clear(self) -> None:
        """
        Clears contents of hash map without changing table capacity
        """
        # Set each bucket to empty linked list
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()

        # Reset size to 0
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes hash map table based on new capacity input (must be greater than 1)

        Input: New capacity (int)
        """
        # Return if input is less than 1
        if new_capacity < 1:
            return

        # Check if input capacity is a prime number and adjust capacity
        if self._is_prime(new_capacity) is False:
            self._capacity = self._next_prime(new_capacity)
        else:
            self._capacity = new_capacity

        # Initialize copy of previous bucket and set buckets data member to new instance of DynamicArray
        old_bucket = self._buckets
        self._buckets = DynamicArray()

        # Reset size since the put method increments counter
        self._size = 0

        # Populate new bucket list with empty linked list
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        # Iterate through old bucket and populate new bucket's linked list nodes
        for i in range(old_bucket.length()):
            linked_list = old_bucket[i]
            for node in linked_list:
                self.put(node.key, node.value)

    def get(self, key: str):
        """
        Returns value associated with given key, None otherwise

        Input: Key (string)
        """
        # Get linked list at index based on input key and return node value if it exists
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        node = linked_list.contains(key)

        if node is not None:
            return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns true if given key is in hash map, False otherwise

        Input: Key (string)
        Output: Boolean
        """
        # Get linked list at index based on input key and return True if it exists
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        node = linked_list.contains(key)

        if node is not None:
            return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes given key and its associated value if it exists within hash map

        Input: Key (string)
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        node = linked_list.contains(key)

        # If node is not None, remove node and decrement size
        if node is not None:
            linked_list.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns dynamic array where each index contains a tuple of key/value pair in hash map

        Output: Array (DynamicArray)
        """
        return_array = DynamicArray()

        # Iterate bucket and for each linked list, if node is not None, append it's key/value to output array
        for index in range(self._capacity):
            linked_list = self._buckets[index]
            for node in linked_list:
                if node is not None:
                    return_array.append((node.key, node.value))

        return return_array

    def get_node(self, key: str) -> SLNode:
        """
        Returns linked list node associated with specified key, None otherwise

        Input: Key (string)
        Output: Node (SLNode)
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        node = linked_list.contains(key)

        return node


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Returns a tuple of a dynamic array with the mode value(s) and highest count

    Input: Array (DynamicArray)
    Output: Tuple (DynamicArray, int)
    """
    hash_map = HashMap(11, hash_function_1)
    mode_array = DynamicArray()
    max_count = 1

    # Populate hash map with key and count of key
    for i in range(da.length()):
        element = da[i]

        # Hash map doesn't contain element, insert into hash map
        if hash_map.contains_key(element) is False:
            hash_map.put(element, 1)
        # Hash map contains element, update count
        else:
            node = hash_map.get_node(element)
            node.value += 1
            # Update max count variable to track highest occuring frequency
            if node.value > max_count:
                max_count = node.value

    # Get array of tuples with key and key count
    key_and_count_array = hash_map.get_keys_and_values()

    # Populate return array with mode key
    for i in range(key_and_count_array.length()):
        key = key_and_count_array[i][0]
        key_count = key_and_count_array[i][1]

        # Append the key to output array if key count is equal to max count
        if key_count == max_count:
            mode_array.append(key)

    # No modes, return original array in tuple
    if mode_array.length() == 0:
        return da, max_count

    return mode_array, max_count


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
