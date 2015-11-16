#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from datetime import datetime

class Node:
    def __init__(self):
        self.value = None
        self.children = {}    # children is of type {char, Node}                                                                                                       
 
class Trie:
    def __init__(self):
        self.root = Node()
        self.get_words = {}
        self.words = {}
        
 
    def insert(self, key):      # key is of type string                                                                                                                
        # key should be a low-case string, this must be checked here!       
        key = key.lower()                                                                                           
        node = self.root
        for char in key:
            if char not in node.children:
                child = Node()
                node.children[char] = child
                node = child
                node.char = char
            else:
                node = node.children[char]
        node.value = key
 
    def search(self, key):
        node = self.root
        # error percentage
        if len(key)<=6:
            rate = 0.2
        elif len(key)>=18:
            rate = 0.2
        else:
            rate = 0.25

        num = int(round( len(key)*rate ))  # allow error num
        for char in key:
            if char in node.children:
                node = node.children[char]

        if node.value and (len(node.value) ==len(key)):
            # entire right
            print node.value
        else:
            # some error
            self.dfs(key,self.root,num)

            for word in self.get_words:
                if word in self.words:
                    if self.get_words[word] < self.words[word]:
                        self.get_words[word] = self.words[word]

            # self.get_words= sorted(self.get_words.iteritems(), key=lambda d:d[1], reverse = True)
            print self.get_words        

    def dfs(self,key,node,num):
        keep_num = num
        i = 0  
        if num > 0:
            # blank char
            for node_char in node.children:
                self.dfs(key,node.children[node_char],num-1)

            # more char
            self.dfs(key[1:],node,num-1)

        for char in key:
            i +=1
            # error char
            if num > 0:
                for error_char in node.children:
                    self.dfs(key[i:],node.children[error_char],num-1)
                num -=1
            # right char
            if char in node.children:
                node = node.children[char]
                self.dfs(key[i:],node,keep_num)
            else:
                if num <= 0:
                    return
        # record word
        if node.value and (not key):
            if node.value in self.get_words:
                self.get_words[node.value] +=1
            else:
                self.get_words[node.value] = 1

    # def display_node(self, node):
    #     if node.value:
    #         print node.value
    #     for char in node.children:
    #             self.display_node(node.children[char])
 
    # def display(self):
    #     self.display_node(self.root)

    def word_weight(self):
        filename = "frequent_words.csv"
        f = open(filename)
        lines = f.readlines()
        f.close()
        for line in lines:
            line = re.sub(r'\n','',line)
            line = line.split(',')
            word = line[0].lower()
            weight = line[1]
            self.words[word] = int(weight)

    def get_trie(self):
        filename = "words.txt"
        f = open(filename)
        lines = f.readlines()
        f.close()
        for line in lines:
            self.insert(re.sub(r'\n','',line))

    def start(self):
        self.get_trie()
        self.word_weight()
        n = int(raw_input('please input number : '))
        for x in xrange(0,n):
            key = raw_input('please input word : ')
            key = key.lower()
            if len(key) > 22 or re.search(r'[^a-z]',key):
                print 'error word!'
            else:
                # print datetime.now()
                self.search(key)
                # print datetime.now()
                self.get_words = {}
                



if __name__=='__main__':
 
    trie = Trie()

    trie.start()
# trie.display()
# trie.search('ealous')
