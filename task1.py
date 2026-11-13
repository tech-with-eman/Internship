import random
import os

HANGMAN_STAGES = [
    """
       ------
       |    |
            |
            |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
            |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
            |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      /     |
            |
    ---------
    """,
    """
       ------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
    ---------
    """
]

def load_words(filename="words.txt", min_length=4):
    """Loads words from a text file, filtering out very short words or non-alphabetic entries."""
    if not os.path.exists(filename):
        # Fallback list in case words.txt isn't found
        return ["PYTHON", "DEVELOPER", "HANGMAN", "PROGRAMMING", "TERMINAL"]
    
    with open(filename, "r", encoding="utf-8") as file:
        words = [
            line.strip().upper()
            for line in file
            if line.strip().isalpha() and len(line.strip()) >= min_length
        ]
    return words

def get_masked_word(secret_word, guessed_letters):
    return " ".join([letter if letter in guessed_letters else "_" for letter in secret_word])

def play_hangman(word_list):
    print("========================================")
    print("       WELCOME TO TERMINAL HANGMAN      ")
    print("========================================")
    
    secret_word = random.choice(word_list)
    guessed_letters = set()
    incorrect_guesses = 0
    max_attempts = 6

    while incorrect_guesses < max_attempts:
        print(HANGMAN_STAGES[incorrect_guesses])
        print(f"Word: {get_masked_word(secret_word, guessed_letters)}")
        print(f"Guessed Letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
        print(f"Remaining Lives: {max_attempts - incorrect_guesses}")
        print("-" * 40)

        if all(letter in guessed_letters for letter in secret_word):
            print("\n🎉 CONGRATULATIONS! YOU WON! 🎉")
            print(f"The secret word was: {secret_word}")
            break

        guess = input("Guess a letter: ").strip().upper()

        if not guess or len(guess) != 1 or not guess.isalpha():
            print("❌ Invalid input. Please enter a single alphabetic letter.\n")
            continue

        if guess in guessed_letters:
            print(f"⚠️ You already guessed '{guess}'. No penalty incurred.\n")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"✅ Good job! '{guess}' is in the word.\n")
        else:
            incorrect_guesses += 1
            print(f"❌ Sorry, '{guess}' is not in the word.\n")

    else:
        print(HANGMAN_STAGES[max_attempts])
        print("\n💀 GAME OVER! YOU LOST! 💀")
        print(f"The secret word was: {secret_word}")

if __name__ == "__main__":
    words = load_words("words.txt", min_length=4)
    while True:
        play_hangman(words)
        replay = input("\nWould you like to play again? (y/n): ").strip().lower()
        if replay != 'y':
            print("Thanks for playing! Goodbye!")
            break
        print("\n" * 2)