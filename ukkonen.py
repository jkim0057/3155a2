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

            while True: # TODO: not sure (need to loop until i-j is 0?)
                child_edge = active_node.edges[ord(text[j])]
                
                # Rule 3: no leaf found, create leaf
                if child_edge is None:
                    leaf = Node(suffix_start_index=j)
                    active_node.edges[ord(text[j])] = Edge(start=i, end=global_end, target=leaf)
                    
                    j += 1
                # Rule 2: corresponding edge found
                else:
                    # Condition 1: no active edge yet - set the active edge
                    if active_edge is None:
                        active_edge = child_edge
                        active_len += 1
                    # Condition 2: matching characters have gone beyond the active edge
                    elif active_len == active_edge.end[0] - active_edge.start + 1:
                        if active_edge.target.edges[ord(text[i])]:
                            active_node = active_edge.target
                            active_edge = active_edge.target.edges[ord(text[i])]
                            active_len = 1
                        else:
                            leaf = Node(suffix_start_index=j)
                            active_edge.target.edges[ord(text[j])] = Edge(start=i, end=global_end, target=leaf)
                            active_len -= 1
                            j += 1
                            break
                    elif text[i] == text[active_edge.start + active_len]:
                        active_len += 1
                    elif text[i] != text[active_edge.start + active_len]:
                        # Rule 2 extension: Perform edge split and jump using link
                        leaf = Node(suffix_start_index=j)
                        active_edge.end = active_edge.start + active_len - 1
                        rear_edge = Edge(target=active_edge.target, start=active_edge.start + active_len, end=active_edge.end)
                        internal_node = Node()
                        active_edge.target = internal_node
                        internal_node.edges[ord(text[active_edge.start + active_len])] = rear_edge
                        internal_node.edges[i] = Edge(target=leaf, start=i, end=global_end)
                        
                        # Internal node created: create link
                        if prev_internal_node:
                            prev_internal_node.link = internal_node
                        else:
                            internal_node.link = root
                        prev_internal_node = internal_node

                        if active_node.link:
                            active_node = active_node.link
                        else:
                            j += 1
                            active_len -= 1
                            break
        return root