"""
COMS W4705 - Natural Language Processing - Summer 2022
Homework 2 - Parsing with Probabilistic Context Free Grammars 
Daniel Bauer
"""
from curses import termname
import math
from symbol import term
import sys
from collections import defaultdict
import itertools
from grammar import Pcfg
from pprint import pprint

### Use the following two functions to check the format of your data structures in part 3 ###
def check_table_format(table):
    """
    Return true if the backpointer table object is formatted correctly.
    Otherwise return False and print an error.  
    """
    if not isinstance(table, dict): 
        sys.stderr.write("Backpointer table is not a dict.\n")
        return False
    for split in table: 
        if not isinstance(split, tuple) and len(split) ==2 and \
          isinstance(split[0], int)  and isinstance(split[1], int):
            sys.stderr.write("Keys of the backpointer table must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write("Value of backpointer table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str): 
                sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            bps = table[split][nt]
            if isinstance(bps, str): # Leaf nodes may be strings
                continue 
            if not isinstance(bps, tuple):
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Incorrect type: {}\n".format(bps))
                return False
            if len(bps) != 2:
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Found more than two backpointers: {}\n".format(bps))
                return False
            for bp in bps: 
                if not isinstance(bp, tuple) or len(bp)!=3:
                    sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has length != 3.\n".format(bp))
                    return False
                if not (isinstance(bp[0], str) and isinstance(bp[1], int) and isinstance(bp[2], int)):
                    print(bp)
                    sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a pair ((i,k,A),(k,j,B)) of backpointers. Backpointer has incorrect type.\n".format(bp))
                    return False
    return True

def check_probs_format(table):
    """
    Return true if the probability table object is formatted correctly.
    Otherwise return False and print an error.  
    """
    if not isinstance(table, dict): 
        sys.stderr.write("Probability table is not a dict.\n")
        return False
    for split in table: 
        if not isinstance(split, tuple) and len(split) ==2 and isinstance(split[0], int) and isinstance(split[1], int):
            sys.stderr.write("Keys of the probability must be tuples (i,j) representing spans.\n")
            return False
        if not isinstance(table[split], dict):
            sys.stderr.write("Value of probability table (for each span) is not a dict.\n")
            return False
        for nt in table[split]:
            if not isinstance(nt, str): 
                sys.stderr.write("Keys of the inner dictionary (for each span) must be strings representing nonterminals.\n")
                return False
            prob = table[split][nt]
            if not isinstance(prob, float):
                sys.stderr.write("Values of the inner dictionary (for each span and nonterminal) must be a float.{}\n".format(prob))
                return False
            if prob > 0:
                sys.stderr.write("Log probability may not be > 0.  {}\n".format(prob))
                return False
    return True



