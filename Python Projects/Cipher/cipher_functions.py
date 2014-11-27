"""
    Very basic encryption/decryption program using a cipher (deck of cards)
"""

# Functions for running an encryption or decryption.

# The values of the two jokers.
JOKER1 = 27
JOKER2 = 28

# Write your functions here:

# as opposed to putting this list over and over in each function I made it a
# global variable
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def clean_message(input_str):
    '''(str) -> str

    Convert string to all caps and remove all non-alpha characters

    >>> clean_message("adsfadsf")
    'ADSFADSF'
    >>> clean_message("Asjth54akljg53!248^%#$")
    'ASJTHAKLJG'
    '''
    # create an empty string-format result variable
    res = ""
    # check each letter of the input_str
    for i in range(0, len(input_str)):
        input_char = input_str[i]
        # if the character is a letter add it to the result variable
        if (input_char.isalpha()):
            res += input_char
            i += 1
        # if the character is anything other than a letter, ignore it
        else:
            i += 1
    # take the result variable about make all the letters uppercase and
    # return it
    res = res.upper()
    return res


def encrypt_letter(input_char, ks_char):
    ''' (str, int) -> str

    Take a letter and it's keystring and encrypt the character and return the
    encrypted result

    >>> encrypt_letter("A", 24)
    'Y'
    >>> encrypt_letter("B", 12)
    'N'
    '''
    # find the index of the character you are encrypting in the alphabet
    input_char = alphabet.index(input_char)
    # add that to the keystream value
    res = input_char + ks_char
    # if that is greater than 25 or the index of 'Z', the last letter of the
    # alphabet, then subtract 26 from it. This makes the alphabet circular or
    # modulo 26
    if (res > 25):
        res = res - 26
    # convert this number back into a letter and return it
    e_char = alphabet[res]
    return e_char


def decrypt_letter(input_char, ks_char):
    ''' (str, int) -> str

    Take a letter and it's keystring and encrypt the character and return the
    encrypted result

    >>> decrypt_letter("Y", 24)
    'A'
    >>> decrypt_letter("N", 12)
    'B'
    '''
    # find the index of the input_char in the alphabet
    input_char = alphabet.index(input_char)
    # subtract the keystream value from it
    res = input_char - ks_char
    # if the res is less than zero at 26, making the alphabet circular or
    # modulo 26
    if (res < 0):
        res = res + 26
    # convert this number back into a letter and return it
    d_char = alphabet[res]
    return d_char


def swap_cards(sc_deck, card_index):
    ''' (list of int, int) -> NoneType

    Swap the card at card_index of deck with the card following it

    >>> x = [0, 1, 2, 3, 4, 5]
    >>> swap_cards(x, 2)
    >>> x
    [0, 1, 3, 2, 4, 5]
    >>> x = [0, 1, 2, 3, 4,5]
    >>> swap_cards(x, 5)
    >>> x
    [5, 1, 2, 3, 4, 0]
    '''
    # create variable swap_card for the card that will be swapped with the
    # one following it
    swap_card = sc_deck[card_index]
    # because the deck needs to be looked at as circular, if the card index
    # is the last card in the deck then switch it with the first card
    if (card_index == len(sc_deck)-1):
        sc_deck[card_index] = sc_deck[0]
        sc_deck[0] = swap_card
    # otherwise swap the card with the one that follows it
    else:
        sc_deck[card_index] = sc_deck[card_index + 1]
        sc_deck[card_index + 1] = swap_card


def move_joker_1(j1_deck):
    ''' (list of int) -> NoneType

    Find the position of JOKER1 in the list and swap it with the following
    card

    >>> x = [0, 1, 2, 3, 4, 5, 6, 7, 27, 9]
    >>> move_joker_1(x)
    >>> x
    [0, 1, 2, 3, 4, 5, 6, 7, 9, 27]
    >>> x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 27]
    >>> move_joker_1(x)
    >>> x
    [27, 1, 2, 3, 4, 5, 6, 7, 8, 0]
    '''
    # find the index of where JOKER1 is
    joker_index = j1_deck.index(JOKER1)
    # apply swap_cards using the deck and the found index to move the JOKER1
    # back one position
    swap_cards(j1_deck, joker_index)


