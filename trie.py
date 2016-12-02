#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class Node:
    def __init__(self):
        self.value = None
        self.children = {}    # children is of type {char, Node}


class Trie:
    def __init__(self):
        self.root = Node()
        self.get_words = {}
        self.words_weight = {}

    def insert(self, key):      # key is of type string
        # key should be a low-case string, this must be check
        key = key.lower()
        node = self.root
        for char in key:
            if char not in node.children:
                child = Node()
                node.children[char] = child
                node = child
            else:
                node = node.children[char]
        node.value = key

    def get_error_length(self, key):
        if len(key) <= 6:  # error percentage
            rate = 0.2
        elif len(key) >= 18:
            rate = 0.2
        else:
            rate = 0.25

        return int(round(len(key)*rate))

    def best_match(self):
        best_match_words = {}
        best_word_weight = []

        for word in self.get_words:  # get words with weight
            if word in self.words_weight:
                if self.get_words[word] < self.words_weight[word]:
                    self.get_words[word] = self.words_weight[word]

        max_weight = max(value for value in self.get_words.values())
        # get max_weight word

        # get max_weight nearby words
        for word, value in self.get_words.items():
            if (max_weight/value) < 2:
                best_match_words[word] = value
                best_word_weight.append(value)

        best_word_weight = sorted(best_word_weight, reverse=True)

        for weight in best_word_weight:
            for word, value in best_match_words.items():
                if weight == value:
                    print(word)

    def search(self, key):
        node = self.root
        num = self.get_error_length(key)   # allow error num

        for char in key:
            if char in node.children:
                node = node.children[char]

        if node.value and (len(node.value) == len(key)):
            # entire right
            print(node.value)
        else:
            # No found on trie
            self.dfs(key, self.root, num, 0)

            self.best_match()

    def dfs(self, key, node, num, match):
        keep_num = num
        i = 0
        if num > 0:
            for node_char in node.children:  # blank char
                self.dfs(key, node.children[node_char], num-1, match)

            self.dfs(key[1:], node, num-1, match)  # more char

        for char in key:
            i += 1
            if num > 0:  # error char
                for error_char in node.children:
                    self.dfs(key[i:], node.children[error_char], num-1, match)
                num -= 1

            if char in node.children:  # right char
                node = node.children[char]
                match += 1
                self.dfs(key[i:], node, keep_num, match)
            else:
                if num <= 0:
                    return

        if node.value and (not key):  # record word
            if node.value in self.get_words:
                if match > self.get_words[node.value]:
                    self.get_words[node.value] = match
            else:
                self.get_words[node.value] = match

    def get_word_weight(self):
        with open("frequent_words.csv", 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = re.sub(r'\n', '', line)
            line = line.split(',')
            word = line[0].lower()
            weight = line[1]
            self.words_weight[word] = int(weight)

    def create_trie(self):
        with open("words.txt", 'r') as f:
            lines = f.readlines()
        for line in lines:
            self.insert(re.sub(r'\n', '', line))

    def main(self):
        self.create_trie()
        self.get_word_weight()

        while True:
            key = raw_input('please enter word : ')
            key = key.strip()  # 删除word中开头、结尾处的空格
            key = key.lower()
            if len(key) > 22 or re.search(r'[^a-z]', key):
                print('error word!')
            else:
                # print(datetime.now())
                self.search(key)
                # print(datetime.now())
                self.get_words = {}

if __name__ == '__main__':

    trie = Trie()

    trie.main()
