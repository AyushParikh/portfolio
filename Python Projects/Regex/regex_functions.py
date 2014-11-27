"""
# Copyright 2013 Nick Cheng, Brian Harrington, Danny Heap, Aidan Gomez 2014
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSC148, Winter 2014
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment

# Student code below this comment.


def is_regex(s):
    '''(str)->bool
    Determine whether the given string is a valid regex or not.

    >>> is_regex("0.1")
    False
    >>> is_regex("(0.1)")
    True
    >>> is_regex("((0|e)*********.1)")
    True
    >>> is_regex("((0|e)*********.1")
    False
    '''
    all_chars = ["0", "1", "2", "e", ".", "|", "*", ")", "("]
    uni_regex = ["0", "1", "2", "e"]
    operators = "|."
    l_b = 0
    r_b = 0
    center_i = None
    # make sure every character in s is valid
    for c in s:
        if c not in all_chars:
            return False
    # if s is simply a unary regex return true
    if s in uni_regex:
        return True
    # if the regex ends in a star check what is within it
    elif s[-1] == "*":
        try:
            return is_regex(s[:-1])
        except:
            return False
    # try to do the following, and if it fails anywhere, it is not a regex
    try:
        # look inside the first brackets, if the first half of the regex
        # has a bracket, start going through the first half
        s = s[1:-1]
        if s[0] == "(":
            for i, c in enumerate(s):
                # count left and right brackets, and when they are equal you
                # are either one away from the center or a star
                if c == "(":
                    l_b += 1
                elif c == ")":
                    r_b += 1
                if l_b == r_b:
                    center_i = i+1
                    # while it is at a star, keep moving forward
                    while s[center_i] == "*":
                        center_i = center_i+1
                    # if it stopped and is not an operator, then it
                    # must not be a regex
                    if not s[center_i] in operators:
                        return False
                    break
            # if the left brackets never equalled the right brackets then
            # center was not created and the string is not a regex
            if center_i is None:
                return False
            # check that both sides of the regex are valid
            if is_regex(s[:center_i]) and is_regex(s[center_i+1:]):
                return True
            else:
                return False
        # if there isn't a bracket in the first half the go through each
        # character until you find an operator. That must be the center.
        else:
            for i, c in enumerate(s):
                if c in operators:
                    r1 = s[:i]
                    r2 = s[i+1:]
                    # check the left and right sides of the regex for validity.
                    return is_regex(r1) and is_regex(r2)
    # if any failure arises, return False
    except:
        return False


def find_center_index(s):
    '''(str)->int
    find the center index of a string s such that "("+s+")" is equal to a regex.

    >>> find_center_index("(0.1).5")
    5
    >>> find_center_index("((0.1).5****)|e*********")
    12
    >>> find_center_index("0.(1*****.2*****************)")
    1
    '''
    operators = "|."
    l_b = 0
    r_b = 0
    # use the same process as is_regex to find center
    if s[0] == "(":
        for i, c in enumerate(s):
            if c == "(":
                l_b += 1
            elif c == ")":
                r_b += 1
            if l_b == r_b:
                center_i = i+1
                while s[center_i] == "*":
                    center_i = center_i+1
                break
        return center_i
    else:
        for i, c in enumerate(s):
            if c in operators:
                return i


def all_regex_permutations(s):
    '''(str)->set
    return the set of all permutations of regex s

    >>> all_regex_permutations("(0.1)")
    {(0.1), (1.0)}
    >>> all_regex_permutations("((e.1)|(e|(0.1)))")
    {'((e.1)|((0.1)|e))', '((1.e)|((0.1)|e))', '((e|(1.0))|(e.1))',
     '(((0.1)|e)|(1.e))', '((e.1)|((1.0)|e))', '(((0.1)|e)|(e.1))',
     '((1.e)|(e|(0.1)))', '(((1.0)|e)|(e.1))', '((e|(1.0))|(1.e))',
     '((e.1)|(e|(1.0)))', '((1.e)|(e|(1.0)))', '(((1.0)|e)|(1.e))',
     '((e|(0.1))|(1.e))', '((e.1)|(e|(0.1)))', '((e|(0.1))|(e.1))',
     '((1.e)|((1.0)|e))'}
    '''
    all_chars = ["0", "1", "2", "e", ".", "|", "*", ")", "("]
    uni_regex = ["0", "1", "2", "e", "0*", "1*", "2*", "e*"]
    operators = "|."
    # if s isn't a regex return an empty set
    if not is_regex(s):
        return set()
    perms = set()
    # add s to the set of permutation
    perms.add(s)
    # if s is a simple one char (+star) regex just return it
    if s in uni_regex:
        return perms
    # if there is a star at the end of the regex, permutate what is within is,
    # add a star to the end of each of those and add them to the set
    if s[-1] == "*":
        temp_perms = all_regex_permutations(s[:-1])
        for perm in temp_perms:
            perms.add(perm+"*")
    s_temp = s[1:-1]
    center_i = find_center_index(s_temp)
    center_c = s_temp[center_i]
    # if either side of the regex is a dot/bar regex get all permutations for
    # each and then add all combinations of them to the set
    if s_temp[0] == "(" or s_temp[-1] == ")":
        r1_perms = all_regex_permutations(s_temp[:center_i])
        r2_perms = all_regex_permutations(s_temp[center_i+1:])
        for perm1 in r1_perms:
            for perm2 in r2_perms:
                perms.add("("+perm1+center_c+perm2+")")
                perms.add("("+perm2+center_c+perm1+")")
    # otherwise, add the second permutation of the regex to the set
    else:
        s_perm = "("+s_temp[center_i+1:]+center_c+s_temp[:center_i]+")"
        perms.add(s_perm)
    return perms


def tree_to_regex(t):
    '''(RegexTree)->str
    Convert a valid regex tree into a regex string

    >>> tree_to_regex(Leaf("0"))
    '0'
    >>> tree_to_regex(StarTree(DotTree(Leaf("0"), BarTree(Leaf("e"), Leaf("1"))
                                       )))
    '(0.(e|1))*'
    '''
    uni_node = ["0", "1", "2", "e"]
    operators = "|."
    # if t is a unary regex return it
    if t.symbol in uni_node:
        return t.symbol
    # if t is a star regex, return the conversion of what is inside and
    # add a star to the end.
    elif t.symbol == "*":
        return tree_to_regex(t.children[0])+"*"
    # if it is an operator return the conversion of each side with the
    # symbol in the middle.
    elif t.symbol in operators:
        return "("+tree_to_regex(t.children[0]) + t.symbol + \
            tree_to_regex(t.children[1]) + ")"


def star_bar_check(r, s):
    '''(RegexTree, str)->bool
    Check that a regextree rooted at r that is a StarTree with a BarTree
    within matches the string s

    >>> a = StarTree(BarTree(Leaf("0"), Leaf("1")))
    >>> b = StarTree(BarTree(Leaf("e"), Leaf("1")))
    >>> star_bar_check(a, "01101010001")
    True
    >>> star_bar_check(a, "")
    True
    >>> star_bar_check(a, "2")
    False
    >>> star_bar_check(b, "111111")
    True
    >>> star_bar_check(b, "11e1eee1")
    False
    '''
    # if the s is simply one occurance of the tree return True
    if regex_match(r.children[0], s):
                return True
    s_temp = s
    for i in range(len(s)):
        # check each group of s to see if it can match with the tree
        if regex_match(r.children[0], s_temp[:i]):
            s_temp = s_temp[i:]
            # now check if the remaining letters can be made from the regex
            return star_bar_check(r, s_temp)
    # if no combination can be found return False
    return False


def regex_match(r, s):
    '''(RegexTree, str)->bool
    determine whether a RegexTree rooted at r could produce string s

    >>> a = BarTree(Leaf("0"), Leaf("1"))
    >>> b = StarTree(BarTree(DotTree(Leaf("e"), Leaf("2")), Leaf("1")))
    >>> regex_match(a, "")
    False
    >>> regex_match(a, "0")
    True
    >>> regex_match(a, "2")
    False
    >>> regex_match(b, "")
    True
    >>> regex_match(b, "2")
    True
    >>> regex_match(b, "e2")
    False
    '''
    # if r is a unary regex (excluding e) return whether it equals the string
    if r.symbol in "012":
        return r.symbol == s
    # if r is a unary e regex check that the string is empty
    elif r.symbol == "e":
        return s == ""
    # if r is a star regex
    if r.symbol == "*":
        # if s is empty it is valid
        if s == "":
            return True
        # if child is a unary e regex check that the string is empty
        if r.children[0].symbol == "e":
            return s == ""
        # if child is a unary regex check that every char in s is the symbol
        elif r.children[0].symbol in "012":
            for c in s:
                if r.children[0].symbol != c:
                    return False
            return True
        # if child is a dot regex
        elif r.children[0].symbol == ".":
            # is there is only one repition of the tree in s it must be valid
            if regex_match(r.children[0], s):
                return True
            # look for some sequence of characters that satisfies child and
            # repeats an integer number of times
            for i in range((len(s)//2)+1):
                if regex_match(r.children[0], s[:i]):
                    try:
                        int(len(s)/i)
                        if s[:i]*(len(s)//i) == s:
                            return True
                    except:
                        pass
            return False
        elif r.children[0].symbol == "|":
            return star_bar_check(r, s)
    # if r is a dot regex check every break point and try to find two halves of
    # the regex that will satisfy the addition of both children
    elif r.symbol == ".":
        for i in range(len(s)+1):
            l_s = s[:i]
            r_s = s[i:]
            if regex_match(r.children[0], l_s) and regex_match(r.children[1],
                                                               r_s):
                return True
        return False
    # if r is a bar matrix check that s satisfies at least 1 child of r
    elif r.symbol == "|":
        return regex_match(r.children[0], s) or regex_match(r.children[1], s)


def build_regex_tree(regex):
    '''(str)->RegexTree
    build a regextree from a string regex

    >>> build_regex_tree("(0.1)")
    DotTree(Leaf("0"), Leaf("1"))
    >>> build_regex_tree("((e.(1|0))|2)*")
    StarTree(BarTree(DotTree(Leaf("e"), BarTree(Leaf("1"), Leaf("0"))),
                     Leaf("2")))
    '''
    # check that regex is a regex
    if not is_regex(regex):
        return None
    uni_regex = ["0", "1", "2", "e"]
    # if the regex is a unary regex simply return a Leaf of regex
    if regex in uni_regex:
        return Leaf(regex)
    # if the regex ends in a star return a StarTree with the tree
    # representation of the inside of the star
    elif regex[-1] == "*":
        return StarTree(build_regex_tree(regex[:-1]))
    r_temp = regex[1:-1]
    center_i = find_center_index(r_temp)
    center_c = r_temp[center_i]
    # if the regex is a dot regex return the DotTree with the tree forms of
    # either side of regex
    if center_c == ".":
        return DotTree(build_regex_tree(r_temp[:center_i]),
                       build_regex_tree(r_temp[center_i+1:]))
    # if the regex is a bar regex return the BarTree with the tree forms of
    # either side of regex
    elif center_c == "|":
        return BarTree(build_regex_tree(r_temp[:center_i]),
                       build_regex_tree(r_temp[center_i+1:]))
