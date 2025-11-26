import random
import re
import nltk
from nltk import pos_tag, word_tokenize, sent_tokenize
from nltk.parse import DependencyGraph

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger_eng')
except LookupError:
    nltk.download('averaged_perceptron_tagger_eng')


def identify_passive_voice(sentence):
    """
    Identify if a sentence is in passive voice
    Returns: (is_passive, auxiliary_verb, past_participle, subject, by_phrase)
    """
    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    
    # Look for passive voice pattern: form of "to be" + past participle (VBN)
    be_forms = ['is', 'are', 'was', 'were', 'be', 'been', 'being', 'am']
    
    for i in range(len(tags) - 1):
        word, tag = tags[i]
        if word.lower() in be_forms:
            # Check if next word is past participle
            if i + 1 < len(tags) and tags[i + 1][1] == 'VBN':
                # Try to find "by" phrase
                by_index = -1
                for j in range(i + 2, len(tags)):
                    if tags[j][0].lower() == 'by':
                        by_index = j
                        break
                
                return (True, i, i + 1, by_index, tokens, tags)
    
    return (False, None, None, None, None, None)


def passive_to_active(sentence):
    """
    Convert passive voice to active voice
    Example: "The ball was thrown by John" -> "John threw the ball"
    """
    result = identify_passive_voice(sentence)
    if not result[0]:
        return sentence
    
    _, be_index, participle_index, by_index, tokens, tags = result
    
    # If there's no "by" phrase, we can't easily convert to active
    if by_index == -1:
        return sentence
    
    try:
        # Extract components
        subject = tokens[:be_index]  # Original subject (becomes object)
        be_verb = tokens[be_index]
        participle = tokens[participle_index]
        middle = tokens[participle_index + 1:by_index]
        
        # Extract the agent (after "by")
        agent_end = len(tokens)
        for i in range(by_index + 1, len(tokens)):
            if tokens[i] in [',', '.', '!', '?', ';']:
                agent_end = i
                break
        
        agent = tokens[by_index + 1:agent_end]
        remainder = tokens[agent_end:]
        
        # Convert past participle to past tense verb
        verb_conversions = {
            'thrown': 'threw', 'written': 'wrote', 'taken': 'took',
            'given': 'gave', 'made': 'made', 'seen': 'saw',
            'done': 'did', 'gone': 'went', 'eaten': 'ate',
            'driven': 'drove', 'broken': 'broke', 'spoken': 'spoke',
            'chosen': 'chose', 'known': 'knew', 'grown': 'grew',
            'shown': 'showed', 'bought': 'bought', 'taught': 'taught',
            'caught': 'caught', 'brought': 'brought', 'thought': 'thought',
            'fought': 'fought', 'built': 'built', 'sent': 'sent',
            'spent': 'spent', 'lost': 'lost', 'found': 'found',
            'held': 'held', 'told': 'told', 'sold': 'sold'
        }
        
        active_verb = verb_conversions.get(participle.lower(), participle)
        
        # Reconstruct sentence: agent + verb + original subject + middle + remainder
        new_sentence = agent + [active_verb] + subject + middle + remainder
        
        # Capitalize first word
        if new_sentence:
            new_sentence[0] = new_sentence[0].capitalize()
        
        return ' '.join(new_sentence)
    
    except (IndexError, KeyError):
        return sentence


