import copy
from collections import defaultdict

class VectorClock(object):
    def __init__(self, values):
        """Initialize a vector clock with a given set of values."""
        self.values = values

    def __repr__(self):
        return 'VectorClock(%r)' % self.values

    def __str__(self):
        return str(self.values)

    def increment(self, i):
        """Increment the vector clock for a specific processor.  Return a new result."""
        new_vals = copy.copy(self.values)
        new_vals[i] += 1
        return VectorClock(new_vals)

    def update(self, other):
        """Compute a new vector clock by computing an element-wise maximum."""
        new_vals = [max(a, b) for a, b in zip(self.values, other.values)]
        return VectorClock(new_vals)

class SmartStop(object):
    def __init__(self, n):
        def initial_vector_clock():
            return VectorClock([-1] * n)

        # Vector clock associated with each processor
        self.processor_clocks = [initial_vector_clock()] * n

        # Vector clock associated with each memory word
        self.word_clocks = defaultdict(initial_vector_clock)

    def add(self, pid, address, is_write):
        """Record a memory access."""
        vc = self.processor_clocks[pid]
        vc = vc.increment(pid)

        if address:
            if is_write:
                self.word_clocks[address] = vc
            else:
                vc = vc.update(self.word_clocks[address])

        self.processor_clocks[pid] = vc
        return vc

if __name__ == '__main__':
    ss = SmartStop(2)
    accesses = [(0, 'A', False), (0, 'A', True), (0, 'B', True), (0, 'A', False),
                (1, 'B', False), (1, 'A', False), (1, 'A', True), (1, None, False)]

    for pid, address, is_write in accesses:
        print '%s %s %s: %s' % (pid, address, is_write, ss.add(pid, address, is_write))
