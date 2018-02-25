import math

class WordSet:
    def __init__(self, word_list):
        self.word_set = set(word_list)
        self.max_word_size = 0
        for word in word_list:
            self.max_word_size = max(self.max_word_size, len(word))

    def get_matched_words(self, text):
        matched_words = []
        for i in range(1, self.max_word_size + 1):
            if text[:i] in self.word_set:
                matched_words.append(text[:i])
        return matched_words

def get_words_list():
    with open("polish_words.txt", 'r') as f_stream:
        words_str = f_stream.read()
        return list(words_str.split())

def get_split_cost(text, word_set, cost_map, words_map):
    if len(text) in cost_map:
        return cost_map[len(text)]
    if len(text) == 0:
        cost_map[0] = 0
        return cost_map[0]
    matched_words = word_set.get_matched_words(text)
    max_cost, best_word = 0, ''
    for matched_word in matched_words:
        cur_cost = get_split_cost(text[len(matched_word):], word_set, cost_map, words_map)
        cur_cost += len(matched_word) ** 2
        if cur_cost > max_cost:
            max_cost = cur_cost
            best_word = matched_word
    cost_map[len(text)] = max_cost
    words_map[len(text)] = best_word
    return cost_map[len(text)]

def divide_text(text, word_set):
    cost_map = {}
    words_map = {}
    get_split_cost(text, word_set, cost_map, words_map)
    if cost_map[len(text)] == -1:
        return text
    text_ind = 0
    divided_text = []
    while text_ind < len(text):
        cur_word = words_map[len(text) - text_ind]
        divided_text.append(cur_word)
        text_ind += len(cur_word)
        if len(cur_word) == 0:
            return ''
    return ' '.join(divided_text)

def main():
    word_list = get_words_list()
    word_set = WordSet(word_list)
    while True:
        try:
            text = raw_input()
            print(divide_text(text, word_set))
        except (EOFError):
            break

main()
