#!/usr/bin/env python3
"""
Substitution Cipher Decryptor

Usage: python decrypt.py <inputfile>

This program reads an encrypted text file (using a substitution cipher),
attempts to decrypt it (assuming the plaintext is in English), and writes
the decrypted message to a new file. If the file has been processed before
(identified by its hash), the program retrieves the cached result.
"""

import os
import sys
import json
import hashlib
import random
import math

# ----- Utility Functions -----

def compute_file_hash(filename):
    """Compute SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def decrypt(ciphertext, key_mapping):
    """Apply a substitution key mapping to the ciphertext."""
    result = ""
    for char in ciphertext:
        if char.upper() in key_mapping:
            dec_char = key_mapping[char.upper()]
            # Preserve case
            result += dec_char if char.isupper() else dec_char.lower()
        else:
            result += char
    return result

# ----- Quadgram Scorer -----

class QuadgramScorer:
    """
    Scores text based on quadgram frequencies.
    If 'quadgrams.txt' exists in the same directory, it will be loaded.
    Otherwise, a minimal default dictionary is used.
    """
    def __init__(self, filename='quadgrams.txt'):
        self.quadgrams = {}
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) == 2:
                        self.quadgrams[parts[0]] = int(parts[1])
        else:
            # Minimal default quadgram dictionary (for demonstration)
            self.quadgrams = {
                "THEN": 10, "THER": 9, "TION": 8, "HERE": 7,
                "THAT": 7, "ATIO": 6, "NDTH": 5, "THEM": 5
            }
        self.total = sum(self.quadgrams.values())
        self.log_prob = {}
        for key in self.quadgrams:
            self.log_prob[key] = math.log10(float(self.quadgrams[key]) / self.total)
        self.floor = math.log10(0.01 / self.total)

    def score(self, text):
        """Score text by summing log probabilities of quadgrams."""
        # Remove spaces and convert to uppercase for scoring
        text = text.upper().replace(" ", "")
        score = 0
        for i in range(len(text) - 3):
            quad = text[i:i+4]
            if quad in self.log_prob:
                score += self.log_prob[quad]
            else:
                score += self.floor
        return score

# ----- Hill Climbing Algorithm -----

def hill_climb(ciphertext, scorer, max_iter=1000):
    """
    Performs hill climbing to find the best decryption key.
    Returns the best decryption text, its key mapping, and the score.
    """
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Start with a random key permutation.
    best_key = list(alphabet)
    random.shuffle(best_key)
    best_key = ''.join(best_key)
    best_mapping = {best_key[i]: alphabet[i] for i in range(26)}
    best_decryption = decrypt(ciphertext, best_mapping)
    best_score = scorer.score(best_decryption)

    current_key = best_key
    current_score = best_score

    for _ in range(max_iter):
        # Swap two random letters to generate a new candidate key.
        a, b = random.sample(range(26), 2)
        new_key_list = list(current_key)
        new_key_list[a], new_key_list[b] = new_key_list[b], new_key_list[a]
        new_key = ''.join(new_key_list)
        new_mapping = {new_key[i]: alphabet[i] for i in range(26)}
        new_decryption = decrypt(ciphertext, new_mapping)
        new_score = scorer.score(new_decryption)
        if new_score > current_score:
            current_key = new_key
            current_score = new_score
            if current_score > best_score:
                best_score = current_score
                best_key = current_key
    final_mapping = {best_key[i]: alphabet[i] for i in range(26)}
    return decrypt(ciphertext, final_mapping), final_mapping, best_score

def solve_substitution(ciphertext, scorer, restarts=20, iterations=1000):
    """
    Runs multiple hill climbing restarts to find the overall best decryption.
    """
    best_overall_score = -float('inf')
    best_overall_decryption = None
    best_overall_mapping = None
    for _ in range(restarts):
        decryption, mapping, score = hill_climb(ciphertext, scorer, iterations)
        if score > best_overall_score:
            best_overall_score = score
            best_overall_decryption = decryption
            best_overall_mapping = mapping
    return best_overall_decryption, best_overall_mapping, best_overall_score

# ----- Main Function -----

def main():
    if len(sys.argv) < 2:
        print("Usage: python decrypt.py <inputfile>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file + ".decrypted.txt"

    # Compute the hash of the input file.
    file_hash = compute_file_hash(input_file)

    # Load or initialize the cache.
    cache_filename = "decryption_cache.json"
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r') as f:
            cache = json.load(f)
    else:
        cache = {}

    # Check if the file was previously processed.
    if file_hash in cache:
        print("Cached result found for this file. Retrieving decryption...")
        result = cache[file_hash]
        decrypted_text = result["decrypted_text"]
    else:
        # Read the encrypted text from file.
        with open(input_file, 'r') as f:
            ciphertext = f.read().strip()

        # Create a quadgram scorer instance.
        scorer = QuadgramScorer()
        # Solve the substitution cipher.
        decrypted_text, mapping, score = solve_substitution(ciphertext, scorer, restarts=20, iterations=1000)
        # Save the result in the cache.
        cache[file_hash] = {
            "decrypted_text": decrypted_text,
            "mapping": mapping,
            "score": score
        }
        with open(cache_filename, 'w') as f:
            json.dump(cache, f, indent=4)
        print("Decryption completed.")

    # Write the decrypted text to the output file.
    with open(output_file, 'w') as f:
        f.write(decrypted_text)
    print("Decrypted text written to:", output_file)

if __name__ == '__main__':
    main()
