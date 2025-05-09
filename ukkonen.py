class Node:
    def __init__(self, suffix_start_index=None) -> None:
        self.edges = [None] * 128
        self.link = None
        self.suffix_start_index = suffix_start_index

class Edge:
    def __init__(self, target: Node, start:int, end, length:int) -> None:
        self.start = start
        self.end = end
        self.target = target
        self.length = length

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
            prev_internal_node = None
            self.print_tree()

            while i - j + 1 > 0: # TODO: not sure yet
                self.print_tree()
                
                edge_length = 0
                while active_edge and active_len > 0:
                    edge_length = active_edge.end[0] - active_edge.start + 1 if active_edge.target.suffix_start_index else active_edge.end - active_edge.start + 1
                    
                    if active_len < edge_length:
                        # Case 1: extension point found! finish the traverse
                        break
                    if active_len == edge_length:
                        # Case 1: edge covered by active_len, update active node only
                        active_node = active_edge.target
                        active_len = 0
                        active_edge = None
                        break
                    else:
                        # Case 2: target exists somewhere beyond the rear node
                        active_len -= edge_length
                        active_node = active_edge.target
                        active_edge = active_node.edges[ord(text[j + active_edge.start + edge_length])]
                
                if active_edge:
                    pass
                else:
                    # Rule 3: no leaf found, create leaf
                    if active_node.edges[ord(text[i])] is None:
                        leaf = Node(suffix_start_index=j)
                        active_node.edges[ord(text[j])] = Edge(start=i, end=global_end, target=leaf, length=global_end[0]-i+1)
                        j += 1
                    
                

        return root

if __name__ == '__main__':
    ukk = Ukkonen("abaaabbbaabbbaaab$")
    ukk.print_tree()
    # print(ukk.suffix_tree.edges[ord('a')].target.edges)