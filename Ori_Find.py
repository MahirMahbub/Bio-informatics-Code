# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:35:11 2020

@author: Mahir Mahbub
"""
from typing import List

Vector = List[str]

class Ori_Finding(object):
    def __init__(self, k):
        self.pattern: Vector = []
        self.nucluoids = ["A", "C", "G", "T" ]
        self.k = k
    
    def reverse_complement(self, sequence):
        reverse: str = ""
        for i in sequence:
            if i == "A":
                reverse = "T" + reverse 
            elif i == "T":
                reverse = "A" + reverse 
            elif i == "G":
                reverse = "C" + reverse 
            elif i == "C":
                reverse = "G" + reverse 
        return reverse
    def pattern_matching(self, sequence, pattern):
        pattern_len = len(pattern)
        idx_list = []
        for i in range(len(sequence)-pattern_len+1):
            if sequence[i:i+pattern_len] == pattern:
                idx_list.append(i)
        return idx_list
    
    def number_to_pattern(self, index):
        if len(self.pattern) == 0:
            self.pattern_generator()
        
        return self.pattern[index]
    
    def frequent_words_dic(self, sequence):
        counts = dict()
        for i in range(len(sequence)-self.k+1):
            counts[sequence[i:(i+self.k)]] = counts.get(sequence[i:(i+self.k)], 0) + 1
        frequency = max(counts.values())
        return [t for t, v in counts.items() if v == frequency]
            
    def pattern_to_number(self, pattern):
        if len(self.pattern) == 0:
            self.pattern_generator()
        #print(self.pattern)
        return self.pattern.index(pattern)
         
    def pattern_generator(self, current_pattern: str = "", k_count: int = 0) -> int:
        if k_count == self.k:
            self.pattern.append(current_pattern)
            return 1
        
        for pat in self.nucluoids:
            val = self.pattern_generator(current_pattern+pat, k_count+1)
            if val == 0:
                return 0
    def pattern_count(self, sequence, pattern):
        count = 0
        pattern_len = len(pattern)
        for i in range(len(sequence)-pattern_len+1):
            if sequence[i:i+pattern_len] == pattern:
                count+=1
        return count
    
    def computing_frequencies(self, sequence):
        frequency_array = [0 for i in range(4**self.k)]
        for start_idx in range(len(sequence)-self.k+1):
            pattern = sequence[start_idx:start_idx+self.k]
            
            pattern_idx = self.faster_pattern_to_number(pattern)
            #print(pattern, pattern_idx)
            frequency_array[pattern_idx] += 1
        return frequency_array
    
    def frequent_words(self, sequence):
        freq_array = self.computing_frequencies(sequence)
        max_freq = max(freq_array)
        max_freq_word = []
        for idx in range(len(freq_array)):
            if freq_array[idx] == max_freq:
                max_freq_word.append(self.faster_number_to_pattern(idx))
        return max_freq_word
    
    def faster_frequent_words(self, text):
        frequent_pattern = set()
        frequency_list = self.computing_frequencies(text)
        max_count = max(frequency_list)
        last = 4 ** self.k
        for i in range(last):
            if frequency_list[i] == max_count:
                pattern = self.number_to_pattern(i)
                frequent_pattern.add(pattern)
        return list(frequent_pattern)
    def faster_pattern_to_number(self, pattern):
        pattern= pattern[::-1]
        frequency_array = [4**i for i in range(self.k)]
        for i in range(len(frequency_array)):
            if pattern[i] == "A":
                frequency_array[i] *= 0
            elif pattern[i] == "C":
                frequency_array[i] *= 1
            elif pattern[i] == "G":
                frequency_array[i] *= 2
            elif pattern[i] == "T":
                frequency_array[i] *= 3
        return sum(frequency_array)
    
    def faster_number_to_pattern(self, index):
        pattern = ""
        for i in range(self.k):
            symbol = self.nucluoids[index%4]
            pattern=symbol+pattern
            index //= 4
        return pattern
    def clump_finding(self, sequence, L, t):
        frequent_patterns = set()
        clump = [0 for i in range(4**self.k)]
        for i in range(len(sequence)-L+1):
            text = sequence[i:i+L]
            frequency_array = self.computing_frequencies(text)
            for idx in range(4**self.k):
                if frequency_array[idx] >= t:
                    clump[idx] = 1
        for i in range(4**self.k):
            if clump[i] == 1:
                pattern = self.faster_number_to_pattern(i)
                frequent_patterns.add(pattern)
        return list(frequent_patterns)
    
    def better_clump_finding(self, sequence, L, t):
        frequent_patterns = set()
        clump = [0 for i in range(4**self.k)]
        text = sequence[0:L]
        frequency_array = self.computing_frequencies(text)
        for i in range(4**self.k):
            if frequency_array[i] >= t:
                clump[i] = 1
        for i in range(1, len(sequence)-L+1):
            first_pattern = sequence[i-1: i-1+self.k]
            idx = self.faster_pattern_to_number(first_pattern)
            frequency_array[idx] = frequency_array[idx] - 1
            
            last_pattern = sequence[i+L-self.k:i+L]
            idx = self.faster_pattern_to_number(last_pattern)
            frequency_array[idx] = frequency_array[idx] + 1
            if frequency_array[idx] >= t:
                clump[idx] = 1
        for i in range(4 ** self.k):
             if clump[i] == 1:
                pattern = self.faster_number_to_pattern(i)
                frequent_patterns.add(pattern)
        return list(frequent_patterns)
    def hamming_distance(self, pattern_1, pattern_2):
        count = 0
        for i in range(len(pattern_1)):
            if pattern_1[i] != pattern_2[i]:
                count+=1
        return count
    
    def approx_pattern_matching(self, pattern, sequence, d):
        pattern_pos= []
        pattern_len = len(pattern)
        for i in range(len(sequence)-pattern_len+1):
            if self.hamming_distance(pattern, sequence[i:i+pattern_len]) <= d:
                pattern_pos.append(i)
        return pattern_pos
    
    def approx_pattern_matching_count(self, pattern, sequence, d):
        return len(self.approx_pattern_matching(pattern, sequence, d))
                
                

if __name__ == "__main__":
    #le = len("AGTC")
    fin = Ori_Finding(9)
    pattern = "ATCTGG"
    sequence = input()
    d = 2
    print(fin.approx_pattern_matching_count(pattern, sequence, d))
    #text = input()
    #with open('E_coli.txt', 'r') as file:
    #    text = file.read().replace('\n', '')
    #with open('Vibrio_cholerae.txt', 'r') as file:
    #    text = file.read().replace('\n', '')
    #v = fin.frequent_words('TGCCCGAGGCTGCGAAT')
    #v = fin.better_clump_finding(text, 500, 3)
    #v = fin.pattern_matching(text, "CTTGATCAT")
    #v = fin.pattern_count("GCGCG", "GCG")
    #inp1 = input()
    #inp2 = input()
    #v = fin.hamming_distance(inp1, inp2)
    #fin.pattern_generator()
    #v = fin.pattern
    #v = fin.pattern_to_number('TATGC')
    #v1 = fin.faster_pattern_to_number('TGCCCGAGGCTGCGAAT')
    #v1 = fin.faster_number_to_pattern(6102)
    #v = fin.number_to_pattern(5437)
    #v = fin.faster_frequent_words(text)
    #print('whatever', file=f)
    #print(v)