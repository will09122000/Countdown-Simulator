"""
A simulated game of Countdown from a command-line interface.

This problem is broken down into 4 main functions detailed below:

The user is prompted 9 times to choose either a vowel or a consonant
using the letters 'v' and 'c' as inputs. A random letter depending on
their input is added to a list using the same probability distribution
from the Countdown show.  The 9 letters for this function will be
returned as a string.

A list of words is created from 'words.txt' with punctuation
removed and words less than 10 letters long. The argument for this
function is expected to be the name of a text file as a string. The
words will then be returned as a list.

The next function will take the 9 letter string and return two lists.
The first being all possible words that can be made from those 9
letters and the second being the longest words that can be made.

The last main function asks the user to input their best guess as
well as being given the chance to shuffle the letters. Their input
is checked against all possible words to see if there is a match. If
there is the program will print out: the number of points scored,
statistics on how 'good' their word was, if they scored maximum
points and lastly a list of the longest words.
"""

if __name__ == '__main__':

    # Used in the select_characters function to select a random letter
    # from either a list of vowels or consonents.
    import random

    # (Was) used for the 30 countdown second timer.
    # import time
    # Used to return all letter combinations of the 9 letter string.
    from itertools import combinations

    # Used to exit the program.
    import sys

    # Used to create ASCII art
    # https://bit.ly/314YbVX
    import pyfiglet

    # Threading used for a 30 second timer, didn't work in the python
    # shell so it has been commented out. https://bit.ly/2B2buvW
    # import threading


    def select_characters() -> str:
        """
        This function will ask the user if they would like a vowel of a
        consonant for their next letter and repeats 9 times. A vowel of
        consonant is randomly appended to the 'letters' list based on
        the following probability distribution:
        http://www.thecountdownpage.com/letters.htm
        """

        # 2D list of vowels and consonants each with a weighting.
        VOWELS = [['A', 15], ['E', 21], ['I', 13], ['O', 13], ['U', 5]]
        CONSONANTS = [['B', 2], ['C', 3], ['D', 6], ['F', 2], ['G', 3],
                      ['H', 2], ['J', 1], ['K', 1], ['L', 5], ['M', 4],
                      ['N', 8], ['P', 4], ['Q', 1], ['R', 9], ['S', 9],
                      ['T', 9], ['V', 1], ['W', 1], ['X', 1], ['Y', 1],
                      ['Z', 1]]

        def create_weighted_list(letter_type):
            """
            Function to define a list for both vowels and consonants
            that will contain repeated letters based on the
            probability distribution parameter using the lists above.
            """

            weighted_list = []
            # Repeat for the number of letters in the list.
            for counter, _ in enumerate(letter_type):
                # Repeat for the weighting of that individual number.
                # https://bit.ly/2LZlEUo
                for _ in range(letter_type[counter][1]):
                    weighted_list.append(letter_type[counter][0])
            # Returns the list with repeated letters to be used when
            # the user is selecting letters.
            return weighted_list

        vowels_weighted = create_weighted_list(VOWELS)
        consonants_weighted = create_weighted_list(CONSONANTS)

        letters = []
        # Instructions to user outside of loop so it's not repeated 9
        # or more times.
        print('\n' + 'Please enter \'v\' for vowel and \'c\' for', \
              'consonant 9 times.' + '\n')

        # While loop used to be able to change the number of iterations
        # as the loop is in progress to handle incorrect user
        # inputs.
        letter_count = 0
        while letter_count < 9:
            # Prompts user for an input and indicates their progress by
            # displaying the letter number.
            letter_type = input('Letter ' + str(letter_count+1)
                                + ' (\'v\' or \'c\'): ').lower()
            if letter_type == 'v':
                # Append a random element from the list of vowels to
                # the letters list.
                letter = (random.choice(vowels_weighted))
                letters.append(letter)
                # Removes the random letter from the weighted list
                # reducing the weighting of that letter.
                vowels_weighted.remove(letter)
                # Successful letter choice so i is incremented.
                letter_count += 1
                # Displays letters to the user has chosen so far in an
                # easy to read way, this has been done as the user's
                # next choice may be influenced by the result of
                # previous choices.
                print(' '.join(letters))

            # Same as above but for consonants.
            elif letter_type == 'c':
                letter = (random.choice(consonants_weighted))
                letters.append(letter)
                consonants_weighted.remove(letter)
                letter_count += 1
                print(' '.join(letters))
            # If the input is not 'v' or 'c'.
            else:
                print('Incorrect input, please enter the letter', \
                      '\'v\' for a vowel or the letter \'c\' for', \
                      'a consonant.')
                # To handle incorrect inputs the number of iterations
                # would have to increase by 1 each time in order to
                # still get 9 letters. I tried changing the number of
                # iterations in a for loop and realised from the source
                # below this was not possible so I chose to use a while
                # loop instead. https://bit.ly/2VpcIuA

        print('\n' + 'Calculating the longest possible words...', \
              '\n')
        # Returns the randomly selected letters as a string.
        return ''.join(letters)


    def dictionary_reader(file_name: str) -> list:
        """
        This function takes in a file name string argument, opens that
        file, iterates through each line removing punctuation,
        appending each line to a list if the word is less than 10
        letters and finally returns that list.
        """

        # Open the text file in read mode.
        with open(file_name, 'r') as txt_file:
            # Creates a list of all words in the text file.
            txt_list_all = txt_file.read().split('\n')
            # New list will have words with punctuation removed
            # from it and words less than 10 letters appended to it.
            txt_list_filtered = []
            # Repeat for the number of words in the unfiltered list.
            for _, word in enumerate(txt_list_all):
                # If the word includes a '-', remove it.
                word = word.replace('-', '').upper()
                # If the length of the word is less than 10.
                if len(word) < 10:
                    txt_list_filtered.append(word)
            #Returns the filterd list of words.
            return txt_list_filtered


    def word_lookup(string_lookup: str) -> list:
        """
        This function takes in a string argument of letters generated
        from 'select_characters' and checks if the letters in that
        string can be used to make any of the words in 'word.txt'
        shorter than 10 letters. All possible words and all longest
        words are returned in separate lists.
        """

        possible_words = []
        longest_words = []
        letter_combinations = []
        word_list_sorted = []

        # https://bit.ly/2oiBMYb
        # ca1-combinations-generator.py
        string_lookup_sorted = ''.join(sorted(string_lookup))
        # starting with the longest letter string count down to zero
        for i in range(len(string_lookup_sorted), 0, -1):
            # for each length of letter strings generate all possible
            # combinations
            for substring_letters_list in \
                combinations(string_lookup_sorted, i):
                # for each combination of letters convert list to
                # string
                substring_letters = ''.join(substring_letters_list)
                # Appends the combination to the list.
                letter_combinations.append(substring_letters)

        # Sorts letters in each word alphabetically and appends to an
        # empty list.
        for _, word in enumerate(WORD_LIST):
            word_list_sorted.append(''.join(sorted(word)))

        # Checks each word against each letter combination both of
        # which are sorted alphabetically. If there's a match, the
        # original word is appended to the 'possible_words' list.
        for counter0, word in enumerate(word_list_sorted):
            for _, combination in enumerate(letter_combinations):
                if combination == word:
                    possible_words.append(WORD_LIST[counter0])

        # Finds the length of the longest words in all possible words.
        best_word_len = len((max(possible_words, key=len)))

        # As there can be more than one longest word, this iterates
        # through each possible word to check if it's length is equal
        # to the longest word length and appends it to the
        # 'longest_word' list if it is.
        for _, word in enumerate(possible_words):
            if len(word) == best_word_len:
                longest_words.append(word)

        # Retuns both possible and longest words list as the possible
        # words list will be needed to check if the user's answer is
        # correct.
        return possible_words, longest_words


    def user_guess():
        """
        This function handles the user's best guess at the longest
        word, displays the longest words, tells the user how many
        points they scored and stats on how good their word was if
        their input was a valid word.
        """

        print(pyfiglet.figlet_format(' '.join(USER_LETTERS)))
        # The user is prompted for an answer and given the chance to
        # shuffle the the letters.
        answer = False
        while not answer:
            user_answer = input('Please enter the longest word you '
                                'can think of with the letters '
                                'above or press \'1\' to shuffle '
                                'the letters.' + '\n')
            if user_answer == '1':
                temp_letter_list = list(USER_LETTERS)
                random.shuffle(temp_letter_list)
                print(pyfiglet.figlet_format
                      (' '.join(temp_letter_list)))
            else:
                answer = True

        #timer.cancel()

        # If the word the user enters is one of the possible words, the
        # number of points they scored is calculated and displayed. The
        # user is also told how 'good' their word was with a percentage
        # and if their answer was one of the longest words possibe. If
        # the word is not found they score 0 points. The best words are
        # then displayed.
        if user_answer.upper() in possible_words:
            if len(user_answer) == 1:
                print('\n' + 'You scored ' + str(len(user_answer))
                      + ' point.')
            else:
                print('\n' + 'You scored ' + str(len(user_answer))
                      + ' points.')

            possible_words_sorted = (sorted(possible_words, key=len,
                                            reverse=True))
            # Dict used to remove duplicates from the set while
            # keeping the order of elements in the list.
            # https://stackoverflow.com/a/7961425
            for counter, word in \
            (enumerate(list(dict.fromkeys(possible_words_sorted)))):
                if user_answer.upper() == word.upper():
                    percentage = (counter / len(set(possible_words))
                                  * 100)
                    print('Your word was in the top '
                          + str(round(percentage, 1))
                          + '% of all possible words, the '
                          + str(ordinal(counter)) + ' best word.')

                if user_answer.upper() in longest_words:
                    print('Congratulations, you scored maximum', \
                          'points!')

        else:
            print(user_answer.upper() + ' is an incorrect word,', \
            'you scored 0 points.')
        if len(longest_words) < 2:
            print('\n' + 'The longest word was: ')
            for word in set(longest_words):
                print(word)
        else:
            print('\n' + 'The longest words were: ')
            for word in set(longest_words):
                print(word)


    # Both functions used for a 30 second timer, didn't work in the
    # python shell so it has been commented out.

    # def timer():
        """
        30 second timer while the user is thinking of the longest
        word.
        """

        # global timer
        # timer = threading.Timer(10.0, timer_up)
        # timer.start()

    # def timer_up():
        # print('\n' + 'You have ran out of time, you score 0 points.')

        # if len(longest_words) == 1:
            # print('\n' + 'The longest word is: ')
            # for word in set(longest_words):
                # print(word)
        # else:
            # print('\n' + 'The longest words are: ')
            # for word in set(longest_words):
                # print(word)


    def ordinal(numb):
        """
        Used in 'user_guess' function as a suffix to the position of
        their word in all possible words.
        https://stackoverflow.com/a/18670679
        """

        if numb < 20:
            if numb == 1:
                suffix = 'st'
            elif numb == 2:
                suffix = 'nd'
            elif numb == 3:
                suffix = 'rd'
            else:
                suffix = 'th'
        else:
            tens = str(numb)
            tens = tens[-2]
            unit = str(numb)
            unit = unit[-1]
            if tens == "1":
                suffix = "th"
            else:
                if unit == "1":
                    suffix = 'st'
                elif unit == "2":
                    suffix = 'nd'
                elif unit == "3":
                    suffix = 'rd'
                else:
                    suffix = 'th'
        return str(numb)+ suffix

    # Program title.
    print(pyfiglet.figlet_format('Countdown'))

    # Dictionary reader function only needs to run once no matter how
    # many times the user plays the game in one running of the program.
    WORD_LIST = dictionary_reader('words.txt')

    # Other functions will repeat until the user decides to quit which
    # is asked at the end of each round.
    replay = 'p'
    while replay == 'p':
        USER_LETTERS = select_characters()
        possible_words, longest_words = word_lookup(USER_LETTERS)
        user_guess()

        # Once a round has finished the user is asked if they want to
        # play again.
        replay = input('\n' + 'Press \'p\' to play again or press '
                       '\'q\' to exit the program' + '\n')

        # Program will exit.
        if replay == 'q':
            try:
                print(pyfiglet.figlet_format('Thanks for playing'))
            except:
                print('Thanks for playing')
            sys.exit()

        #If the input was unexpected, the question is asked again.
        elif replay != 'p':
            replay = input('\n' + 'Press \'p\' to play again or', \
                   'press \'q\' to exit the program' + '\n')
