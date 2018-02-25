from collections import deque

class GameState:
    def __init__(self, king0_pos, rook0_pos, king1_pos, player_num):
        self.king0_pos = king0_pos
        self.rook0_pos = rook0_pos
        self.king1_pos = king1_pos
        self.player_num = player_num 

    def get_opponent_player(self):
        return self.player_num ^ 1

    def get_moved_field(self, field, direction):
        return (field[0] + direction[0], field[1] + direction[1])

    def is_field_valid(self, field):
        return (field[0] >= 0 and field[0] <= 7 and field[1] >= 0 and field[1] <= 7)

    def is_field_empty(self, field):
        return (field not in [self.king0_pos, self.rook0_pos, self.king1_pos])

    def get_repr(self):
        return (self.king0_pos, self.rook0_pos, self.king1_pos, self.player_num)

    def __hash__(self):
        return hash(self.get_repr())

    def __eq__(self, other):
        if isinstance(other, GameState):
            return self.get_repr() == other.get_repr()
        return False

    def get_rook0_dir_neighbours(self, direction):
        neigh_list = []
        for move_size in range(1, 8):
            move_pos = (direction[0] * move_size, direction[1] * move_size)
            rook_pos = self.get_moved_field(self.rook0_pos, move_pos)
            if self.is_field_valid(rook_pos) == False or self.is_field_empty(rook_pos) == False:
                break
            neigh_list.append(GameState(self.king0_pos, rook_pos, self.king1_pos, self.get_opponent_player()))
        return neigh_list

    def get_rook0_neighbours(self):
        neigh_func = (lambda x: self.get_rook0_dir_neighbours(x))
        return neigh_func((1, 0)) + neigh_func((-1, 0)) + neigh_func((0, 1)) + neigh_func((0, -1))

    def is_king_move_valid(self, king_pos, opp_king_pos, banned_x=None, banned_y=None):
        if self.is_field_valid(king_pos) == False or self.is_field_empty(king_pos) == False:
            return False
        if king_pos[0] == banned_x or king_pos[1] == banned_y:
            return False
        dist_x = abs(king_pos[0] - opp_king_pos[0])
        dist_y = abs(king_pos[1] - opp_king_pos[1])
        return (dist_x > 1 or dist_y > 1)

    def get_king0_neighbours(self):
        neigh_list = []
        for dir_x in [-1, 0, 1]:
            for dir_y in [-1, 0, 1]:
                if dir_x == 0 and dir_y == 0:
                    continue
                king_pos = self.get_moved_field(self.king0_pos, (dir_x, dir_y))
                if self.is_king_move_valid(king_pos, self.king1_pos):
                    neigh_list.append(GameState(king_pos, self.rook0_pos, self.king1_pos, self.get_opponent_player()))
        return neigh_list

    def get_king1_neighbours(self):
        neigh_list = []
        for dir_x in [-1, 0, 1]:
            for dir_y in [-1, 0, 1]:
                if dir_x == 0 and dir_y == 0:
                    continue
                king_pos = self.get_moved_field(self.king1_pos, (dir_x, dir_y))
                if self.is_king_move_valid(king_pos, self.king0_pos, self.rook0_pos[0], self.rook0_pos[1]):
                    neigh_list.append(GameState(self.king0_pos, self.rook0_pos, king_pos, self.get_opponent_player()))
        return neigh_list

    def get_neighbours(self):
        if self.player_num == 0:
            return self.get_king0_neighbours() + self.get_rook0_neighbours()
        else:
            return self.get_king1_neighbours()

def encode_position(pos_str):
    return (ord(pos_str[0]) - ord('a'), int(pos_str[1]) - 1)

def decode_position(pos):
    return chr(ord('a') + pos[0]) + str(pos[1] + 1)

def encode_player(player_str):
    return {'white': 0, 'black': 1}[player_str] 

def decode_player(player):
    return {0: 'white', 1: 'black'}[player]

def construct_path(prev_state_map, cur_state):
    path = []
    while cur_state is not None:
        path.append(cur_state)
        cur_state = prev_state_map[cur_state]
    return list(reversed(path))

def get_step_path(init_state):
    state_queue = deque([init_state])
    prev_state_map = {init_state: None}
    while len(state_queue) > 0:
        cur_state = state_queue.popleft()
        neigh_list = cur_state.get_neighbours()
        if len(neigh_list) == 0:
            return construct_path(prev_state_map, cur_state)
        for neigh in neigh_list:
            if neigh not in prev_state_map:
                prev_state_map[neigh] = cur_state
                state_queue.append(neigh)
    return []

def create_game_state(player_str, king0_str, rook0_str, king1_str):
    king0_pos, rook0_pos, king1_pos = map(lambda x: encode_position(x), [king0_str, rook0_str, king1_str])
    player_num = encode_player(player_str)
    return GameState(king0_pos, rook0_pos, king1_pos, player_num)

def main():
    player_str, king0_str, rook0_str, king1_str = raw_input().split()
    game_state = create_game_state(player_str, king0_str, rook0_str, king1_str)
    print(len(get_step_path(game_state)))

if __name__ == "__main__":
    main()
