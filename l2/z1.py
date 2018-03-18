import sys, os
sys.path.insert(0, os.path.abspath('..'))
from l1.z5 import BoardState
import fileinput
import time
import random

class HoleStateDist:
    def __init__(self, word_size, hole_sizes):
        self.word_size = word_size
        self.hole_sizes = hole_sizes
        self.state_words = None
        self.init_state_words()
    
    def generate_cand_words(self, cur_word='', pos=0):
        if pos == self.word_size:
            return [cur_word]
        zero_word = cur_word + '0'
        one_word = cur_word + '1'
        cand_words = []
        cand_words += self.generate_cand_words(zero_word, pos + 1)
        cand_words += self.generate_cand_words(one_word, pos + 1)
        return cand_words

    def is_state_word(self, word):
        cur_hole = 0
        word_holes = []
        word += '0'
        for i in range(len(word)):
            if word[i] == '1':
                cur_hole += 1
            elif cur_hole > 0:
                word_holes.append(cur_hole)
                cur_hole = 0
        return (word_holes == self.hole_sizes)

    def init_state_words(self):
        cand_words = self.generate_cand_words()
        self.state_words = filter(lambda x: self.is_state_word(x), cand_words)
        self.state_words = map(lambda word: map(lambda x: bool(int(x)), word), self.state_words)

class ExtBoardState(BoardState):
    def __init__(self, row_count, col_count):
        BoardState.__init__(self, row_count, col_count)
    
    def is_row_matched(self, col_num, row_num, row_state, pref):
        for index in range(pref, len(row_state.state_words)):
            board_slice = list(self.board_state[row_num, 0:(col_num + 1)])
            state_slice = row_state.state_words[index][0:(col_num + 1)]
            if board_slice == state_slice:
                return index
        return -1
        
    def are_cols_matched(self, col_num, row_states, pref_list):
        next_pref_list = [0 for i in range(len(row_states))]
        for i in range(len(row_states)):
            row_num = self.is_row_matched(col_num, i, row_states[i], pref_list[i])
            if row_num == -1:
                return []
            next_pref_list[i] = row_num
        return next_pref_list

    def repair_board(self, row_states, col_states, col_num=0, pref_list=None):
        if pref_list is None:
            pref_list = [0 for i in range(len(row_states))]
        if col_num >= self.board_state.shape[1]:
            return True
        for state_word in col_states[col_num].state_words:
            self.board_state[:, col_num] = state_word
            next_pref_list = self.are_cols_matched(col_num, row_states, pref_list) 
            if len(next_pref_list) == 0:
                continue
            if self.repair_board(row_states, col_states, col_num + 1, next_pref_list):
                return True
        return False

def find_solution(row_states, col_states, max_iter=300):
    board = ExtBoardState(len(row_states), len(col_states))
    board.repair_board(row_states, col_states)
    return board

def read_input():
    with open('zad_input.txt', 'r') as input_file:
        input_lines = iter(input_file.readlines())
    row_count, col_count = map(lambda x: int(x), next(input_lines).split())
    row_nums, col_nums = [], []
    for i in range(row_count):
        row_nums.append(map(lambda x: int(x), next(input_lines).split()))
    for i in range(col_count):
        col_nums.append(map(lambda x: int(x), next(input_lines).split()))
    return row_nums, col_nums

def main():
    row_nums, col_nums = read_input()
    row_states = map(lambda x: HoleStateDist(len(col_nums), x), row_nums)
    col_states = map(lambda x: HoleStateDist(len(row_nums), x), col_nums)
    board = find_solution(row_states, col_states)
    sys.stdout = open('zad_output.txt', 'w')
    board.print_board_state()

main()
