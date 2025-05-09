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
        if self.isTerminalEdge(edge):
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
            self.print_tree()

            while i - j + 1 > 0:
                self.print_tree()
                active_edge = active_node.edges[ord(text[i])]
                if active_len == 0:
                    if active_edge is None:
                        leaf = Node(suffix_start_index=j)
                        active_node.edges[ord(text[i])] = Edge(leaf, i, global_end)
                        prev_internal_node = None
                        j += 1
                        break # TODO: experiment needed (continue?)
                
                # A character from the current node is found
                if active_edge:
                    # Skip count trick (traverse down the edge)
                    edge_len = self.getLength(active_edge)
                    while active_len >= edge_len:
                        active_node = active_edge.target
                        active_len -= edge_len
                        active_edge = active_node.edges[ord(text[j])]
                        # Case 1: no character found after a node
                        if active_edge is None:
                            leaf = Node(suffix_start_index=j)
                            active_node.edges[ord(text[i])] = Edge(leaf, i, global_end)
                            prev_internal_node = None
                            j += 1
                            break
                        # Case 2: exact node found with no remainder - set active_node only
                        if active_len == 0:
                            active_edge = active_node.edges[ord(text[i])]
                            break

                    # Make other extensions
                    # Perform edge split 
                    internal_node = self.split_edge(active_node, active_edge, active_len, i, j, global_end)
                    # Resolve links
                    if prev_internal_node:
                        prev_internal_node.link = internal_node
                    prev_internal_node = internal_node

                    # Showstopper?
                
                else:
                    pass
                
                # Keep this condition (correct for sure)
                j += 1
        return root

if __name__ == '__main__':
    ukk = Ukkonen("aabcaba$")
    ukk.print_tree()

                # # Rule 3: no leaf found, create leaf
                # if child_edge is None:
                #     leaf = Node(suffix_start_index=j)
                #     active_node.edges[ord(text[j])] = Edge(start=i, end=global_end, target=leaf)
                #     prev_internal_node = None
                #     j += 1
                #     break

                # else:
                #     # Condition 1: no active edge yet - set the active edge
                #     if active_edge is None:
                #         active_edge = child_edge
                #         active_len = 1
                #         prev_internal_node = None
                #         break
                #         # if i - j > 0:
                #         #     continue
                #         # else:
                #         #     break
                #     # Condition 2: matching characters have gone beyond the active edge
                #     elif active_edge.target.suffix_start_index is None and (active_len == active_edge.end - active_edge.start + 1):
                #         if active_edge.target.edges[ord(text[i])]:
                #             active_node = active_edge.target
                #             active_edge = active_edge.target.edges[ord(text[i])]
                #             active_len = 1
                #             prev_internal_node = None
                #             break # TODO: need to think here
                #         else:
                #             leaf = Node(suffix_start_index=j)
                #             active_edge.target.edges[ord(text[i])] = Edge(start=i, end=global_end, target=leaf)
                #             active_len -= 1
                #             j += 1
                #             if active_node.link:
                #                 active_node = active_node.link
                #             active_edge = None
                #             prev_internal_node = None
                #     # Condition 4: one more character matched within the same active edge
                #     elif text[i] == text[active_edge.start + active_len]:
                #         if active_len > 0:
                #             active_len += 1
                #             prev_internal_node = None
                #             break
                #         else:
                #             active_node = active_edge.target
                #             break
                #     elif text[i] != text[active_edge.start + active_len]:
                #         # Rule 2 extension: Perform edge split and jump using link
                #         leaf = Node(suffix_start_index=j)
                #         rear_edge = Edge(target=active_edge.target, start=active_edge.start + active_len, end=active_edge.end)
                #         active_edge.end = active_edge.start + active_len - 1
                        
                #         internal_node = Node()
                #         active_edge.target = internal_node
                #         internal_node.edges[ord(text[active_edge.start + active_len])] = rear_edge
                #         internal_node.edges[ord(text[i])] = Edge(target=leaf, start=i, end=global_end)
                        
                #         # Internal node created: create link
                #         if prev_internal_node:
                #             prev_internal_node.link = internal_node
                #         internal_node.link = root
                #         prev_internal_node = internal_node
                #         active_edge = None

                #         if active_node.link:
                #             active_node = active_node.link
                #         else:
                #             active_len -= 1
                #             active_node = root
                        
                #         j += 1
                #         if active_node == root:
                #             active_edge = active_node.edges[ord(text[j])]
                #         else:
                #             active_edge = active_node.edges[ord(text[i-active_len])]

                #         # Skip and count trick
                #         while active_edge and active_len > 0:
                #             edge_length = active_edge.end[0] - active_edge.start + 1 if active_edge.target.suffix_start_index else active_edge.end - active_edge.start + 1
                #             if active_len < edge_length:
                #                 # Case 1: edge length is greater, so the active edge must be this
                #                 break
                #             elif active_len == edge_length:
                #                 # Case 2: edge covered by active_len, update active node only
                #                 active_node = active_edge.target
                #                 active_len = 0
                #                 active_edge = None
                #                 break
                #             else:
                #                 # Case 3: target exists somewhere beyond the rear node
                #                 active_len -= edge_length
                #                 active_node = active_edge.target
                #                 if active_len > 0:
                #                     active_edge = active_node.edges[ord(text[j + active_edge.start + edge_length])]
                #                 else:
                #                     active_edge = None
                #         if active_edge and active_len == 0 and self.getLength(active_edge) == 1:
                #             active_edge = None