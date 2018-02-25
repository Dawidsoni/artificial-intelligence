def get_dist(bin_word1, bin_word2):
    dist = 0
    for i in range(len(bin_word1)):
        if bin_word1[i] != bin_word2[i]:
            dist += 1
    return dist

def generate_one_word(word_len, one_count, start_ind):
    suf_size = word_len - one_count - start_ind
    return ''.join('0' * start_ind) + ''.join('1' * one_count) + ''.join('0' * suf_size) 

def get_min_swap_count(word, one_count):
    min_swap_count = float("inf")
    for i in range(0, len(word) - one_count + 1):
        one_word = generate_one_word(len(word), one_count, i)
        min_swap_count = min(min_swap_count, get_dist(word, one_word))
    return min_swap_count

def main():
    word, one_count = raw_input(), int(raw_input())
    print(get_min_swap_count(word, one_count))

main()