def active_to_passive(sentence):
    """
    Convert active voice to passive voice
    Example: "John threw the ball" -> "The ball was thrown by John"
    """
    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    
    # Find main verb (first verb that's not auxiliary)
    verb_index = -1
    for i, (word, tag) in enumerate(tags):
        if tag in ['VBD', 'VBP', 'VBZ', 'VB']:  # Past, present, base form
            verb_index = i
            break
    
    if verb_index == -1 or verb_index == 0:
        return sentence
    
    try:
        # Extract components
        subject = tokens[:verb_index]
        verb = tokens[verb_index]
        obj_and_rest = tokens[verb_index + 1:]
        
        # Find direct object (usually first noun/pronoun after verb)
        object_end = -1
        for i, (word, tag) in enumerate(pos_tag(obj_and_rest)):
            if tag.startswith('NN') or tag in ['PRP', 'PRP$']:
                # Find end of noun phrase
                for j in range(i + 1, len(obj_and_rest)):
                    if pos_tag([obj_and_rest[j]])[0][1] not in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'DT']:
                        object_end = j
                        break
                if object_end == -1:
                    object_end = len(obj_and_rest)
                break
        
        if object_end == -1:
            return sentence
        
        obj = obj_and_rest[:object_end]
        remainder = obj_and_rest[object_end:]
        
        # Convert verb to past participle
        participle_conversions = {
            'threw': 'thrown', 'wrote': 'written', 'took': 'taken',
            'gave': 'given', 'made': 'made', 'saw': 'seen',
            'did': 'done', 'went': 'gone', 'ate': 'eaten',
            'drove': 'driven', 'broke': 'broken', 'spoke': 'spoken',
            'chose': 'chosen', 'knew': 'known', 'grew': 'grown',
            'showed': 'shown', 'bought': 'bought', 'taught': 'taught',
            'caught': 'caught', 'brought': 'brought', 'thought': 'thought',
            'fought': 'fought', 'built': 'built', 'sent': 'sent',
            'spent': 'spent', 'lost': 'lost', 'found': 'found',
            'held': 'held', 'told': 'told', 'sold': 'sold'
        }
        
        participle = participle_conversions.get(verb.lower(), verb + 'ed')
        
        # Determine appropriate "be" verb based on tense
        be_verb = 'was'
        if tags[verb_index][1] == 'VBP' or tags[verb_index][1] == 'VBZ':
            be_verb = 'is'
        
        # Reconstruct: object + be + participle + remainder + by + subject
        new_sentence = obj + [be_verb, participle] + remainder + ['by'] + subject
        
        # Capitalize first word and ensure proper ending
        if new_sentence:
            new_sentence[0] = new_sentence[0].capitalize()
        
        return ' '.join(new_sentence)
    
    except (IndexError, KeyError):
        return sentence


def reorder_compound_sentence(sentence):
    """
    Reorder clauses in compound sentences
    Example: "I went to the store, and I bought milk" -> "I bought milk, and I went to the store"
    """
    # Common coordinating conjunctions
    conjunctions = [', and ', ', but ', ', or ', ', yet ', ', so ', ', nor ', '; however, ', '; moreover, ', '; therefore, ']
    
    for conj in conjunctions:
        if conj in sentence.lower():
            # Split on conjunction
            parts = re.split(re.escape(conj), sentence, maxsplit=1, flags=re.IGNORECASE)
            if len(parts) == 2:
                clause1, clause2 = parts
                
                # Remove ending punctuation from clause2 if present
                ending_punct = ''
                if clause2 and clause2[-1] in '.!?':
                    ending_punct = clause2[-1]
                    clause2 = clause2[:-1]
                
                # 50% chance to reorder
                if random.random() < 0.5:
                    # Capitalize appropriately
                    clause2 = clause2.strip().capitalize()
                    clause1 = clause1.strip().lower()
                    
                    # Reconstruct with clauses swapped
                    return f"{clause2}{conj}{clause1}{ending_punct}"
    
    return sentence


def vary_sentence_beginning(sentence):
    """
    Vary sentence beginnings by adding transitions or moving adverbs
    """
    sentence = sentence.strip()
    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    
    if len(tokens) < 4:
        return sentence
    
    # Transition words to add at the beginning
    transitions = {
        'addition': ['Furthermore', 'Moreover', 'Additionally', 'Also', 'Besides'],
        'contrast': ['However', 'Nevertheless', 'Nonetheless', 'Conversely', 'In contrast'],
        'result': ['Therefore', 'Thus', 'Consequently', 'As a result', 'Hence'],
        'example': ['For instance', 'For example', 'Specifically', 'In particular'],
        'time': ['Meanwhile', 'Subsequently', 'Previously', 'Initially'],
        'emphasis': ['Indeed', 'Certainly', 'Undoubtedly', 'Clearly']
    }
    
    # Check if sentence starts with subject-verb pattern
    if tags[0][1].startswith('NN') or tags[0][1] == 'PRP':
        # 30% chance to add a transition
        if random.random() < 0.3:
            category = random.choice(list(transitions.keys()))
            transition = random.choice(transitions[category])
            return f"{transition}, {sentence.lower()}"
    
    # Look for adverbs in the sentence (not at the beginning)
    for i in range(1, len(tags)):
        word, tag = tags[i]
        if tag == 'RB' and word.lower() not in ['not', "n't", 'very', 'too', 'so']:
            # Move adverb to the beginning
            if random.random() < 0.4:
                new_tokens = [word.capitalize()] + tokens[:i] + tokens[i+1:]
                # Ensure first word after adverb is lowercase (unless proper noun)
                if len(new_tokens) > 1 and tags[0][1] not in ['NNP', 'NNPS']:
                    new_tokens[1] = new_tokens[1].lower()
                return ', '.join([new_tokens[0], ' '.join(new_tokens[1:])])
    
    return sentence


