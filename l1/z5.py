from __future__ import print_function
import random 
import numpy as np
from z4 import StateDist

class BoardState:
    def __init__(self, row_size, col_size):
        self.board_state = np.zeros((row_size, col_size), dtype=np.bool)
        self.draw_board_state()

    def draw_board_state(self):
        for i in range(self.board_state.shape[0]):
            for j in range(self.board_state.shape[1]):
                self.board_state[i, j] = random.choice([False, True])

    def print_board_state(self):
        for i in range(self.board_state.shape[0]):
            for j in range(self.board_state.shape[1]):
                if self.board_state[i, j]:
                    print('#', end='')
                else:
                    print(',', end='')
            print()	

    def is_correct_state(self, row_states, col_states):
		for index, row_state in enumerate(row_states):
			if row_state.get_dist(self.board_state[index, :]) > 0:
				return False
		for index, col_state in enumerate(col_states):
			if col_state.get_dist(self.board_state[:, index]) > 0:
				return False
		return True

    def repair_row(self, row_ind, row_state, col_states):
        min_col, max_improvement = 0, float("-inf")
        for i in range(self.board_state.shape[1]):
            row_cost = row_state.get_dist(self.board_state[row_ind, :])
            col_cost = col_states[i].get_dist(self.board_state[:, i])   
            self.board_state[row_ind, i] ^= True
            row_cost -= row_state.get_dist(self.board_state[row_ind, :])  
            col_cost -= col_states[i].get_dist(self.board_state[:, i])   
            if row_cost + col_cost > max_improvement:
                max_improvement = row_cost + col_cost
                min_col = i
            self.board_state[row_ind, i] ^= True	
        self.board_state[row_ind, min_col] ^= True		

    def repair_col(self, col_ind, col_state, row_states):
        min_row, max_improvement = 0, float("-inf")
        for i in range(self.board_state.shape[0]):
            row_cost = row_states[i].get_dist(self.board_state[i, :]) 
            col_cost = col_state.get_dist(self.board_state[:, col_ind]) 
            self.board_state[i, col_ind] ^= True
            row_cost -= row_states[i].get_dist(self.board_state[i, :]) 
            col_cost -= col_state.get_dist(self.board_state[:, col_ind]) 
            if row_cost + col_cost > max_improvement:
                max_improvement = row_cost + col_cost
                min_row = i
            self.board_state[i, col_ind] ^= True
        self.board_state[min_row, col_ind] ^= True

    def repair_board(self, row_states, col_states):
        row_cand_list = filter(lambda x: x[1].get_dist(self.board_state[x[0], :]) > 0, enumerate(row_states))
        if len(row_cand_list) > 0:
            row_ind, row_state = random.choice(row_cand_list)
            self.repair_row(row_ind, row_state, col_states)
            return
        col_cand_list = filter(lambda x: x[1].get_dist(self.board_state[:, x[0]]) > 0, enumerate(col_states))
        if len(col_cand_list) > 0:
            col_ind, col_state = random.choice(col_cand_list)
            self.repair_col(col_ind, col_state, row_states)

def find_solution(row_states, col_states, max_iter=100):
    while True:
        board = BoardState(len(col_states), len(row_states))
        for i in range(max_iter):
            if board.is_correct_state(row_states, col_states):
                return board
            board.repair_board(row_states, col_states)

def main():
    test_list = [  
        ([7,7,7,7,7,7,7], [7,7,7,7,7,7,7]), 
        ([2,2,7,7,2,2,2], [2,2,7,7,2,2,2]), 
        ([2,2,7,7,2,2,2], [4,4,2,2,2,5,5]),
        ([7,6,5,4,3,2,1], [1,2,3,4,5,6,7]),
        ([7,5,3,1,1,1,1], [1,2,3,7,3,2,1])
    ]
    for test in test_list:
        row_states = map(lambda x: StateDist(len(test[1]), x), test[0])
        col_states = map(lambda x: StateDist(len(test[0]), x), test[1])
        board = find_solution(row_states, col_states)
        board.print_board_state()
        print()

if __name__ == '__main__':
    main()


