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

class Ukkonen:
    def __init__(self, text:str) -> None:
        self.text = text
        self.suffix_tree = self.generate_suffix_tree(text)

    def generate_suffix_tree(self, text:str) -> Node:
        n = len(text)

        global_end = [0]
        root = Node()
        active_node = root
        active_edge = None
        active_len = 0
        prev_internal_node = None

        # Rule 1: expand leaf
        # Rule 2: branch
        # Rule 3: exists (create internal node)
        
        j = 0
        for i in range(n):
            global_end[0] = i

            child_edge = active_node.edges[ord(text[j])]
            
            # Rule 3: no leaf found, create leaf
            if child_edge is None:
                leaf = Node(suffix_start_index=j)
                active_node.edges[ord(text[j])] = Edge(start=i, end=global_end, target=leaf)
                
                j += 1
    
        return root