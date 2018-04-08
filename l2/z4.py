from __future__ import print_function
import numpy as np
from collections import deque
import sys
import random

class BoardState:
    def __init__(self, occupied_set, start_pos_set, end_pos_set, board_size):
        self.occupied_set = occupied_set
        self.start_pos_set = start_pos_set
        self.end_pos_set = end_pos_set
        self.board_size = board_size
        self.repr = tuple(start_pos_set)

    def __hash__(self):
        return hash(self.repr)

    def __eq__(self, other):
        if isinstance(other, BoardState):
            return self.repr == self.repr
        return False

    def get_neighbour(self, move_dir):
        neigh_pos_set = set()
        for pos in self.start_pos_set:
            neigh_pos = (pos[0] + move_dir[0], pos[1] + move_dir[1])
            if neigh_pos in self.occupied_set:
                neigh_pos_set.add(pos)
            else:
                neigh_pos_set.add(neigh_pos)
        return BoardState(self.occupied_set, neigh_pos_set, self.end_pos_set, self.board_size)

    def get_neighbours(self):
        move_list = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return map(lambda x: (self.get_neighbour(x), x), move_list)

    def is_final_state(self):
        return self.start_pos_set <= self.end_pos_set

    def get_board_size(self):
        return self.board_size

    def get_pos_cost(self, init_pos):
        path_size_map = {init_pos: 0}
        state_queue = deque([init_pos])
        while len(state_queue) > 0:
            cur_pos = state_queue.popleft()
            if cur_pos in self.occupied_set:
                continue
            if cur_pos in self.end_pos_set:
                return path_size_map[cur_pos]
            move_list = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            neigh_pos_list = map(lambda x: (x[0] + cur_pos[0], x[1] + cur_pos[1]), move_list)
            for neigh_pos in neigh_pos_list:
                if neigh_pos not in path_size_map:
                    path_size_map[neigh_pos] = path_size_map[cur_pos] + 1
                    state_queue.append(neigh_pos)
        return 0

    def get_cost(self):
        return max(map(lambda x: self.get_pos_cost(x), self.start_pos_set))

def read_input():
    with open('zad_input.txt', 'r') as input_file:
        input_lines = map(lambda x: list(x), input_file.readlines())
        return np.array(input_lines)            

def greedy_dir_search(board_state, move_dir, step_count): 
    path = []
    for i in range(step_count):
        board_state, neigh_dir = board_state.get_neighbours()[move_dir]
        path.append(neigh_dir)
    return board_state, path

def greedy_random_search(board_state, step_count):
    path = []
    visited_board_set = set()
    for i in range(step_count):
        if len(board_state.start_pos_set) <= 3:
            break
        neigh_list = board_state.get_neighbours()
        cand_list = filter(lambda x: x[0] not in visited_board_set, neigh_list)
        if len(cand_list) == 0:
            cand_list = neigh_list[:]
        board_state, neigh_dir = random.choice(cand_list)
        visited_board_set.add(board_state)
        path.append(neigh_dir)
    return board_state, path

def greedy_max_path_search(board_state, step_count):
    path = []
    for i in range(step_count):
        neigh_list = board_state.get_neighbours()
        min_cost = min(map(lambda x: x[0].get_cost(), neigh_list)) 
        board_state, neigh_dir = random.choice(filter(lambda x: x[0].get_cost() == min_cost, neigh_list))
        path.append(neigh_dir)
    return board_state, path

def greedy_search_path(board_state, step_count=130):
    path = []
    row_dir, row_step_count = np.random.choice([0, 1]), board_state.get_board_size()[0]
    row_search = (lambda: greedy_dir_search(board_state, row_dir, row_step_count))
    col_dir, col_step_count = np.random.choice([2, 3]), board_state.get_board_size()[1]
    col_search = (lambda: greedy_dir_search(board_state, col_dir, col_step_count))
    for search_func in np.random.permutation([row_search, col_search]):
        board_state, dir_path = search_func()
        path += dir_path
    board_state, dir_path = greedy_random_search(board_state, step_count - len(path))
    path += dir_path
    board_state, dir_path = greedy_max_path_search(board_state, step_count - len(path))
    path += dir_path
    return (board_state, path)

def construct_path(prev_state_map, prev_offset_map, cur_state):
    path = []
    while prev_offset_map[cur_state] is not None:
        path.append(prev_offset_map[cur_state])
        cur_state = prev_state_map[cur_state]
    return list(reversed(path))

def bfs_search_path(init_state, step_count=20):
    state_queue = deque([init_state])
    prev_state_map = {init_state: None}
    prev_offset_map = {init_state: None}
    path_size_map = {init_state: 0}
    while len(state_queue) > 0:
        cur_state = state_queue.popleft()
        if cur_state.is_final_state():
            return (cur_state, construct_path(prev_state_map, prev_offset_map, cur_state))
        if path_size_map[cur_state] > step_count:
            return (cur_state, [])
        neigh_list = cur_state.get_neighbours()
        for neigh, offset in neigh_list:
            if neigh not in prev_state_map:
                prev_state_map[neigh] = cur_state
                prev_offset_map[neigh] = offset
                path_size_map[neigh] = path_size_map[cur_state] + 1
                state_queue.append(neigh)
    return (cur_state, [])

def search_path(init_state):
    while True:
        board_state, greedy_path = greedy_search_path(init_state)
        if len(board_state.start_pos_set) > 3 or board_state.get_cost() > 20:
            continue
        board_state, bfs_path = bfs_search_path(board_state)
        if board_state.is_final_state():
            return greedy_path + bfs_path

def get_pos_list(board_str, pos_type_list):
    pos_list = []
    for i in range(board_str.shape[0]):
        for j in range(board_str.shape[1]):
            if board_str[i][j] in pos_type_list:
                pos_list.append((i, j))
    return pos_list

def map_offset(offset):
    return {
        (-1, 0): 'U',
        (1, 0): 'D',
        (0, -1): 'L',
        (0, 1): 'R'
    }[offset]

def main():
    board_str = read_input()
    occupied_set = set(get_pos_list(board_str, ['#']))
    start_pos_set = set(get_pos_list(board_str, ['S', 'B']))
    end_pos_set = set(get_pos_list(board_str, ['G', 'B']))
    board_state = BoardState(occupied_set, start_pos_set, end_pos_set, board_str.shape)
    path = search_path(board_state)
    sys.stdout = open('zad_output.txt', 'w')
    print(''.join(map(lambda x: map_offset(x), path)))

main()
