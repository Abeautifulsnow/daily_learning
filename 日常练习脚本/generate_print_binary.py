"""
An Interesting Method to Generate Binary Numbers from 1 to n.
"""
import time
import sys
from queue import Queue


def generate_print_binary(n):
    q = Queue()
    # enqueue the first binary number.
    q.put("1")
    # This loop is like BFS of a tree with 1 as root 
    # 0 as left child and 1 as right child and so on 
    while n > 0:
        n -= 1
        # print the front of queue.
        s1 = q.get()
        print(s1)

        # store s1 before changing it.
        s2 = s1
        # append "0" to s1 and enqueue it
        q.put(s1 + "0")

        # append "1" to s2 and enqueue it. Not that s2
        # contains the previous front.
        q.put(s2 + "1")


if __name__ == "__main__":
    start = time.monotonic()
    input_num = sys.argv[1]
    n = int(input_num)
    generate_print_binary(n)
    print("# Total time cost: {0} s.".format(time.monotonic() - start))
