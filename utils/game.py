import re
import random
from .hangman_pics import HANGMANPICS
from .colors import bcolors
from typing import List

class Hangman:
    """
    A class who's purpose is to be able to play a game of Hangman, a game where 
    the player tries to guess each letter of the word that is hidden with a limited set of lives.
    """
    possible_words: List[str] = ['becode', 'learning', 'mathematics', 'sessions']

    def __init__(self):
        """
        Constructor with all the attributes setup so you can play the game 
        without any problems
        """
        self.word_to_find: str = random.choice(Hangman.possible_words)

        # Do not touch this variable or else problem will arise upon showing the hangman drawing
        self._lives: int = 6
        self._correctly_guessed_letters: List[str] = []
        self._wrongly_guessed_letters: List[str] = []
        self._turn_count: int = 0
        self._error_count: int = 0
        self._hidden_word: str = self.hide_word(self.word_to_find)

    def start_game(self):
        """
        Start the game of Hangman by looping through the game's data such as 
        the letters of the word, the list of correctly guessed and wrongly guessed 
        words, the lives, the errors and the turn count.
        The function will call other functions to play the game and show a 
        winning text or game over text.
        """
        while self._lives > 0 and self._hidden_word != self.word_to_find:
            print(HANGMANPICS[self._error_count])
            print(' '.join(self._hidden_word) + "\n")
            print(f"{bcolors.OKGREEN}Correctly guessed: {self._correctly_guessed_letters}{bcolors.ENDC}")
            print(f"{bcolors.FAIL}Wrongly guessed: {self._wrongly_guessed_letters}{bcolors.ENDC}")
            print(f"{bcolors.BOLD}Lives: {self._lives}")
            print(f"Error(s): {self._error_count}")
            print(f"Turn(s): {self._turn_count}{bcolors.ENDC}")
            self.play()

        if self._hidden_word == self.word_to_find:
            self.well_played()
        elif self._lives == 0:
            self.game_over()
    
    def play(self):
        """
        Asks the player to input a single letter and verifies if the letter is conform 
        if not the user is asked again until it is.
        After the checks if correctly guessed, the letter is then revealed at its right place 
        and added to the correctly guessed list.
        If it is wrongly guessed then the player loses a life, has its error count incremented and 
        has its letter appear in the wrongly guessed list.
        """
        letter = input(f"{bcolors.BOLD}Please enter a single letter...: {bcolors.ENDC}").lower().strip()
        if len(letter) == 1 and letter.isalpha():
            if letter not in self._correctly_guessed_letters and letter not in self._wrongly_guessed_letters:
                self._turn_count += 1
                if re.search(letter, self.word_to_find):
                    self._correctly_guessed_letters += letter
                    # This for loop is used to replace the underscore(s)(hidden word)
                    # with the letter(s) at the right index
                    for m in re.finditer(f"[{letter}]", self.word_to_find):
                        self._hidden_word = self._hidden_word[:m.start()] + letter + self._hidden_word[m.start()+1:]   
                else:
                    self._error_count += 1
                    self._lives -= 1
                    self._wrongly_guessed_letters.append(letter)
            else:
                print(f"{bcolors.WARNING}Please do not input a letter that you have already guessed.{bcolors.ENDC}\n")
                return self.play()
        else:
            print(f"{bcolors.WARNING}Wrong input!!\n{bcolors.ENDC}")
            return self.play()

    def game_over(self):
        """
        Print the game over screen with the word so the player knows what was/were the missing letter(s).
        """
        print(HANGMANPICS[self._error_count])
        print(f"The word was: {self.word_to_find}")
        print(f"{bcolors.BOLD}{bcolors.FAIL}game over...{bcolors.ENDC}")

    def well_played(self):
        """
        Print the winning screen with the data of the game.
        """
        print(f"{bcolors.OKGREEN}\nYou found the word: {bcolors.BOLD}{self.word_to_find}{bcolors.ENDC}{bcolors.OKGREEN}, in {self._turn_count} turns with {self._error_count} errors!{bcolors.ENDC}")

    def hide_word(self, word_to_hide: str):
        """
        Hide the obtained word with underscores with the same number of characters.
        This is only used to get a clearer view of the hidden word.
        :param word_to_hide: The string that has to be hidden.
        :return: The obtained string hidden by underscores and spaced.
        """
        hidden_word = ""
        for char in word_to_hide:
            if char == '-':
                hidden_word += char
            else:    
                hidden_word += "_"
        return hidden_word
