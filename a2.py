from typing import List
import sys

class Node:
    def __init__(self, suffix_start_index=None, parent_start_index=None) -> None:
        self.edges = [None] * 128
        self.link = None
        self.suffix_start_index = suffix_start_index
        self.parent_start_index = parent_start_index

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
                    end = edge.end[0] if self.is_terminal_edge(edge) else edge.end
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
        parent_index = active_node.parent_start_index if active_node.parent_start_index else j
        
        leaf = Node(suffix_start_index=j)
        internal_node = Node(parent_start_index=parent_index)
        rear_edge = Edge(internal_node, active_edge.start, active_edge.start + active_len - 1)
        active_node.edges[ord(self.text[rear_edge.start])] = rear_edge
        internal_node.edges[ord(self.text[i])] = Edge(leaf, i, global_end)
        active_edge.start += active_len
        internal_node.edges[ord(self.text[active_edge.start])] = active_edge

        return internal_node
    
    def traverse_and_check_matches(self, given_text: str, return_start_index=False) -> int:
        i = 0
        past_edge_length = 0
        n = len(given_text)

        if i >= n:
            return 0
        current_edge = self.suffix_tree.edges[ord(given_text[i])]
        if not current_edge:
            return 0
        start_index = None
        while i < n and self.text[current_edge.start + (i - past_edge_length)] == given_text[i]:
            current_edge_length = self.get_length(current_edge)
            if (i - past_edge_length + 1) == current_edge_length:
                past_edge_length += current_edge_length
                if i + 1 < n:
                    next_edge = current_edge.target.edges[ord(given_text[i + 1])]
                    start_index = current_edge.target.parent_start_index if current_edge.target.parent_start_index else None
                    if next_edge:
                        current_edge = next_edge
                    else:
                        i += 1
                        break
            i += 1
        return i, start_index if return_start_index else i
    
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
                if n-1 == i == j:
                    return root
                if active_len == 0:
                    active_edge = active_node.edges[ord(text[i])]
                    if active_edge is None:
                        leaf = Node(suffix_start_index=j)
                        active_node.edges[ord(text[i])] = Edge(leaf, i, global_end)
                        active_node.parent_start_index = j
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
                        active_edge = active_node.edges[ord(text[j])]
                        # Case 1: no character found after a node
                        if active_edge is None:
                            leaf = Node(suffix_start_index=j)
                            active_node.edges[ord(text[i])] = Edge(leaf, i, global_end)
                            new_leaf_created = True
                            break
                        # Case 2: exact node found with no remainder - set active_node only
                        if active_len == 0:
                            active_edge = active_node.edges[ord(text[i])]
                            break
                        edge_len = self.get_length(active_edge)

                    if new_leaf_created:
                        prev_internal_node = None
                        active_node = active_node.link
                        j += 1
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
                    else:
                        internal_node.link = root
                    prev_internal_node = internal_node

                # At internal node and link found - jump using link
                jumped = False
                if active_node != root and active_node.link is not None:
                    active_node = active_node.link
                    jumped = True
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
                    active_edge = active_node.edges[ord(text[j + 2 if jumped else j + 1])]
                j += 1
        return root

class A2Solver:
    def __init__(self, texts: List[str], patterns: List[str]):
        self.texts = texts
        self.text_trees = [Ukkonen(text) for text in self.texts]
        self.text_trees_rev = [Ukkonen(text[::-1]) for text in self.texts]
        self.patterns = patterns

    def calculate_dl_distance(self, text_index: int, pattern_index: int):
        text_tree = self.text_trees[text_index]
        text_tree_rev = self.text_trees_rev[text_index]
        pattern = self.patterns[pattern_index]
        pattern_rev = pattern[::-1]        
        
        start_index = -1
        dl_distance = -1
        
        match_count_left, start_index = text_tree.traverse_and_check_matches(pattern, return_start_index=True)
        match_count_right = text_tree_rev.traverse_and_check_matches(pattern_rev)

        gap = len(pattern) - (match_count_left + match_count_right)
        if gap < 0:
            dl_distance = 0
        elif gap == 0:
            inserted_char = self.texts[text_index][text_tree.suffix_tree.edges[ord(pattern[0])].start_index_from_text + match_count_left]
            inserted_pattern = pattern[0:match_count_left] + inserted_char + pattern[match_count_left:]
            if text_tree.traverse_and_check_matches(inserted_pattern) == len(pattern)+1:
                dl_distance = 1
        elif gap == 1:
            dl_distance = 1
        elif gap == 2:
            swapped_pattern = pattern[0:match_count_left] + pattern[match_count_left + 1] + pattern[match_count_left] + pattern[match_count_left + 2:]
            if text_tree.traverse_and_check_matches(swapped_pattern) == len(pattern):
                dl_distance = 1
        else:
            dl_distance = -1



        # start_char = pattern[0]
        # if match_count_left <= 1 and dl_distance == 1:
        #     start_char = pattern[1]
        # if dl_distance != -1:
        #     start_index = text_tree.suffix_tree.edges[ord(start_char)].start_index_from_text

        return start_index, dl_distance
    
    def compute_dl_for_all_pairs(self) -> List[List[int]]:
        result = []
        for t in range(len(self.texts)):
            for p in range(len(self.patterns)):
                start_index, dl_distance = self.calculate_dl_distance(t, p)
                if dl_distance != -1:
                    result.append([p, t, start_index, dl_distance])
        return result

def read_all(config_file_path: str):
    f = open(config_file_path, 'r')
    lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    f.close()

    texts, patterns = [], []
    config_content = lines
    file_counts = config_content[0].split(" ")
    text_file_count, pattern_file_count = int(file_counts[0]), int(file_counts[1])
    config_content = config_content[1:]

    for t in range(text_file_count):
        text_filename = config_content[t].split(" ")[1]
        ft = open(text_filename)
        content = ft.readlines()
        texts.append(content[0])
        ft.close()

    for p in range(text_file_count, text_file_count + pattern_file_count):
        pattern_filename = config_content[p].split(" ")[1]
        fp = open(pattern_filename)
        content = fp.readlines()
        patterns.append(content[0])
        fp.close()

    return texts, patterns

def write_to_file(result_file_path: str, content: List[List[int]]):
    f = open(result_file_path, 'w')
    for result in content:
        pattern_number = str(result[0])
        text_number = str(result[1])
        position_of_occurence = str(result[2])
        dl_distance = str(result[3])
        f.write(pattern_number + " " + text_number + " " + position_of_occurence + " " + dl_distance + "\n")
    f.close()

if __name__ == '__main__':
    texts, patterns = read_all('run-configuration')
    solver = A2Solver(texts, patterns)
    # compute_result = solver.compute_dl_for_all_pairs()
    # write_to_file("output_a2.txt", compute_result)

    print(solver.calculate_dl_distance(1, 1))
    # solver.text_trees_rev[1].print_tree()