def vary_sentence_structure(text, percent_reorder=40, percent_voice_change=20, 
                           percent_beginning_vary=30, ignore_quotes=True):
    """
    Apply various sentence structure variations to text
    
    :param text: Input text to modify
    :param percent_reorder: Percentage chance to reorder compound sentences
    :param percent_voice_change: Percentage chance to change voice (active/passive)
    :param percent_beginning_vary: Percentage chance to vary sentence beginnings
    :param ignore_quotes: Whether to ignore quoted text
    :return: Modified text with varied sentence structure
    """
    sentences = sent_tokenize(text)
    modified_sentences = []
    
    in_quotes = False
    
    for sentence in sentences:
        # Track quote state
        if '"' in sentence:
            quote_count = sentence.count('"')
            in_quotes = (quote_count % 2 != 0) if not in_quotes else not (quote_count % 2 != 0)
        
        # Skip if in quotes and ignore_quotes is True
        if ignore_quotes and '"' in sentence:
            modified_sentences.append(sentence)
            continue
        
        modified = sentence
        
        # Apply transformations based on probability
        
        # 1. Reorder compound sentences
        if random.randint(0, 100) < percent_reorder:
            modified = reorder_compound_sentence(modified)
        
        # 2. Change voice (active/passive)
        if random.randint(0, 100) < percent_voice_change:
            passive_result = identify_passive_voice(modified)
            if passive_result[0]:
                # It's passive, maybe convert to active
                if random.random() < 0.7:  # 70% chance to convert passive to active
                    modified = passive_to_active(modified)
            else:
                # It's active, maybe convert to passive
                if random.random() < 0.3:  # 30% chance to convert active to passive
                    modified = active_to_passive(modified)
        
        # 3. Vary sentence beginnings
        if random.randint(0, 100) < percent_beginning_vary:
            modified = vary_sentence_beginning(modified)
        
        modified_sentences.append(modified)
    
    return ' '.join(modified_sentences)


def combined_transformation(text, synonyms, adjectives, 
                           percent_synonyms=30, percent_reorder=40,
                           percent_voice_change=20, percent_beginning_vary=30,
                           percent_adjectives=60, ignore_quotes=True,
                           use_pos_filtering=True):
    """
    Apply both context-aware synonym replacement AND sentence structure variation
    
    This provides the most comprehensive text transformation by combining:
    - Context-aware synonym replacement
    - Sentence reordering
    - Voice changes (active/passive)
    - Varied sentence beginnings
    
    :param text: Input text to modify
    :param synonyms: Dictionary of word -> list of synonyms
    :param adjectives: List of adjectives for emphasis
    :param percent_synonyms: Percentage of words to replace with synonyms
    :param percent_reorder: Percentage chance to reorder compound sentences
    :param percent_voice_change: Percentage chance to change voice
    :param percent_beginning_vary: Percentage chance to vary sentence beginnings
    :param percent_adjectives: Percentage of adjectives to emphasize
    :param ignore_quotes: Whether to ignore quoted text
    :param use_pos_filtering: Whether to use POS-based synonym filtering
    :return: Fully transformed text
    """
    # Import here to avoid circular dependency
    from gptzzzs.context_aware_change import change_text_contextual
    
    # First apply sentence structure variations
    text_varied = vary_sentence_structure(
        text, 
        percent_reorder=percent_reorder,
        percent_voice_change=percent_voice_change,
        percent_beginning_vary=percent_beginning_vary,
        ignore_quotes=ignore_quotes
    )
    
    # Then apply context-aware synonym replacement
    final_text = change_text_contextual(
        text_varied,
        synonyms=synonyms,
        adjectives=adjectives,
        percent_synonyms=percent_synonyms,
        ignore_quotes=ignore_quotes,
        percent_adjectives=percent_adjectives,
        use_pos_filtering=use_pos_filtering
    )
    
    return final_text
