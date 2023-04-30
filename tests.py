"""
CSE331 Project 6 SS'23
Circular Double-Ended Queue
tests.py
"""

import random
import unittest
from solution import CircularDeque, get_winning_numbers, get_winning_probability
from xml.dom import minidom

random.seed(1342)

NAMES = ['Aaron', 'Abhinay', 'Adam', 'David', 'Gabriel', 'Jackson', 'Joseph', 'Joshua',
         'Khushi', 'Krish', 'Lauren', 'Lukas', 'Matt', 'Misha', 'Nate', 'Roshanak', 'Sai', 'Bank']


class CircularDequeTests(unittest.TestCase):
    def test_len(self):
        # Test 1 : length 0
        cd = CircularDeque()
        self.assertEqual(0, len(cd))

        # Test 2 : length 1
        cd = CircularDeque([1])
        self.assertEqual(1, len(cd))

        # Test 3 : length 2
        cd = CircularDeque([1, 2])
        self.assertEqual(2, len(cd))

        # Test 4 : length 50
        cd = CircularDeque(list(range(50)), capacity=50)
        self.assertEqual(50, len(cd))

    def test_is_empty(self):
        # Test 1 : Empty deque -> true
        cd = CircularDeque()
        self.assertTrue(cd.is_empty())

        # Test 2 : length 1 -> false
        cd = CircularDeque([1])
        self.assertFalse(cd.is_empty())

        # Test 3 : length 2 -> false
        cd = CircularDeque([1, 2])
        self.assertFalse(cd.is_empty())

        # Test 4 : length 50 -> false
        cd = CircularDeque(list(range(50)), capacity=50)
        self.assertFalse(cd.is_empty())

    def test_front_element(self):
        # Test 1: Empty deque -> None
        cd = CircularDeque()
        self.assertIsNone(cd.front_element())

        # Test 2: CD <1> -> 1
        cd = CircularDeque([1])
        self.assertEqual(1, cd.front_element())

        # Test 3: CD <2, 1> -> 2
        cd = CircularDeque([2, 1])
        self.assertEqual(2, cd.front_element())

        # Test 4: CD <50, 49, ..., 0> -> 50
        cd = CircularDeque(list(range(50, 0, -1)), capacity=50)
        self.assertEqual(50, cd.front_element())

    def test_back_element(self):
        # Test 1: Empty Deque -> None
        cd = CircularDeque()
        self.assertIsNone(cd.back_element())

        # Test 2: CD <1> -> 1
        cd = CircularDeque([1])
        self.assertEqual(1, cd.back_element())

        # Test 3: CD <1, 2> -> 2
        cd = CircularDeque([1, 2])
        self.assertEqual(2, cd.back_element())

        # Test 4: CD <50, 49, ..., 0> -> 0
        cd = CircularDeque(list(range(50, 0, -1)), capacity=50)
        self.assertEqual(1, cd.back_element())

    def test_grow(self):
        """
        Tests grow functionality without use of enqueue
        Note that we call the grow function directly
        thus if you have a capacity check in your grow function this will fail
        """
        # Test (1) Empty Dequeue
        cd = CircularDeque()
        cd.grow()
        self.assertEqual(0, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual([None] * 8, cd.queue)

        # Test (2) Four element dequeue then grow
        cd = CircularDeque(NAMES[:4])
        cd.grow()
        self.assertEqual(4, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(NAMES[:4] + [None] * 4, cd.queue)

    def test_grow_additional(self):
        """
        Additional test function for grow without use of enqueue
        Note that we call the grow function directly
        thus if you have a capacity check in your grow function this will fail
        """
        # Test (1) Reset front and back of wrap-around
        cd = CircularDeque(NAMES[:4])
        cd.front = 2
        cd.back = 1
        cd.grow()
        self.assertEqual(4, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(["Adam", "David", "Aaron", "Abhinay"] + [None] * 4, cd.queue)

        # Test (2) Reset front and back of wrap-around
        cd = CircularDeque(NAMES[:8], capacity=8)
        cd.front = 1
        cd.back = 0
        cd.grow()
        self.assertEqual(8, cd.size)
        self.assertEqual(16, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(7, cd.back)
        self.assertEqual(['Abhinay', 'Adam', 'David', 'Gabriel', 'Jackson', 'Joseph', 'Joshua', 'Aaron'] + [None] * 8, cd.queue)

        # Test (3) Reset front and back of wrap-around
        cd = CircularDeque(NAMES[5:8] + NAMES[:5], capacity=8)
        cd.front = 3
        cd.back = 2
        cd.grow()
        self.assertEqual(8, cd.size)
        self.assertEqual(16, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(7, cd.back)
        self.assertEqual(NAMES[:8] + [None] * 8, cd.queue)

    def test_shrink(self):
        """
        Tests shrink without the use of dequeue
        NOTE: If you have a capacity/size check in your shrink this will fail since we call shrink directly
        """

        # Test 1, Capacity 8 -> 4
        cd = CircularDeque(NAMES[:4], capacity=8)
        cd.shrink()
        self.assertEqual(4, cd.capacity)
        self.assertEqual(4, cd.size)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(NAMES[:4], cd.queue)

        # Test 2, Capacity 16 -> 8
        cd = CircularDeque(NAMES[:8], capacity=16)
        cd.shrink()
        self.assertEqual(8, cd.capacity)
        self.assertEqual(8, cd.size)
        self.assertEqual(0, cd.front)
        self.assertEqual(7, cd.back)
        self.assertEqual(NAMES[:8], cd.queue)

    def test_shrink_additional(self):
        """
        Test additional for shrink without using dequeue
        NOTE: If you have a capacity/size check in your shrink this will fail since we call shrink directly
        """
        # Test 1, Capacity 8 -> 4 with wrap-around index
        cd = CircularDeque(NAMES[2:4] + [None] * 4 + NAMES[:2], capacity=8)
        cd.front = 6
        cd.back = 1
        cd.size = 4
        cd.shrink()
        self.assertEqual(4, cd.capacity)
        self.assertEqual(4, cd.size)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(NAMES[:4], cd.queue)

        # Test 2, Capacity 16 -> 8 with wrap-around index
        cd = CircularDeque(NAMES[7:8] + [None] * 8 + NAMES[:7], capacity=16)
        cd.front = 9
        cd.back = 1
        cd.size = 8
        cd.shrink()
        self.assertEqual(8, cd.capacity)
        self.assertEqual(8, cd.size)
        self.assertEqual(0, cd.front)
        self.assertEqual(7, cd.back)
        self.assertEqual(NAMES[:8], cd.queue)

    def test_front_enqueue_basic(self):
        """
        Tests front enqueue but does not test grow functionality
        """

        # Test 1: One element
        cd = CircularDeque()
        cd.enqueue('First')
        self.assertEqual(0, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(1, cd.size)
        self.assertEqual(['First', None, None, None], cd.queue)

        # Test 2: Wraparound two elements
        cd.enqueue('Second')
        self.assertEqual(3, cd.front)  # Test 2
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(2, cd.size)
        self.assertEqual(['First', None, None, 'Second'], cd.queue)

        # Set deque capacity to 100, use name list which has length 14 thus we'll
        # never grow with unique insertion because math

        # Test 3: Front enqueue no wrap-around
        cd = CircularDeque(front=50, capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name)
            self.assertEqual(name, cd.front_element())
            self.assertEqual(49 - i, cd.front)
            self.assertEqual('Start', cd.back_element())  # back_element should never change
            self.assertEqual(50, cd.back)
            self.assertEqual(i + 2, len(cd))
            self.assertEqual(100, cd.capacity)

        # Test 4: Front enqueue wrap-around
        cd = CircularDeque(capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name)
            self.assertEqual(name, cd.front_element())
            self.assertEqual((100 - i) % 100, cd.front)
            self.assertEqual('Aaron', cd.back_element())  # back_element should never change
            self.assertEqual(0, cd.back)
            self.assertEqual(i + 1, len(cd))
            self.assertEqual(100, cd.capacity)

    def test_back_enqueue_basic(self):
        """
        Tests back enqueue but does not test grow functionality
        """

        # Test 1: One element
        cd = CircularDeque()
        cd.enqueue('First', front=False)
        self.assertEqual(0, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(1, cd.size)
        self.assertEqual(['First', None, None, None], cd.queue)

        # Test 2: Wraparound two elements
        cd = CircularDeque(data=['First'], front=3)
        cd.enqueue('Second', front=False)
        self.assertEqual(3, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(2, cd.size)
        self.assertEqual(['Second', None, None, 'First'], cd.queue)

        # Test 3: Back enqueue normal (no wrap around) more elements
        cd = CircularDeque(capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name, front=False)
            self.assertEqual(name, cd.back_element())
            self.assertEqual(i, cd.back)
            self.assertEqual('Aaron', cd.front_element())  # back_element should never change
            self.assertEqual(0, cd.front)
            self.assertEqual(i + 1, len(cd))
            self.assertEqual(100, cd.capacity)

        # Test 4: Back enqueue wraparound (back < front) more elements
        cd = CircularDeque(front=99, capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name, front=False)
            self.assertEqual(name, cd.back_element())
            self.assertEqual((100 + i) % 100, cd.back)
            self.assertEqual('Start', cd.front_element())  # front_element should never change
            self.assertEqual(99, cd.front)
            self.assertEqual(i + 2, len(cd))
            self.assertEqual(100, cd.capacity)

    def test_front_enqueue(self):
        """
        Tests front_enqueue and grow functionality
        """
        # Test 1: Front_enqueue, multiple grows with 50 elements starting with default capacity
        cd = CircularDeque()
        for element in range(1, 51):
            cd.enqueue(element)
            # Test capacity of the dequeue while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            else:
                self.assertEqual(64, cd.capacity)
        # check the position of elements in the dequeue
        self.assertEqual(list(range(32, 0, -1)) + [None] * 14 + list(range(50, 32, -1)), cd.queue)
        self.assertEqual(50, cd.size)

        # Test 2: Front_enqueue, multiple grows with 64 elements starting with default capacity
        cd = CircularDeque()
        for element in range(1, 65):
            cd.enqueue(element)
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            elif element < 64:
                self.assertEqual(64, cd.capacity)
        # check the position of elements in the cd
        self.assertEqual(list(range(64, 0, -1)) + [None] * 64, cd.queue)
        self.assertEqual(64, cd.size)
        self.assertEqual(128, cd.capacity)

    def test_back_enqueue(self):
        """
        Tests back_enqueue and grow functionality
        """
        # Test 1: 50 item, multiple grows
        cd = CircularDeque()
        for element in range(1, 51):
            cd.enqueue(element, front=False)
            # Test capacity of the cd while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            else:
                self.assertEqual(64, cd.capacity)
        self.assertEqual(list(range(1, 51)) + [None] * 14, cd.queue)
        self.assertEqual(64, cd.capacity)
        self.assertEqual(50, cd.size)

        # Test 2: 64 items, multiple grows
        cd = CircularDeque()
        for element in range(1, 65):
            cd.enqueue(element, front=False)
            # Test capacity of the cd while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            elif element < 64:
                self.assertEqual(64, cd.capacity)
        self.assertEqual(list(range(1, 65)) + [None] * 64, cd.queue)
        self.assertEqual(128, cd.capacity)
        self.assertEqual(64, cd.size)

    def test_front_dequeue_basic(self):
        """
        Testing front/back dequeue without shrinking
        Does not use either enqueue function
        """
        # Test 0: empty deque
        cd = CircularDeque()
        self.assertIsNone(cd.dequeue())

        # Test 1: 1 element front dequeue
        cd = CircularDeque([1])
        self.assertEqual(1, cd.dequeue())
        self.assertEqual(0, len(cd))

        # Test 2: Multiple element front dequeue
        cd = CircularDeque([0, 1, 2])
        for i in range(3):
            self.assertEqual(i, cd.front)
            self.assertEqual(i, cd.dequeue())
            self.assertEqual(2 - i, len(cd))

        # Test 3: front Dequeue wrap-around
        dequeue_result = [3, 0, 1, 2]
        cd = CircularDeque([0, 1, 2, 3])
        cd.front = 3
        cd.back = 2
        for i in range(4):
            self.assertEqual(dequeue_result[i], cd.front)
            self.assertEqual(dequeue_result[i], cd.dequeue())
            self.assertEqual(3 - i, len(cd))
        self.assertIsNone(cd.dequeue())

    def test_back_dequeue_basic(self):
        """
        Testing front/back dequeue without shrinking
        Does not use either enqueue function
        """
        # Test 0: empty deque
        cd = CircularDeque()
        self.assertIsNone(cd.dequeue(False))

        # Test 1: 1 element front dequeue
        cd = CircularDeque([1])
        self.assertEqual(1, cd.dequeue(False))
        self.assertEqual(0, len(cd))

        # Test 2: Multiple element front dequeue
        cd = CircularDeque([3, 2, 1, 0])
        for i in range(4):
            self.assertEqual(3 - i, cd.back)
            self.assertEqual(i, cd.dequeue(False))
            self.assertEqual(3 - i, len(cd))

        # Test 3: front Dequeue wrap-around
        dequeue_result = [0, 3, 2, 1]
        cd = CircularDeque([0, 1, 2, 3])
        cd.front = 1
        cd.back = 0
        for i in range(4):
            self.assertEqual(dequeue_result[i], cd.back)
            self.assertEqual(dequeue_result[i], cd.dequeue(False))
            self.assertEqual(3 - i, len(cd))
        self.assertIsNone(cd.dequeue(False))

    def test_back_dequeue(self):
        """
        Tests dequeue over shrinking conditions, does test size (length)
        Does not rely on enqueue functions
        """
        # Test 1: Begin with capacity 16, empty queue while checking all parameters
        cd = CircularDeque([i for i in range(15)], capacity=16)

        for item in range(15):
            self.assertEqual(14 - item, cd.dequeue(False))

            if item <= 9:  # shrunk 0 times
                self.assertEqual(list(range(15)) + [None], cd.queue)
                self.assertEqual(16, cd.capacity)
            elif item <= 11:  # shrunk 1 time
                self.assertEqual(list(range(4)) + [None, None, None, None], cd.queue)
                self.assertEqual(8, cd.capacity)
            else:  # shrunk twice
                self.assertEqual([0, 1, None, None], cd.queue)
                self.assertEqual(4, cd.capacity)

            # ensure back is set correctly - note: pointers for an empty queue are up to implementation
            if cd.size != 0:
                self.assertEqual(13 - item, cd.back)

    def test_front_dequeue(self):
        """
        Tests dequeue along with shrinking
        Does not rely on enqueue functions
        """
        # Test 1: identical to above but removing from front rather than back
        cd = CircularDeque([i for i in range(15)], capacity=16)

        fronts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 1, 0, 1]

        for item in range(15):
            self.assertEqual(item, cd.dequeue())

            if item <= 9:
                self.assertEqual(list(range(15)) + [None], cd.queue)
                self.assertEqual(16, cd.capacity)
            elif item <= 11:
                self.assertEqual([11, 12, 13, 14, None, None, None, None], cd.queue)
                self.assertEqual(8, cd.capacity)
            else:
                self.assertEqual([13, 14, None, None], cd.queue)

            if cd.size != 0:
                self.assertEqual(fronts[item], cd.front)

    def test_winning_numbers(self):
        """
        Tests the get_winning_numbers function
        """
        # Test empty
        numbers = []
        size = 3
        expected = []
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test one number
        numbers = [1]
        size = 1
        expected = [1]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test simple
        numbers = [1, 2]
        size = 1
        expected = [1, 2]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test simple
        numbers = [1, 2]
        size = 2
        expected = [2]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test 1
        numbers = [1, 3, -1, -3, 5, 3, 6, 7]
        size = 3
        expected = [3, 3, 5, 5, 6, 7]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test 2
        numbers = [5, 7, 2, 4, -10, -2, 3, 22, 30, 102, -13, 20]
        size = 4
        expected = [7, 7, 4, 4, 22, 30, 102, 102, 102]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test 3
        numbers = [2, 3, 9, 2, 8, 10, 3, 1, 0, 8]
        size = 2
        expected = [3, 9, 9, 8, 10, 10, 3, 1, 8]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test 4
        numbers = [-2, -3, -9, -2, -8, -10, -3, -1, -4, -8]
        size = 2
        expected = [-2, -3, -2, -2, -8, -3, -1, -1, -4]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test 5
        numbers = [10000, 1000000, 100000, -10000, -1000000, -1000000, 1000, -1000, 10000]
        size = 4
        expected = [1000000, 1000000, 100000, 1000, 1000, 10000]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

        # Test 6
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        size = 1
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        output = get_winning_numbers(numbers, size)
        self.assertEqual(expected, output)

    def test_winning_probability(self):
        """
        Tests the get_winning_probability function
        """
        # Test empty
        winning_numbers = []
        expected = 0
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test one element
        winning_numbers = [8]
        expected = 8
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test two elements
        winning_numbers = [5, 10]
        expected = 10
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test 1
        winning_numbers = [1, 3, 5, 2, 7]
        expected = 13
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test 2
        winning_numbers = [1, 2, 3, 1]
        expected = 4
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test 3
        winning_numbers = [2, 7, 9, 3, 1]
        expected = 12
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test 4
        winning_numbers = [7, 9, 2, 5, 3]
        expected = 14
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test with Winning Numbers from previous function 1
        winning_numbers = [3, 3, 5, 5, 6, 7]
        expected = 15
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test with Winning Numbers from previous function 2
        winning_numbers = [7, 7, 4, 4, 22, 30, 102, 102, 102]
        expected = 237
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test with Winning Numbers from previous function 3
        winning_numbers = [3, 9, 9, 8, 10, 10, 3, 1, 8]
        expected = 35
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test with Winning Numbers from previous function 4
        winning_numbers = [1000000, 1000000, 100000, 1000, 1000, 10000]
        expected = 1110000
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)

        # Test with Winning Numbers from previous function 5
        winning_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        expected = 110
        output = get_winning_probability(winning_numbers)
        self.assertEqual(expected, output)


if __name__ == '__main__':
    unittest.main()
