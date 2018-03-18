class StateDist:
    def __init__(self, word_len, one_count):
        self.word_len = word_len
        self.one_count = one_count
        self.init_state_words()

    def get_swap_count(self, bin_word1, bin_word2):
        dist = 0
        for i in range(len(bin_word1)):
            if bin_word1[i] != bin_word2[i]:
                dist += 1
        return dist

    def generate_one_word(self, start_ind):
        suf_size = self.word_len - self.one_count - start_ind
        return ''.join('0' * start_ind) + ''.join('1' * self.one_count) + ''.join('0' * suf_size) 

    def init_state_words(self):
        self.state_words = []
        for i in range(0, self.word_len - self.one_count + 1):
            self.state_words.append(self.generate_one_word(i))

    def get_dist(self, word):
        word = ''.join(map(lambda x: str(int(x)), word))
        return min(map(lambda x: self.get_swap_count(word, x), self.state_words))
