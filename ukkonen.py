from typing import List
 
class Node:
    def __init__(self, suffix_start_index=None) -> None:
        self.edges = [None] * 128
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
            self.print_tree()
            # Rule 1: expand leaf
            global_end[0] = i

            while i - j + 1 > 0: # TODO: not sure yet
                child_edge = active_node.edges[ord(text[j])]
                
                # Rule 2: no leaf found, create leaf
                if child_edge is None:
                    leaf = Node(suffix_start_index=j)
                    active_node.edges[ord(text[j])] = Edge(start=i, end=global_end, target=leaf)
                    prev_internal_node = None
                    j += 1
                    break

                else:
                    # Condition 1: no active edge yet - set the active edge
                    if active_edge is None:
                        active_edge = child_edge
                        active_len += 1
                        prev_internal_node = None
                        break
                    # Condition 2: matching characters have gone beyond the active edge
                    elif active_edge.target.suffix_start_index is None and (active_len == active_edge.end - active_edge.start + 1):
                        if active_edge.target.edges[ord(text[i])]:
                            active_node = active_edge.target
                            active_edge = active_edge.target.edges[ord(text[i])]
                            active_len = 1
                            prev_internal_node = None
                            break # TODO: need to think here
                        else:
                            leaf = Node(suffix_start_index=j)
                            active_edge.target.edges[ord(text[j])] = Edge(start=i, end=global_end, target=leaf)
                            active_len -= 1
                            j += 1
                            if active_node.link:
                                active_node = active_node.link
                            
                    # Condition 3: one more character matched within the same active edge
                    elif text[i] == text[active_edge.start + active_len]:
                        active_len += 1
                        prev_internal_node = None
                    elif text[i] != text[active_edge.start + active_len]:
                        # Rule 2 extension: Perform edge split and jump using link
                        leaf = Node(suffix_start_index=j)
                        rear_edge = Edge(target=active_edge.target, start=active_edge.start + active_len, end=active_edge.end)
                        active_edge.end = active_edge.start + active_len - 1
                        
                        internal_node = Node()
                        active_edge.target = internal_node
                        internal_node.edges[ord(text[active_edge.start + active_len])] = rear_edge
                        internal_node.edges[ord(text[i])] = Edge(target=leaf, start=i, end=global_end)
                        
                        # Internal node created: create link
                        if prev_internal_node:
                            prev_internal_node.link = internal_node
                        else:
                             internal_node.link = root
                        prev_internal_node = internal_node
                        active_edge = None

                        if active_node.link:
                            active_node = active_node.link
                            j += 1
                            active_len = 0
                        else:
                            j += 1
                            active_len -= 1
                            continue  
        return root
    
if __name__ == '__main__':
    ukk = Ukkonen("aabcabc$")