def move_joker_2(j2_deck):
    ''' (list of int) -> NoneType

    Find the position of JOKER2 in the list and swap it with the card two
    down from it

    >>> x = [0, 1, 2, 28]
    >>> move_joker_2(x)
    >>> x
    [1, 28, 2, 0]
    >>> x = [0, 1, 28, 3]
    >>> move_joker_2(x)
    >>> x
    [28, 1, 3, 0]
    '''
    # find the JOKER2's index and apply swap_cards to move it back once of the
    # two times necessary
    joker_index = j2_deck.index(JOKER2)
    swap_cards(j2_deck, joker_index)
    # find the new position of the JOKER2 and apply swap_cards to move it
    # back a second time completing the description of the function
    joker_index = j2_deck.index(JOKER2)
    swap_cards(j2_deck, joker_index)


def triple_cut(deck):
    '''(list of int) -> NoneType

    Find the two jokers and switch everything before the first with\
    everything behind the second

    >>> x = [1, 2, 3, 4, 27, 6, 7, 8, 28, 10, 11, 12]
    >>> triple_cut(x)
    >>> x
    [10, 11, 12, 27, 6, 7, 8, 28, 1, 2, 3, 4]
    >>> x = [1, 27, 28, 2]
    >>> triple_cut(x)
    >>> x
    [2, 27, 28, 1]
    '''
    # find the indexes of JOKER1 and JOKER2 and the length of the deck
    joker1_index = deck.index(JOKER1)
    joker2_index = deck.index(JOKER2)
    lendeck = len(deck)
    # if the JOKER1 comes first
    if (joker2_index > joker1_index):
        # add to the deck everything from JOKER2 (exclusive) to the end
        deck += deck[joker2_index+1:len(deck)]
        # add to the deck everything from JOKER1 to JOKER2 (inclusive)
        deck += deck[joker1_index:joker2_index+1]
        # add to the deck everything from the beginning to JOKER1 (exclusive)
        deck += deck[0:joker1_index]
        # delete the old deck by deleting the range up to the end of the deck
        # before anything was added to it
        del deck[:lendeck]
    # if the JOKER2 comes first
    elif (joker1_index > joker2_index):
        # add to the deck everything from JOKER1 (exclusive) to the end
        deck += deck[joker1_index+1:len(deck)]
        # add to the deck everything from JOKER2 to JOKER1 (inclusive)
        deck += deck[joker2_index:joker1_index+1]
        # add to the deck everything from the beginning to JOKER2 (exclusive)
        deck += deck[0:joker2_index]
        # delete the old deck by deleting the range up to the end of the deck
        # before anything was added to it
        del deck[:lendeck]