class CkyParser(object):
    """
    A CKY parser.
    """

    def __init__(self, grammar): 
        """
        Initialize a new parser instance from a grammar. 
        """
        self.grammar = grammar

    def is_in_language(self,tokens):
        """
        Membership checking. Parse the input tokens and return True if 
        the sentence is in the language described by the grammar. Otherwise
        return False
        """
        # TODO, part 2
        #return False 
        # Grammar = (n, sig, r, s)
        #   n = non terminals
        #   sig = terminal symbols
        #   r = production rules (n -> (n u sig))
        #   s = start symbol (in n)

        table = {}
        n = len(tokens)

        # initialize base cases
        for i in range(n):
            table[(i,i + 1)] = {}
            # getting rules for each word 
            terminal_rules = self.grammar.rhs_to_rules
            #print(tokens[i])

            #print(tokens[i])
            #pprint(terminal_rules[(tokens[i],)])
            #print(terminal_rules[('FROM',)])

            # iterating through each rule to get possible terminal transitions
            for rule in terminal_rules[(tokens[i],)]:
                table[(i,i + 1)][rule[0]] = tokens[i]

        # setting up main recursive loop
        for length in range(2, n + 1):
            # looping through starts
            for i in range((n - length + 1)):
                # setting ends
                j = i + length

                # creating idx dict
                table[i,j] = {}
                
                # looping through splits
                for k in range((i + 1), j):
                    # loop through all possible permutations of BC
                    for B in table[(i, k)]:
                        for C in table[(k, j)]:
                            # checking if valid combo 
                            if (B,C) in terminal_rules.keys():
                                print((B,C))
                                rules_BC = terminal_rules[(B,C)]
                                print(rules_BC)
                                # add rule to table (includes backponiters [i think lol]) (or maybe all rules)
                                # table[i,j][rules_BC[0][0]] = ((B,i,k), (C,k,j))
                                for rule in rules_BC:
                                    table[i,j][rule[0]] = ((B,i,k), (C,k,j))

        #print(table)
        pprint(table)

        # checking if valid
        if self.grammar.startsymbol in table[0, n]:
            return True
        else:
            return False

       
    def parse_with_backpointers(self, tokens):
        """
        Parse the input tokens and return a parse table and a probability table.
        """
        # TODO, part 3
        table= {}
        probs = {}

        n = len(tokens)

        #copy paste from 2
        # initialize base cases
        for i in range(n):
            table[(i,i + 1)] = {}
            probs[(i,i + 1)] ={}
            # getting rules for each word 
            terminal_rules = self.grammar.rhs_to_rules

            # iterating through each rule to get possible terminal transitions
            # do an if in rules else prob 0#######
            
            for rule in terminal_rules[(tokens[i],)]:
                print(rule)
                print(math.log(rule[2]))
                table[(i,i + 1)][rule[0]] = tokens[i]
                probs[(i,i + 1)][rule[0]] = math.log(rule[2])


        # setting up main recursive loop
        for length in range(2, n + 1):
            # looping through starts
            for i in range((n - length + 1)):
                # setting ends
                j = i + length

                # creating idx dict
                table[i,j] = {}
                probs[i,j] = {}
                
                # looping through splits
                for k in range((i + 1), j):
                    # loop through all possible permutations of BC
                    for B in table[(i, k)]:
                        for C in table[(k, j)]:
                            # checking if valid combo 
                            if (B,C) in terminal_rules.keys():
                                #print((B,C))
                                rules_BC = terminal_rules[(B,C)]
                                #print(rules_BC)
                                # add rule to table (includes backponiters [i think lol]) (or maybe all rules)
                                # table[i,j][rules_BC[0][0]] = ((B,i,k), (C,k,j))


                                ### should change this to account for single tuple of backpointers and adding to prob table
                                for rule in rules_BC:
                                    # checking if some backpointers not already in dict 
                                    #if len(table[i,j][rule[0]]) == 0:
                                    if rule[0] not in table[i,j]:
                                        # add backpointers to table
                                        table[i,j][rule[0]] = ((B,i,k), (C,k,j))
                                        # add probability to table
                                        probs[i,j][rule[0]] = math.log(rule[2])
                                    elif math.log(rule[2]) > probs[i,j][rule[0]]:
                                        # add backpointers to table
                                        table[i,j][rule[0]] = ((B,i,k), (C,k,j))
                                        # add probability to table
                                        probs[i,j][rule[0]] = math.log(rule[2])

        #print(table)
        #pprint(table)
        # probability is incorrect, as not adding and not initializing base probs

        return table, probs


def get_tree(chart, i,j,nt): 
    """
    Return the parse-tree rooted in non-terminal nt and covering span i,j.
    """
    # TODO: Part 4
    # establish base case
    if j == i + 1:
        # getting most probable
        '''most_prob = ""
        for symbol in probs[(i,j)]:
            if most_prob == "":
                most_prob = symbol
            elif probs[symbol] < probs[most_prob]:
                most_prob = symbol'''
        

        return (nt, chart[(i,j)][nt])

    else:
        B = chart[(i,j)][nt][0]
        C = chart[(i,j)][nt][1]
        return (nt, (get_tree(chart, B[1], B[2], B[0])), (get_tree(chart, C[1], C[2], C[0])))
    #return None 
 
       
if __name__ == "__main__":
    
    with open('atis3.pcfg','r') as grammar_file: 
        grammar = Pcfg(grammar_file) 
        parser = CkyParser(grammar)
        toks =['flights', 'from','miami', 'to', 'cleveland','.'] 
        #parser.is_in_language(toks)
        print(parser.is_in_language(toks))
        table,probs = parser.parse_with_backpointers(toks)

        pprint(table)
        #pprint(probs)
        assert check_table_format(table)
        assert check_probs_format(probs)
        
        print(get_tree(table, 0, len(toks), grammar.startsymbol))
        print(get_tree(table, 3, 5, 'PP'))
