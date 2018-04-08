from __future__ import print_function
import numpy as np 
import sys
from collections import deque
from Queue import PriorityQueue

class BoardState:
    CHEST_COST = 5

    def __init__(self, board_state):
        self.board_state = board_state
        self.repr = ''.join(''.join(word for word in line) for line in self.board_state)

    def get_repr(self):
        return self.repr

    def __hash__(self):
        return hash(self.get_repr())

    def __eq__(self, other):
        if isinstance(other, BoardState):
            return self.get_repr() == other.get_repr()
        return False
    
    def get_moved(self, pos, offset):
        return (pos[0] + offset[0], pos[1] + offset[1])

    def get_warehouseman_pos(self):
        ind = np.where(self.board_state == 'K')
        if len(ind[0]) != 0:
            return (ind[0][0], ind[1][0])
        ind = np.where(self.board_state == '+')
        return (ind[0][0], ind[1][0])

    def is_neighbour(self, offset):
        old_pos = self.get_warehouseman_pos()
        new_pos = self.get_moved(old_pos, offset)
        beh_pos = self.get_moved(new_pos, offset)
        if self.board_state[new_pos] == 'W':
            return False
        if self.board_state[new_pos] in ['B', '*'] and self.board_state[beh_pos] == 'W':
            return False
        if self.board_state[new_pos] in ['B', '*'] and self.board_state[beh_pos] in ['B', '*']:
            return False
        return True

    def get_neighbour(self, offset):
        neigh_state = np.copy(self.board_state)
        old_pos = self.get_warehouseman_pos()
        new_pos = self.get_moved(old_pos, offset)
        beh_pos = self.get_moved(new_pos, offset)
        if self.board_state[old_pos] == '+':
            neigh_state[old_pos] = 'G'
        else:
            neigh_state[old_pos] = '.'
        if self.board_state[new_pos] in ['G', '*']:
            neigh_state[new_pos] = '+'    
        else:
            neigh_state[new_pos] = 'K'
        if self.board_state[new_pos] in ['B', '*'] and self.board_state[beh_pos] in ['G', '+']:
            neigh_state[beh_pos] = '*' 
        elif self.board_state[new_pos] in ['B', '*']:
            neigh_state[beh_pos] = 'B'
        return BoardState(neigh_state)

    def get_neighbours(self):
        neighbours = []
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.is_neighbour(offset):
                neighbours.append((self.get_neighbour(offset), offset))
        return neighbours

    def is_final_state(self):
        return all([x != 'B' for x in self.get_repr()])

    def print_state(self):
        for line in self.board_state:
            print(''.join(line), end='')

    def cost_estimate(self):
        return self.get_repr().count('B') * self.CHEST_COST

def read_input():
    with open('zad_input.txt', 'r') as input_file:
        input_lines = map(lambda x: list(x), input_file.readlines())
        return np.array(input_lines)

def construct_path(prev_state_map, prev_offset_map, cur_state):
    path = []
    while prev_offset_map[cur_state] is not None:
        path.append(prev_offset_map[cur_state])
        cur_state = prev_state_map[cur_state]
    return list(reversed(path))

def bfs(init_state):
    state_queue = deque([init_state])
    prev_state_map = {init_state: None}
    prev_offset_map = {init_state: None}
    while len(state_queue) > 0:
        cur_state = state_queue.popleft()
        if cur_state.is_final_state():
            return construct_path(prev_state_map, prev_offset_map, cur_state)
        neigh_list = cur_state.get_neighbours()
        for neigh, offset in neigh_list:
            if neigh not in prev_state_map:
                prev_state_map[neigh] = cur_state
                prev_offset_map[neigh] = offset
                state_queue.append(neigh)
    return []
    
def a_star(init_state):
    state_queue = PriorityQueue()
    state_queue.put((0, init_state))
    prev_state_map = {init_state: None}
    prev_offset_map = {init_state: None}
    processed_set = set()
    g_score = {init_state: 0}
    f_score = {init_state: init_state.cost_estimate()}
    while not state_queue.empty():
        cur_score, cur_state = state_queue.get()
        if cur_state in processed_set:
            continue
        processed_set.add(cur_state)
        if cur_state.is_final_state():
            return construct_path(prev_state_map, prev_offset_map, cur_state)
        neigh_list = cur_state.get_neighbours()
        for neigh, offset in neigh_list:
            if neigh in prev_state_map:
                continue
            neigh_g_score = g_score[cur_state] + 1
            if neigh in g_score and neigh_g_score >= g_score[neigh]:
                continue
            prev_state_map[neigh] = cur_state
            prev_offset_map[neigh] = offset
            g_score[neigh] = neigh_g_score
            f_score[neigh] = g_score[neigh] + neigh.cost_estimate()
            state_queue.put((f_score[neigh], neigh))
    return []

def map_offset(offset):
    return {
        (-1, 0): 'U', 
        (1, 0): 'D',
        (0, -1): 'L',
        (0, 1): 'R'
    }[offset]

def main():
    board_str = read_input()
    board_state = BoardState(board_str)
    sys.stdout = open('zad_output.txt', 'w')
    for path_func in [bfs]:
        offset_list = path_func(board_state)
        print(''.join(map(lambda x: map_offset(x), offset_list)))

main()