def insert_top_to_bottom(tb_deck):
    ''' (list of int) -> NoneType

    From the top, take the number of cards as the last card integer of
    the deck and place them behind the last card. If the last card is JOKER2
    then take JOKER1 cards from the top.

    >>> x = [1, 2, 3, 4, 6, 7, 5]
    >>> insert_top_to_bottom(x)
    >>> x
    [7, 1, 2, 3, 4, 6, 5]
    >>> x = [16, 1, 4, 7, 10, 19, 22, 13, 25, 28, 3, 6, 9, 12, 15, 18, 21, 24,\
             27, 5, 8, 11, 14, 17, 20, 23, 26, 2]
    >>> insert_top_to_bottom(x)
    >>> x
    [4, 7, 10, 19, 22, 13, 25, 28, 3, 6, 9, 12, 15, 18, 21, 24, 27, 5, 8, 11,\
 14, 17, 20, 23, 26, 16, 1, 2]
    '''
    # find the number to move by checking what integer value is at the bottom
    # of the deck and find the length of the deck
    num_to_move = tb_deck[len(tb_deck)-1]
    lendeck = len(tb_deck)
    # if the number to move is equal to the value of JOKER2
    if (num_to_move == JOKER2):
        # set the new num_to_move to the value of JOKER1
        num_to_move = JOKER1
        # add to the deck everything after the last card you will need to
        # move to the bottom of the deck
        tb_deck += tb_deck[num_to_move:lendeck-1]
        # add to the deck everything from the beginning to the last card you
        # will need to move. NOTE: despite :num_to_move being excluded,
        # because the deck starts at one it will still include all that are
        # being moved
        tb_deck += tb_deck[:num_to_move]
        # add to the deck the last card, in this case JOKER2
        tb_deck += [JOKER2]
        # delete the old deck by deleting the range up to the end of the deck
        # before anything was added to it
        del tb_deck[:lendeck]
    # if the number to move is anything other than JOKER2
    else:
        # add to the deck everything from the card after the last one that
        # will need to move to the end of the deck
        tb_deck += tb_deck[num_to_move:lendeck-1]
        # add to the deck everything from the beginning to the last card you
        # will need to move. NOTE: despite :num_to_move being excluded,
        # because the deck starts at one it will still include all that are
        # being moved
        tb_deck += tb_deck[:num_to_move]
        # add the card at the end of the deck
        tb_deck += [num_to_move]
        # delete the old deck by deleting the range up to the end of the deck
        # before anything was added to it
        del tb_deck[:lendeck]


def get_card_at_top_index(deck):
    ''' (list of int) -> int

    Take the integer value of the top card in the deck and go to that index
    in the deck. If the card you land on is a JOKER then continue the round
    at step 1. Otherwise, store this number as the keystream value for the
    round.

    >>> get_card_at_top_index([2,5,1,3,4,8,7,6]) #jokers are 8 and 7
    1
    >>> get_card_at_top_index([1,2,3,7,8])
    2
    '''
    # find the interger value of the top card
    card_on_top = deck[0]
    # if the top card is JOKER2
    if (card_on_top == JOKER2):
        # set the top card value to JOKER1 b/c the index of 28 is beyond the
        # end of the deck
        card_on_top = JOKER1
    # set the keystream value to the value of the card at the index of the
    # integer value of the card on top
    keystream_value = deck[card_on_top]
    # return the value of the keystream
    return keystream_value


def get_next_value(gv_deck):
    ''' (list of int) -> int

    Runs all 5 steps of the algorithm and returns the next potential
    keystream value

    >>> get_next_value([1, 4, 28, 10, 13, 16, 19, 22, 25, 26, 3, 6, 9, 12,15,\
                        18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20, 23, 7])
    25
    >>> get_next_value([1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 3, 6, 9, 12, 15,\
                        18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20, 23, 26])
    11
    '''
    # run all five steps of the algorithm
    # move the first joker back one
    move_joker_1(gv_deck)
    # move the second joker back two
    move_joker_2(gv_deck)
    # perform a triple cut on the deck
    triple_cut(gv_deck)
    # insert the number of cards from the top of the deck as the integer
    # value of the bottom card of the deck infront of the last card
    insert_top_to_bottom(gv_deck)
    # return the keystream value that results from all the steps
    return get_card_at_top_index(gv_deck)


def get_next_keystream_value(deck):
    ''' (list of int) -> int

    Use get_next_value repeatedly until an integer keystream value is found

    >>> get_next_keystream_value([1, 4, 28, 10, 13, 16, 19, 22, 25, 26, 3, 6,\
                        9, 12, 15, 18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20,\
                        23, 7])
    25
    >>> get_next_keystream_value([1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 3, 6,\
                        9, 12, 15, 18, 21, 24, 27, 2, 5, 8, 11, 14, 17, 20,\
                        23, 26])
    11
    '''
    # find your first keystream value for the deck
    next_value = get_next_value(deck)
    # while the next_value is equal to a JOKER value keep finding new
    # keystream values until it is not equal to a JOKER value
    while next_value == JOKER1 or next_value == JOKER2:
        next_value = get_next_value(deck)
    # return the non-JOKER keystream value
    return next_value


