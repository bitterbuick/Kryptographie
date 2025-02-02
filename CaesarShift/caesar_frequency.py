#!/usr/bin/env python3
"""
Script: caesar_frequency.py
Purpose: Decrypt a Caesar cipher by first determining the shift by use of frequency analysis.
Usage: python3 caesar_frequency.py <encrypted_file>

English Letter Frequencies are based on:
  1. Kucera, H., & Francis, W. N. (1967). Computational Analysis of Present-Day American English.
  2. Norvig, P. (2009). How to Write a Spelling Corrector. Retrieved from http://norvig.com/spell-correct.html
  3. Wikipedia: Letter Frequency. Retrieved from https://en.wikipedia.org/wiki/Letter_frequency
"""

import sys
import string

ENGLISH_FREQ = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
    'z': 0.074
}

def normalize_text(text):
    """
    Converts the input text to lowercase.
    
    Parameters:
        text (str): The text to be normalized.
        
    Returns:
        str: The lowercase version of the text.
    """
    return text.lower()

def caesar_decrypt(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            base = ord('a')
            plaintext += chr((ord(char) - base - shift) % 26 + base)
        else:
            plaintext += char
    return plaintext

def chi_squared_score(text):
    filtered_text = "".join(filter(str.isalpha, text.lower()))
    if len(filtered_text) == 0:
        return float('inf')
    
    letter_counts = {letter: 0 for letter in string.ascii_lowercase}
    for char in filtered_text:
        if char in letter_counts:
            letter_counts[char] += 1

    chi_sq = 0.0
    total = len(filtered_text)
    for letter in string.ascii_lowercase:
        observed = letter_counts[letter]
        expected = ENGLISH_FREQ[letter] / 100 * total
        if expected > 0:
            chi_sq += (observed - expected) ** 2 / expected
    return chi_sq

def main():
    if len(sys.argv) != 2:
        print("Usage: {} <encrypted_file>".format(sys.argv[0]))
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            ciphertext = file.read().strip()
    except IOError as e:
        print("Error reading file '{}': {}".format(filename, e))
        sys.exit(1)
    
    # Normalize the ciphertext to lowercase
    ciphertext = normalize_text(ciphertext)
    
    best_shift = None
    best_score = float('inf')
    best_plaintext = ""
    for shift in range(26):
        candidate = caesar_decrypt(ciphertext, shift)
        score = chi_squared_score(candidate)
        if score < best_score:
            best_score = score
            best_shift = shift
            best_plaintext = candidate
    
    print("Frequency Analysis Decryption:")
    print("Determined Shift: {:2d}".format(best_shift))
    print("Chi-squared Score: {:.2f}".format(best_score))
    print("Decrypted Message:")
    print(best_plaintext)

if __name__ == "__main__":
    main()
