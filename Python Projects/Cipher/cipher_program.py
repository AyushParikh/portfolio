"""
Encrypt or decrypt the contents of a message file using a deck of cards.
"""

import cipher_functions

DECK_FILENAME = 'deck1.txt'
MSG_FILENAME = 'message1.txt'
MODE = 'e'  # 'e' for encryption, 'd' for decryption.


def main():
    """ () -> NoneType

    Perform the encryption using the deck from a file called DECK_FILENAME and
    the messages from a file called MSG_FILENAME. If MODE is 'e', encrypt;
    otherwise, decrypt.
    """
    # open the deck file and then run read_deck on it
    my_deck = open(DECK_FILENAME, 'r')
    deck = cipher_functions.read_deck(my_deck)
    # open the msg file and run read_messages on it
    my_messages = open(MSG_FILENAME, 'r')
    messages = cipher_functions.read_messages(my_messages)
    # process the messages that read read into a list and then print the
    # decrypted/encrypted messages
    list_of_messages = cipher_functions.process_messages(deck, messages, MODE)
    for i in range(0, len(list_of_messages)):
        print(list_of_messages[i])

main()