def process_message(pm_deck, message, command):
    ''' (list of int, str, str) -> str

    Take a deck, a message and the decrypt/encrypt command and return either
    a decrypted message or an encrypted one.

    >>> process_message([16, 1, 4, 7, 10, 19, 22, 13, 25, 28, 3, 6, 9, 12,\
    15, 18, 21, 24, 27, 5, 8, 11, 14, 17, 20, 23, 26, 2], 'A', 'e')
    'X'
    >>> process_message([16, 1, 4, 7, 10, 19, 22, 13, 25, 28, 3, 6, 9, 12,\
    15, 18, 21, 24, 27, 5, 8, 11, 14, 17, 20, 23, 26, 2], 'X', 'd')
    'A'
    '''
    # clean the inputted message and make an empty result variable and make
    # a index counter for the while statements
    message = clean_message(message)
    res = ""
    i = 0
    # if you are decrypting
    if (command == "d"):
        # run a while statement to decrypt each letter in the message
        while (i < len(message)):
            # use decrypt_letter to decrypt each letter of the message
            res += decrypt_letter(message[i], get_next_keystream_value
                                  (pm_deck))
            i += 1
    # if you are encrypting
    elif (command == "e"):
        # run a while statement to encrypt each letter in the message
        while (i < len(message)):
            # use encrypt_letter to encrypt each letter of the message
            res += encrypt_letter(message[i], get_next_keystream_value
                                  (pm_deck))
            i += 1
    # return the result variable
    return res


def process_messages(pms_deck, str_msgs, command):
    ''' (list of int, list of str, str) -> list of str

    Returns a list of encrypted of decrypted strings dependant on the command

    >>> process_messages([16, 1, 4, 7, 10, 19, 22, 13, 25, 28, 3, 6, 9, 12,\
    15, 18, 21, 24, 27, 5, 8, 11, 14, 17, 20, 23, 26, 2], ['DE','FG'],'e')
    ['AL', 'ZW']
    >>> process_messages([16, 1, 4, 7, 10, 19, 22, 13, 25, 28, 3, 6, 9, 12,\
    15, 18, 21, 24, 27, 5, 8, 11, 14, 17, 20, 23, 26, 2], ['AL','ZW'],'d')
    ['DE', 'FG']
    '''
    # make an empty list type result variable
    res = []
    # create a for statement to process each word in our list of words
    for i in range(0, len(str_msgs)):
        # add the result of process_message of each word in the list to
        # result list
        res += [process_message(pms_deck, str_msgs[i], command)]
    # return the result variable
    return res


def read_messages(filename):
    ''' (file open for reading) -> list of str

    Read and return each word of open file in the form of a list of str.
    '''
    # create an empty string type result variable
    res = ""
    # create a for statement checking each line of the open file
    for next_line in filename:
        # strip the file of newlines and turn it into one line of words
        clean_next_line = next_line.strip('\n')
        # add to the result variable the clean line with a space after it so
        # so that the last word of one line and the first of the next are not
        # blended into one word
        res += (clean_next_line+" ")
    # split this long line of words into a list with each index being a word
    res = res.split()
    # return the result variable
    return res


def read_deck(deck_filename):
    ''' (file open for reading) -> list of int

    Read and return the numbers in the file in a list of int.
    '''
    # create an empty list-type result variable
    res = []
    # create a for statement to check each line of the file
    for next_line in deck_filename:
        # add to the result variable the current line split into a list
        res += next_line.split()
        # use a for to change each element of the list into an integer value
        # instead of a string
        for i in range(0, len(res)):
            res[i] = int(res[i])
    # return the resulting list of integers we will use for our deck
    return res
