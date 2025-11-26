import random
import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


def get_wordnet_pos(treebank_tag):
    """
    Convert Penn Treebank POS tags to WordNet POS tags
    """
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return None


def filter_synonyms_by_pos(word, synonyms, pos_tag):
    """
    Filter synonyms to match the part of speech of the original word
    """
    if not synonyms:
        return []
    
    wn_pos = get_wordnet_pos(pos_tag)
    if wn_pos is None:
        return synonyms
    
    filtered = []
    for syn in synonyms:
        # Check if synonym exists in WordNet with the same POS
        synsets = wn.synsets(syn.lower(), pos=wn_pos)
        if synsets:
            filtered.append(syn)
    
    # If filtering removed all synonyms, return original list
    return filtered if filtered else synonyms


def should_skip_word(word, pos_tag):
    """
    Determine if a word should be skipped (proper nouns, acronyms, etc.)
    """
    # Skip proper nouns
    if pos_tag in ['NNP', 'NNPS']:
        return True
    
    # Skip if all uppercase (likely acronym)
    if word.isupper() and len(word) > 1:
        return True
    
    # Skip very short words
    if len(word) <= 2:
        return True
    
    return False


def separate_punctuation(word):
    """
    Separate word from surrounding punctuation
    Returns: (prefix_punct, clean_word, suffix_punct)
    """
    import re
    match = re.match(r'^(\W*)(\w+)(\W*)$', word)
    if match:
        return match.groups()
    return ('', word, '')


def rank_synonyms_by_context(original, synonyms, pos_tag):
    """
    Rank synonyms by their contextual similarity to the original word
    Prefers synonyms with similar characteristics
    """
    if not synonyms:
        return synonyms
    
    scored_synonyms = []
    original_len = len(original)
    
    for syn in synonyms:
        score = 0
        
        # Prefer similar length (more likely to be similar register/formality)
        length_diff = abs(len(syn) - original_len)
        score += max(0, 10 - length_diff)
        
        # Prefer words that share starting letters (often related)
        if syn[0].lower() == original[0].lower():
            score += 2
        
        # Slight preference for shorter words (usually more common)
        if len(syn) < original_len:
            score += 1
        
        scored_synonyms.append((score, syn))
    
    # Sort by score (descending) and return synonyms
    scored_synonyms.sort(reverse=True, key=lambda x: x[0])
    return [syn for _, syn in scored_synonyms]


def change_text_contextual(text, synonyms, adjectives, percent_synonyms=50, 
                          ignore_quotes=True, percent_adjectives=60, use_pos_filtering=True):
    """
    Context-aware text modification using POS tagging
    
    :param text: Input text to modify
    :param synonyms: Dictionary of word -> list of synonyms
    :param adjectives: List of adjectives for emphasis
    :param percent_synonyms: Percentage of words to replace
    :param ignore_quotes: Whether to ignore quoted text
    :param percent_adjectives: Percentage of adjectives to emphasize
    :param use_pos_filtering: Whether to use POS-based synonym filtering
    :return: Modified text
    """
    
    # Tokenize and tag the text
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    
    # Calculate how many words to change
    num_to_change = int(len(tokens) * percent_synonyms / 100)
    
    # Track which indices we'll change
    changeable_indices = []
    for i, (word, tag) in enumerate(pos_tags):
        if not should_skip_word(word, tag):
            changeable_indices.append(i)
    
    # Randomly select indices to change
    if len(changeable_indices) > num_to_change:
        indices_to_change = set(random.sample(changeable_indices, num_to_change))
    else:
        indices_to_change = set(changeable_indices)
    
    # First pass: Replace synonyms with context awareness
    modified_tokens = []
    in_quotes = False
    
    for i, (token, tag) in enumerate(pos_tags):
        # Track quote state
        if '"' in token:
            in_quotes = not in_quotes
        
        # Skip if in quotes and ignore_quotes is True
        if in_quotes and ignore_quotes:
            modified_tokens.append(token)
            continue
        
        # Check if this word should be changed
        if i in indices_to_change:
            prefix, word, suffix = separate_punctuation(token)
            word_lower = word.lower()
            
            # Check if word has synonyms
            if word_lower in synonyms and synonyms[word_lower]:
                available_synonyms = synonyms[word_lower]
                
                # Filter synonyms by POS if enabled
                if use_pos_filtering:
                    available_synonyms = filter_synonyms_by_pos(
                        word_lower, available_synonyms, tag
                    )
                
                # Rank synonyms by contextual similarity
                if available_synonyms:
                    ranked_synonyms = rank_synonyms_by_context(
                        word_lower, available_synonyms, tag
                    )
                    
                    # Choose from top-ranked synonyms (add some randomness)
                    top_n = min(3, len(ranked_synonyms))
                    chosen_synonym = random.choice(ranked_synonyms[:top_n])
                    
                    # Preserve capitalization
                    if word[0].isupper():
                        chosen_synonym = chosen_synonym.capitalize()
                    
                    modified_tokens.append(prefix + chosen_synonym + suffix)
                else:
                    modified_tokens.append(token)
            else:
                modified_tokens.append(token)
        else:
            modified_tokens.append(token)
    
    # Reconstruct text with proper spacing
    result = []
    for i, token in enumerate(modified_tokens):
        result.append(token)
        # Add space after token unless it's punctuation
        if i < len(modified_tokens) - 1:
            next_token = modified_tokens[i + 1]
            if not next_token[0] in '.,!?;:)\'"':
                result.append(' ')
    
    text_after_synonyms = ''.join(result)
    
    # Second pass: Add emphasis to adjectives
    tokens = word_tokenize(text_after_synonyms)
    pos_tags = pos_tag(tokens)
    
    modified_tokens = []
    emphasis_words = ["very", "really", "extremely", "quite", "so", "incredibly"]
    in_quotes = False
    skip_next = False
    
    for i, (token, tag) in enumerate(pos_tags):
        if skip_next:
            skip_next = False
            continue
            
        # Track quote state
        if '"' in token:
            in_quotes = not in_quotes
        
        # Skip if in quotes and ignore_quotes is True
        if in_quotes and ignore_quotes:
            modified_tokens.append(token)
            continue
        
        prefix, word, suffix = separate_punctuation(token)
        word_lower = word.lower()
        
        # Check if current word is an emphasis word before an adjective
        if (word_lower in emphasis_words and 
            i + 1 < len(pos_tags) and 
            pos_tags[i + 1][1].startswith('JJ')):
            # Randomly remove emphasis words
            if random.randint(0, 100) < percent_adjectives:
                skip_next = False
                modified_tokens.append(pos_tags[i + 1][0])
                skip_next = True
                continue
        
        # Check if word is an adjective (JJ, JJR, JJS)
        if tag.startswith('JJ') and word_lower in adjectives:
            # Randomly add emphasis
            if random.randint(0, 100) < percent_adjectives:
                emp_word = random.choice(emphasis_words)
                modified_tokens.append(emp_word)
                modified_tokens.append(token)
                continue
        
        modified_tokens.append(token)
    
    # Reconstruct final text
    result = []
    for i, token in enumerate(modified_tokens):
        result.append(token)
        if i < len(modified_tokens) - 1:
            next_token = modified_tokens[i + 1]
            if not next_token[0] in '.,!?;:)\'"':
                result.append(' ')
    
    return ''.join(result)
