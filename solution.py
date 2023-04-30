"""
CSE331 Project 6 SS'23
Circular Double-Ended Queue
solution.py
"""

from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
# from matplotlib import pyplot as plt  # COMMENT OUT THIS LINE (and `plot_speed`) if you dont want matplotlib
import gc

T = TypeVar('T')


class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            data = ['Start']  # front will get set to 0 by a front enqueue if the initial data is empty
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = (self.size + front - 1) % self.capacity if data else None
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[(index + front) % capacity] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = ["CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    #
    # Your code goes here!
    #
    def __len__(self) -> int:
        """
        Returns the number of elements in the que
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Returns True if the que is empty, False otherwise
        """
        return self.size == False;


    def front_element(self) -> T:
        """
        Returns the element at the front of the que otherwise None if it is empty
        """
        if self.is_empty():
            return None
        else:
            return self.queue[self.front]

    def back_element(self) -> T:
        """
        Returns the element at the back of the que otherwise None if it is empty
        """
        if self.is_empty():
            return None
        else:
            return self.queue[self.back]

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        This function adds an element to the front or back of the que
        If front is True, the element is added to the front of the que
        If front is False, the element is added to to the back
        """
        if self.size == self.capacity - 1:
            self.grow()

        if self.is_empty():
            self.front = self.back = 0
        else:
            if front:
                self.front = (self.front - 1 + self.capacity) % self.capacity
            else:
                self.back = (self.back + 1) % self.capacity
        if front:
            self.queue[self.front] = value
        else:
            self.queue[self.back] = value
        self.size += 1

    def dequeue(self, front: bool = True) -> T:
        """
        Deque deletes an element from the front or back of the que
        If front is True, remove and return an element from the front of the que
        If front is False, remove and return an element from the back of the que
        Returns None if the que is empty
        """
        if self.is_empty():
            return None

        if front:
            index = self.front
        else:
            index = self.back
        deleted = self.queue[index]
        self.front = (self.front + 1) % self.capacity if front else self.front
        self.back = (self.back - 1) % self.capacity if not front else self.back
        self.size -= 1

        # Check if we need to shrink the deque
        if self.size <= self.capacity // 4 and self.capacity // 2 >= 4:
            self.shrink()

        return deleted

    def grow(self) -> None:
        """
        Doubles the capacity of the que
        """
        new_capacity = self.capacity * 2
        new_queue = [None] * new_capacity

        # Copy over elements to the new queue
        for i in range(self.size):
            new_queue[i] = self.queue[(self.back - self.size + 1 + i) % self.capacity]

        # Update front and back pointers
        self.front = 0
        self.back = self.size - 1
        self.capacity = new_capacity
        self.queue = new_queue

    def shrink(self) -> None:
        """
        cuts the capacity of the que in half
        """
        new_capacity = self.capacity // 2
        new_queue = [None] * new_capacity

        # Copy over elements to the new queue
        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % self.capacity]

        # Update front and back pointers
        self.front = 0
        self.back = self.size - 1
        self.capacity = new_capacity
        self.queue = new_queue

def get_winning_numbers(numbers: List[int], size: int) -> List[int]:
    """
    Returns a list of winning numbers of size based on the given input numbers list
    """
    result = []
    max = []

    for i in range(len(numbers)):

        while max and max[0] < i - size + 1:
            max.pop(0)
        while max and numbers[max[-1]] <= numbers[i]:
            max.pop()
        max.append(i)
        if i >= size - 1:
            result.append(numbers[max[0]])

    return result

def get_winning_probability(winning_numbers: List[int]) -> int:
    """
    Returns the maximum possible winning probability based on the input 'winning_numbers' list
    Returns False if the list is empty
    """
    if not winning_numbers:
        return False

    max_sum = winning_numbers[0]
    prev_max = 0

    for i in range(1, len(winning_numbers)):
        temp = max(max_sum, prev_max + winning_numbers[i])
        prev_max = max_sum
        max_sum = temp

    return max_sum
