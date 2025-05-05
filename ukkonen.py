from typing import List

class Node:
    def __init__(self, suffix_start_index=None) -> None:
        self.edges = []
        self.link = None
        self.suffix_start_index = suffix_start_index

class Edge:
    def __init__(self, target: Node, start:int, end:List[int]) -> None:
        self.start = start
        self.end = end
        self.target = target