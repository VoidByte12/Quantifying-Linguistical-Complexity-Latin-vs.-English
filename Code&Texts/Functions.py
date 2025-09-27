import math
from collections import Counter
import os # allows interaction with the operating system, needed for extracting filenames
import txt_formatter

def analyse(text, analysis_level='word'):

    filename = os.path.basename(text)
    base_name = os.path.splitext(filename)[0]
    results = {}
    results['file_name'] = base_name
    
    text = txt_formatter.format_txt(text) # (txt_format function written in seperate file)
    
    # Tokenize based on the specified analysis level
    if analysis_level == 'word':
        tokens = text.split()
    elif analysis_level == 'phoneme':
        # For phoneme-level analysis, we analyze characters
        tokens = list(text.replace(' ', '').replace('-', ''))  # Remove spaces & hyphens for character-level analysis
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
        
        # NORMALIZATION EXPLANATION:
        # When normalize=True, we scale the entropy to a 0-1 range
        # where 0 = completely predictable (only one unique unit)
        # and 1 = maximum possible unpredictability for the given vocabulary size
        if normalise and len(token_counts) > 1:
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
        results['word_entropy_normalized'] = shannon_entropy(token_counts, total_tokens, normalise=True)[0]
        results['word_types'] = len(freq_dist)
        results['word_tokens'] = sum(freq_dist.values())
        results['type_token_ratio'] = results['word_types'] / results['word_tokens'] if results['word_tokens'] > 0 else 0
        # Average word length calculation
        total_chars = sum(len(word) * count for word, count in freq_dist.items())
        results['avg_word_length'] = total_chars / results['word_tokens'] if results['word_tokens'] > 0 else 0
        HLR_count = Counter(freq_dist.values())[1]
        results['Hapax Legomena Ratio(HLR)'] = HLR_count / results['word_types'] if results['word_types'] > 0 else 0 #counts words that appear only once
        results['word_redundancy_ratio'] = redundancy_ratio(entropy, freq_dist)

    elif analysis_level == 'phoneme':
        results['phoneme_entropy'] = entropy
        results['phoneme_entropy_normalized'] = shannon_entropy(token_counts, total_tokens, normalise=True)[0]
        results['phoneme_types'] = len(freq_dist)   
        results['phoneme_tokens'] = sum(freq_dist.values())
        # TTR irrelevant: if phoneme_types > max because phoneme_tokens rises while phoneme_types plateaus, only useful in the first few hundred phonemes texts
        results['phoneme_redundancy'] = phoneme_redundancy(freq_dist)
        results['phoneme_redundancy_ratio'] = redundancy_ratio(entropy, freq_dist)

    return results

