"""
COMS W4705 - Natural Language Processing - Summer 2022 
Homework 2 - Parsing with Context Free Grammars 
Daniel Bauer
"""

import sys
from collections import defaultdict
from math import fsum, isclose

class Pcfg(object): 
    """
    Represent a probabilistic context free grammar. 
    """

    def __init__(self, grammar_file): 
        self.rhs_to_rules = defaultdict(list)
        self.lhs_to_rules = defaultdict(list)
        self.startsymbol = None 
        self.read_rules(grammar_file)      
 
    def read_rules(self,grammar_file):
        
        for line in grammar_file: 
            line = line.strip()
            if line and not line.startswith("#"):
                if "->" in line: 
                    rule = self.parse_rule(line.strip())
                    lhs, rhs, prob = rule
                    self.rhs_to_rules[rhs].append(rule)
                    self.lhs_to_rules[lhs].append(rule)
                else: 
                    startsymbol, prob = line.rsplit(";")
                    self.startsymbol = startsymbol.strip()
                    
     
    def parse_rule(self,rule_s):
        lhs, other = rule_s.split("->")
        lhs = lhs.strip()
        rhs_s, prob_s = other.rsplit(";",1) 
        prob = float(prob_s)
        rhs = tuple(rhs_s.strip().split())
        return (lhs, rhs, prob)

    def verify_grammar(self):
        """
        Return True if the grammar is a valid PCFG in CNF.
        Otherwise return False. 
        """
        # TODO, Part 1
        #return False 

        # iterate through rules (in this case lhs)
        for lhs in self.lhs_to_rules:
            lhs_rules = self.lhs_to_rules[lhs]

            summed_prob = 0

            # 1. check that non-terminals are capital letters (in idx 1 of rule tuple)
            #   done by comparing nt to itself uppercased
            #       AND
            # 2. check that sum of probabilities is (approx) equal to 1.0
            for rule in lhs_rules:
                # add probability to sum for 2.
                summed_prob += rule[2]

                if len(rule[1]) < 2:
                    # use len to determine if nonterminal
                    for non_terminal in rule[1]:
                        if not non_terminal.isupper():
                            # if non terminal is not uppercase, return false
                            return False

            # if form is good, check for sum for 2.
            if not isclose(summed_prob, 1.0):
                return False       

        # if everything is fine, return True
        return True


if __name__ == "__main__":
    with open(sys.argv[1],'r') as grammar_file:
        grammar = Pcfg(grammar_file)

        if grammar.verify_grammar:
            print('Grammar is a valid PCFG in CNF.')
        else:
            print('Error: grammar is not well formed for the CKY parser.')
        
