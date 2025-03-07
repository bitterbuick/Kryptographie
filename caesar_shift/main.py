import string
from collections import Counter
from itertools import permutations
try:
    import enchant
except ImportError:
    print("The 'enchant' library is not installed. Please install it using 'pip install pyenchant'.")
    exit(1)

def frequency_analysis(ciphertext):
    # Count letter frequencies in the ciphertext
    letter_counts = Counter(c for c in ciphertext if c in string.ascii_lowercase)
    sorted_letters = [pair[0] for pair in letter_counts.most_common()]
    return sorted_letters

def decrypt_with_shift(ciphertext, shift_map):
    # Replace letters based on the shift map
    return "".join(shift_map.get(c, c) for c in ciphertext)

def generate_shift_mappings(cipher_freq_order, english_freq_order):
    # Generate possible substitution mappings by aligning cipher letters to English letters
    for permutation in permutations(english_freq_order, len(cipher_freq_order)):
        yield {cipher_letter: plain_letter for cipher_letter, plain_letter in zip(cipher_freq_order, permutation)}

def is_valid_english(text, dictionary):
    # Check if the text contains valid English words
    words = text.split()
    valid_words = [word for word in words if dictionary.check(word)]
    return len(valid_words) / len(words) > 0.5 if words else False

def main():
    # Prompt user for ciphertext input
    ciphertext = input("Enter the encrypted text: ").strip().lower()

    # Frequency analysis and English letter order
    english_freq_order = "etaoinshrdlcumwfgypbvkjxqz"
    cipher_freq_order = frequency_analysis(ciphertext)

    # Initialize English dictionary
    dictionary = enchant.Dict("en_US")

    # Attempt decryption using frequency analysis and permutations
    for shift_map in generate_shift_mappings(cipher_freq_order, english_freq_order):
        plaintext = decrypt_with_shift(ciphertext, shift_map)
        if is_valid_english(plaintext, dictionary):
            print("Decrypted Text:")
            print(plaintext)
            return

    print("No valid decryption found.")

if __name__ == "__main__":
    main()
