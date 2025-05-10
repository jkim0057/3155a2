from typing import List

class Node:
    def __init__(self, suffix_start_index=None) -> None:
        self.edges = [None] * 128
        self.link = None
        self.suffix_start_index = suffix_start_index

class Edge:
    def __init__(self, target: Node, start:int, end) -> None:
        self.start = start
        self.end = end
        self.target = target

class Ukkonen:
    def __init__(self, text:str) -> None:
        self.text = text
        self.suffix_tree = self.generate_suffix_tree(text)

    def print_tree(self):
        def _print(node, indent=''):
            for i in range(128):
                edge = node.edges[i]
                if edge:
                    start = edge.start
                    end = edge.end[0] if isinstance(edge.end, list) else edge.end
                    label = self.text[start:end + 1]
                    print(f"{indent}|-- {repr(label)}")
                    _print(edge.target, indent + '    ')
        print("Suffix Tree:")
        _print(self.suffix_tree)
        print('-' * 40)

    def is_terminal_edge(self, edge:Edge) -> bool:
        return edge.target.suffix_start_index is not None
    
    def get_length(self, edge:Edge) -> int:
        len = 0
        if self.is_terminal_edge(edge):
            len = edge.end[0] - edge.start + 1
        else:
            len = edge.end - edge.start + 1
        return len
    
    def split_edge(self, active_node:Node, active_edge:Edge, active_len:int, i:int, j:int, global_end:List[int]):
        leaf = Node(suffix_start_index=j)
        internal_node = Node()
        rear_edge = Edge(internal_node, active_edge.start, active_edge.start + active_len - 1)
        active_node.edges[ord(self.text[rear_edge.start])] = rear_edge
        internal_node.edges[ord(self.text[i])] = Edge(leaf, i, global_end)
        active_edge.start += active_len
        internal_node.edges[ord(self.text[active_edge.start])] = active_edge

        return internal_node
    
    def generate_suffix_tree(self, text:str) -> Node:
        n = len(text)

        global_end = [0]
        root = Node()
        active_node = root
        active_edge = None
        active_len = 0
        prev_internal_node = None
        self.suffix_tree = root
        
        j = 0
        for i in range(n):
            global_end[0] = i

            while i - j + 1 > 0:
                if active_len == 0:
                    active_edge = active_node.edges[ord(text[i])]
                    if active_edge is None:
                        leaf = Node(suffix_start_index=j)
                        active_node.edges[ord(text[i])] = Edge(leaf, i, global_end)
                        prev_internal_node = None
                        j += 1
                        continue
                
                # A character from the current node is found
                if active_edge:
                    # Skip count trick (traverse down the edge)
                    edge_len = self.get_length(active_edge)

                    new_leaf_created = False
                    while active_len >= edge_len:
                        active_node = active_edge.target
                        active_len -= edge_len
                        active_edge = active_node.edges[ord(text[i - active_len])]
                        # Case 1: no character found after a node
                        if active_edge is None:
                            leaf = Node(suffix_start_index=j)
                            active_node.edges[ord(text[i])] = Edge(leaf, i, global_end)
                            prev_internal_node = None
                            j += 1
                            new_leaf_created = True
                            break
                        # Case 2: exact node found with no remainder - set active_node only
                        if active_len == 0:
                            active_edge = active_node.edges[ord(text[i])]
                            break
                        edge_len = self.get_length(active_edge)

                    if new_leaf_created:
                        continue

                    # Rule 3: character found after traversal
                    if active_edge is not None and text[i] == text[active_edge.start + active_len]:
                        active_len += 1
                        prev_internal_node = None
                        break

                    # Perform edge split 
                    internal_node = self.split_edge(active_node, active_edge, active_len, i, j, global_end)
                    # Resolve links
                    if prev_internal_node:
                        prev_internal_node.link = internal_node
                    prev_internal_node = internal_node

                # At internal node and link found - jump using link
                if active_node != root and active_node.link is not None:
                    active_node = active_node.link
                # At internal node and link not found - go back to root
                elif active_node != root and active_node.link is None:
                    active_node = root
                # Still at root and active_len still remains - decrement active_len
                elif active_node == root and active_len > 0:
                    active_len -= 1

                # Active length all consumed
                if active_len == 0:
                    active_edge = None
                # Still has active length to remove - set active edge
                else:
                    active_edge = active_node.edges[ord(text[i - active_len])]
                
                j += 1
        return root

if __name__ == '__main__':
    ukk = Ukkonen("aabbbabbabbabbbaabba$")
    ukk.print_tree()