#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRYPTANALYSE EXHAUSTIVE - Système Enigma-like
Force brute sur s (ordre rotors) et key (décalages initiaux)
"""

from itertools import permutations, product
import time

# Configuration exacte des rotors
C1_orig = ["b", "n", "v", "c", "x","'", "z", "l", "k", "j", "h", "g", "f", "d", "s", "q", "m", "u", "i", "e","è", "a", "r", "t", "y", "p", "w"," ", "o","é"]
C2_orig = ["q", "x", "e", "z", "r", "n", "m", "u", "a", "l","h", "t", "b", "s","'","è", "w", "v", "i", "y", "f", " ", "j", "g", "p", "k", "d","é", "o", "c"]
C3_orig = ["j", "x", "b", "e", "m", "l", "z", "y", "g", "h", "s"," ", "p", "w", "v","é", "i", "q","'", "u","è", "o", "r", "f", "d", "t", "n", "c", "a", "k"]
C4_orig = ["o", "q"," ", "t", "a", "c", "j", "d", "m", "g", "b", "h", "x", "u", "l", "w","è", "e", "n", "p", "y", "s", "k","'", "r","é", "z", "v", "f", "i"]
C5_orig = ["f", "r", "b", "w", "z","è", "x","é" ,"j", "k", "i", "m", "t", "y", "o", "g", "s"," ", "l", "v", "q", "c", "u","'", "e", "h", "p", "a", "d", "n"]
C6_orig = ["r", "b", "w", "z", "x", "j", "k", "i", "m", "t", "y","'", "o", "g","é", "s", "l", "v", " ","q", "c","è", "u", "e", "h", "p", "a", "d", "n","f"]
Reflector = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ","'","é","è"]
Reflector2 = ['y', 'r', 'u', 'h', 'q', 's', 'l', 'd', 'p', 'x', 'n', 'g', 'o', 'k', 'm', 'i', 'e', 'b', 'f', 'z', 'c', 'w',"v", 'j', 'a', 't',"'"," ","è","é"]

# Vecteurs de test pour validation
TEST_VECTORS = [
    ("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
     "fieiwz ilwdwf'nwezgt cgéyesbèrgocjémymfoolvzmqnshsbè'tunfqlvhzjnnfjxrtzvlokvrriévnxrskwespn hfrub"),
    
    ("abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz ab",
     "ffyèpilumpgrgviuujoax f'avpbsqmqrusdzéèlèhqdb'bcfdskmèugnknspyduuépwlfvézédajsgkins"),
    
    ("aaaaaaaaaaaaaaaaaaaaaaaaaaa",
     "fieiwz ilwdwf'nwezgt cgéyes"),
]

# Flag à déchiffrer
ENCRYPTED_FLAG = "jgfouypefldyhzllbpbséklpnwsu niuzkvgmfba qbzdbypibbcnzfsléljgfr dyglbéoénhdhhépdvékiffznkynftèqpyxo"

def parator(letter, variation):
    """Localise une lettre dans une séquence"""
    for index, char in enumerate(variation):
        if char == letter:
            return index
    return None

def encrypt(message, C1, C2, C3, C4, C5, C6, s, key):
    """Moteur de chiffrement complet"""
    # Copie des rotors
    C1 = list(C1)
    C2 = list(C2)
    C3 = list(C3)
    C4 = list(C4)
    C5 = list(C5)
    C6 = list(C6)
    
    # Initialisation des rotors avec key
    C1 = C1[-key[0]:] + C1[:-key[0]] if key[0] else C1
    C2 = C2[-key[1]:] + C2[:-key[1]] if key[1] else C2
    C3 = C3[-key[2]:] + C3[:-key[2]] if key[2] else C3
    
    rotors = [C1, C2, C3, C4, C5, C6]
    result = ""
    
    for char in message:
        if char not in Reflector:
            continue
        
        # Chemin forward à travers les rotors
        idx = parator(char, Reflector)
        char = rotors[s[0]-1][idx]
        
        for i in range(1, 6):
            idx = parator(char, rotors[s[i-1]-1])
            char = rotors[s[i]-1][idx]
        
        # Passage au réflecteur
        idx = parator(char, rotors[s[5]-1])
        char = Reflector2[idx]
        
        # Chemin backward à travers les rotors
        idx = parator(char, Reflector2)
        char = Reflector[idx]
        
        for i in range(5, -1, -1):
            idx = parator(char, Reflector if i == 5 else rotors[s[i+1]-1])
            char = rotors[s[i]-1][idx]
        
        idx = parator(char, rotors[s[0]-1])
        char = Reflector[idx]
        
        result += char
        
        # Rotation des rotors
        C1.append(C1.pop(0))
        if len(result) % 26 == 0:
            C2.append(C2.pop(0))
        if len(result) % (26 * 26) == 0:
            C3.append(C3.pop(0))
    
    return result

def validate_candidate(s, key):
    """Valide une paire (s, key) contre tous les vecteurs"""
    for plain, expected in TEST_VECTORS:
        try:
            result = encrypt(plain, C1_orig, C2_orig, C3_orig, C4_orig, C5_orig, C6_orig, s, key)
            if result != expected:
                return False
        except:
            return False
    return True

def main():
    print("=" * 70)
    print("CRYPTANALYSE - SYSTÈME ENIGMA-LIKE")
    print("=" * 70)
    print(f"[*] Vecteurs de test: {len(TEST_VECTORS)}")
    print(f"[*] Espace de recherche: 6! × 30^3 = {720 * (30**3):,} combinaisons")
    print()
    
    start_time = time.time()
    count = 0
    found = False
    
    # Génération de toutes les permutations de rotors
    rotor_perms = list(permutations([1, 2, 3, 4, 5, 6]))
    key_candidates = list(product(range(30), repeat=3))
    
    print(f"[*] Permutations de rotors: {len(rotor_perms)}")
    print(f"[*] Combinaisons de clés: {len(key_candidates)}")
    print()
    
    for s_candidate in rotor_perms:
        for key_candidate in key_candidates:
            count += 1
            
            if count % 500000 == 0:
                elapsed = time.time() - start_time
                rate = count / elapsed
                print(f"[*] Testées {count:,} combinaisons ({rate:.0f} tests/s)...")
            
            if validate_candidate(s_candidate, key_candidate):
                elapsed = time.time() - start_time
                print(f"\n{'=' * 70}")
                print(f"[✓] SOLUTION TROUVÉE EN {elapsed:.2f} SECONDES!")
                print(f"{'=' * 70}")
                print(f"[✓] s (ordre des rotors): {list(s_candidate)}")
                print(f"[✓] key (décalages): {list(key_candidate)}")
                print()
                
                # Déchiffrage du flag
                decrypted = encrypt(ENCRYPTED_FLAG, C1_orig, C2_orig, C3_orig, C4_orig, C5_orig, C6_orig, s_candidate, key_candidate)
                print(f"[✓] FLAG DÉCRYPTÉ:")
                print(f"    {decrypted}")
                print(f"{'=' * 70}")
                found = True
                break
        
        if found:
            break
    
    if not found:
        elapsed = time.time() - start_time
        print(f"\n[-] Aucune solution trouvée après {count:,} tests ({elapsed:.2f}s)")

if __name__ == "__main__":
    main()
