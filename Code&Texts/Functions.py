import math
from collections import Counter
import os # allows interaction with the operating system, needed for extracting filenames
import txt_formatter

def analyse(text,language='english'):

    filename = os.path.basename(text)
    base_name = os.path.splitext(filename)[0]
    results = {}
    results['file_name'] = base_name
    
    text = txt_formatter.format_txt(text) # (txt_format function written in seperate file)
    for a in range(1,3):
        if a == 1:
            analysis_level = 'word'
        if a == 2:
            analysis_level = 'phoneme'
        # Tokenize based on the specified analysis level
        if analysis_level == 'word':
            tokens = text.split()
        elif analysis_level == 'phoneme':
    
            # Language-specific phoneme mappings, use International Phonetic Alphabet (IPA) to formalise phonemes
            if language == 'latin':
                phoneme_map = {
                    # Latin diphthongs and special sequences
                    'ae': 'aɪ', 'oe': 'ɔɪ', 'au': 'aʊ', 'eu': 'ɛʊ',
                    'ei': 'eɪ', 'ui': 'ʊɪ',
                    
                    # Consonant combinations
                    'ch': 'kʰ', 'ph': 'f', 'th': 'tʰ', 'rh': 'r',
                    'qu': 'kw', 'gu': 'gw', 'ng': 'ŋg',
                    'bs': 'ps', 'bt': 'pt',
                    
                    # Single vowels (Classical Latin pronunciation)
                    'a': 'a', 'e': 'ɛ', 'i': 'ɪ', 'o': 'ɔ', 'u': 'ʊ', 'y': 'y',
                    
                    # Consonants
                    'b': 'b', 'c': 'k', 'd': 'd', 'f': 'f', 'g': 'g',
                    'h': 'h', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm',
                    'n': 'n', 'p': 'p', 'q': 'k', 'r': 'r', 's': 's',
                    't': 't', 'v': 'w', 'x': 'ks', 'z': 'z',
                    
                    # Double consonants (geminated)
                    'bb': 'bː', 'cc': 'kː', 'dd': 'dː', 'ff': 'fː', 'gg': 'gː',
                    'll': 'lː', 'mm': 'mː', 'nn': 'nː', 'pp': 'pː', 'rr': 'rː',
                    'ss': 'sː', 'tt': 'tː'
                }
            else:  # English
                phoneme_map = {
                    # Vowels and diphthongs
                    'ee': 'i', 'ea': 'i', 'ie': 'i', 'ei': 'i', 'ey': 'i',
                    'oo': 'u', 'oa': 'oʊ', 'oe': 'oʊ',
                    'ai': 'eɪ', 'ay': 'eɪ', 
                    'ou': 'aʊ', 'ow': 'aʊ', 
                    'oy': 'ɔɪ', 'oi': 'ɔɪ',
                    'au': 'ɔ', 'aw': 'ɔ',
                    'igh': 'aɪ', 
                    'ough': 'ʌf', 'augh': 'æf',
                    
                    # R-controlled vowels
                    'ar': 'ɑr', 'er': 'ər', 'ir': 'ər', 'or': 'ɔr', 'ur': 'ər',
                    'ear': 'ɪr', 'eer': 'ɪr',
                    
                    # Consonants and digraphs
                    'th': 'θ', 'sh': 'ʃ', 'ch': 'tʃ', 'ph': 'f', 
                    'wh': 'w', 'ck': 'k', 'ng': 'ŋ', 'qu': 'kw',
                    'kn': 'n', 'gn': 'n', 'wr': 'r', 'rh': 'r',
                    'gh': '', 'dg': 'dʒ', 'tch': 'tʃ',
                    
                    # Single letters (approximate IPA)
                    'a': 'æ', 'e': 'ɛ', 'i': 'ɪ', 'o': 'ɑ', 'u': 'ʌ',
                    'y': 'j', 
                    'b': 'b', 'c': 'k', 'd': 'd', 'f': 'f', 'g': 'g',
                    'h': 'h', 'j': 'dʒ', 'k': 'k', 'l': 'l', 'm': 'm',
                    'n': 'n', 'p': 'p', 'q': 'k', 'r': 'r', 's': 's',
                    't': 't', 'v': 'v', 'w': 'w', 'x': 'ks', 'z': 'z'
                }
            
            # Process text by replacing patterns
            phoneme_text = text
            
            # sorts patterns by length to prioritize longer matches, so shorter patterns within longer ones don't get replaced first
            for pattern, phoneme in sorted(phoneme_map.items(), key=lambda x: -len(x[0])):
                if len(pattern) > 1:
                    phoneme_text = phoneme_text.replace(pattern, f" {phoneme} ")
            
            # Process single characters
            words = phoneme_text.split()
            tokens = []
            
            for word in words:
                i = 0
                while i < len(word):
                    matched = False
                    # Try to match patterns of decreasing length
                    for length in [4, 3, 2, 1]:
                        if i + length <= len(word):
                            segment = word[i:i+length]
                            if segment in phoneme_map:
                                tokens.append(phoneme_map[segment])
                                i += length
                                matched = True
                                break
                    
                    if not matched:
                        # If no match, keep the character (handles punctuation that slipped through)
                        if word[i].isalpha():
                            tokens.append(word[i])
                        i += 1
            
            tokens = [p for p in tokens if p and p.strip()] # clean list of phonemes, removing empty strings and spaces
        else:
            raise ValueError("analysis_level must be 'word' or 'phoneme'")
        
        # Count frequencies
        token_counts = Counter(tokens)  
        total_tokens = len(tokens)
        
        # Calculate entropy
        def shannon_entropy(token_counts, total_tokens, normalise=False):
            entropy = 0.0
            for count in token_counts.values(): # e.g. {'cat': 1, 'dog': 1, 'the': 1, 'tricked': 1}
                if count > 0:  # Avoid log(0) errors
                    probability = count / total_tokens
                    entropy -= probability * math.log2(probability)
            
            if normalise and len(token_counts) > 1: # entropy normalised to [0,1], 0 means no uncertainty, 1 means maximum uncertainty
                max_entropy = math.log2(len(token_counts))
                entropy = entropy / max_entropy
            
            return entropy, dict(token_counts)

        # Calculate entropy for the specified analysis level
        entropy, freq_dist = shannon_entropy(token_counts, total_tokens)

        def phoneme_redundancy(freq_dist):
            total_tokens = sum(freq_dist.values())
            most_frequent = max(freq_dist.values())
            return most_frequent / total_tokens if total_tokens > 0 else 0
        
        def redundancy_ratio(entropy, freq_dist):
            if len(freq_dist) > 1:
                max_entropy = math.log2(len(freq_dist))
                return 1 - (entropy / max_entropy)
            return 0


        if analysis_level == 'word':
            results['word_entropy'] = entropy
            results['word_entropy_normalised'] = shannon_entropy(token_counts, total_tokens, normalise=True)[0]
            results['word_types'] = len(freq_dist)
            results['word_tokens'] = sum(freq_dist.values())
            results['type_token_ratio'] = results['word_types'] / results['word_tokens'] if results['word_tokens'] > 0 else 0
            # Average word length calculation
            total_chars = sum(len(word) * count for word, count in freq_dist.items())
            results['avg_word_length'] = total_chars / results['word_tokens'] if results['word_tokens'] > 0 else 0
            HLR_count = Counter(freq_dist.values())[1]
            results['Hapax_Legomena_Ratio(HLR)'] = HLR_count / results['word_types'] if results['word_types'] > 0 else 0 #counts words that appear only once
            results['word_redundancy_ratio'] = redundancy_ratio(entropy, freq_dist)

        elif analysis_level == 'phoneme':
            results['phoneme_entropy'] = entropy
            results['phoneme_entropy_normalised'] = shannon_entropy(token_counts, total_tokens, normalise=True)[0]
            results['phoneme_types'] = len(freq_dist)   
            results['phoneme_tokens'] = sum(freq_dist.values()) 
            # TTR irrelevant: if phoneme_types > max because phoneme_tokens rises while phoneme_types plateaus, only useful in the first few hundred phonemes texts
            results['phoneme_redundancy'] = phoneme_redundancy(freq_dist)
            results['phoneme_redundancy_ratio'] = redundancy_ratio(entropy, freq_dist)

    return results

