import importlib.resources as resources
import json
import urllib.request

from gptzzzs.normal_change import change_text
from gptzzzs.context_aware import change_text_contextual
from gptzzzs.sentence_variation import vary_sentence_structure, combined_transformation


class Gptzzzs:
    percent_synonyms = 50
    ignore_quotes = True
    percent_adjectives = 60
    synonym_list = "finnlp"
    custom_synonyms = None
    custom_adjectives = None

    def __init__(self):
        """
        Load synonym, adjective, and common word files
        """

        with open(str(resources.files("gptzzzs").joinpath('data/finnlp-together.json')), "r") as f:
            self.finnlp_together = json.load(f)

        with open(str(resources.files("gptzzzs").joinpath('data/finnlp-separate.json')), "r") as f:
            self.finnlp_separate = json.load(f)

        with open(str(resources.files("gptzzzs").joinpath('data/common_words.json')), "r") as f:
            self.common_words = json.load(f)

        with open(str(resources.files("gptzzzs").joinpath('data/adjectives.json')), "r") as f:
            self.adjectives = json.load(f)

        with open(str(resources.files("gptzzzs").joinpath('data/zaibacu.json')), "r") as f:
            self.zaibacu = json.load(f)

    def basic_change_text(self, text, synonym_list="finnlp", percent_synonyms=50, ignore_quotes=True,
                          percent_adjectives=60, common_words=False, adjective_list="normal"):
        """
        Changes text very simply by replacing words with synonyms and emphasizing adjectives.
        Does not use AI or any advanced techniques.

        :param text: the text to be changed
        :param synonym_list: the list of synonyms to use (finnlp, zaibacu, custom)
        :param percent_synonyms: the percentage of words to change (if possible)
        :param ignore_quotes: whether to ignore words in quotes
        :param percent_adjectives: the percentage of adjectives to change emphasization on
        :param common_words: whether to only use common words
        :param adjective_list: the list of adjectives to use (normal, custom)
        :return: the changed text
        """

        if synonym_list == "finnlp":
            synonyms = self.finnlp_together
        elif synonym_list == "zaibacu":
            synonyms = self.zaibacu
        elif synonym_list == "custom" and self.custom_synonyms is None:
            raise ValueError("Custom synonyms not set")
        elif synonym_list == "custom":
            synonyms = self.custom_synonyms
        else:
            raise ValueError("Invalid synonym list")

        if adjective_list == "normal":
            adjectives = self.adjectives
        elif adjective_list == "custom" and self.custom_adjectives is None:
            raise ValueError("Custom adjectives not set")
        elif adjective_list == "custom":
            adjectives = self.custom_adjectives
        else:
            raise ValueError("Invalid adjective list")

        if common_words:
            synonyms = {word: synonyms[word] for word in synonyms if word in self.common_words}

        return change_text(text, synonyms, adjectives, percent_synonyms, ignore_quotes, percent_adjectives)

    def contextual_change_text(self, text, synonym_list="finnlp", percent_synonyms=30, ignore_quotes=True,
                              percent_adjectives=60, common_words=False, adjective_list="normal",
                              use_pos_filtering=True):
        """
        Changes text using context-aware synonym replacement with POS tagging.
        This method produces more natural results by considering word context.

        :param text: the text to be changed
        :param synonym_list: the list of synonyms to use (finnlp, zaibacu, custom)
        :param percent_synonyms: the percentage of words to change (if possible) - default 30% for better quality
        :param ignore_quotes: whether to ignore words in quotes
        :param percent_adjectives: the percentage of adjectives to change emphasization on
        :param common_words: whether to only use common words
        :param adjective_list: the list of adjectives to use (normal, custom)
        :param use_pos_filtering: whether to filter synonyms by part of speech
        :return: the changed text
        """

        if synonym_list == "finnlp":
            synonyms = self.finnlp_together
        elif synonym_list == "zaibacu":
            synonyms = self.zaibacu
        elif synonym_list == "custom" and self.custom_synonyms is None:
            raise ValueError("Custom synonyms not set")
        elif synonym_list == "custom":
            synonyms = self.custom_synonyms
        else:
            raise ValueError("Invalid synonym list")

        if adjective_list == "normal":
            adjectives = self.adjectives
        elif adjective_list == "custom" and self.custom_adjectives is None:
            raise ValueError("Custom adjectives not set")
        elif adjective_list == "custom":
            adjectives = self.custom_adjectives
        else:
            raise ValueError("Invalid adjective list")

        if common_words:
            synonyms = {word: synonyms[word] for word in synonyms if word in self.common_words}
            synonyms = {word: syn_list for word, syn_list in synonyms.items() if word in self.common_words and syn_list}

        return change_text_contextual(text, synonyms, adjectives, percent_synonyms, 
                                     ignore_quotes, percent_adjectives, use_pos_filtering)

    def advanced_change_text(self, text, synonym_list="finnlp", percent_synonyms=30,
                            percent_reorder=40, percent_voice_change=20, 
                            percent_beginning_vary=30, ignore_quotes=True,
                            percent_adjectives=60, common_words=False, 
                            adjective_list="normal", use_pos_filtering=True):
        """
        Most advanced text transformation combining context-aware synonyms AND sentence structure variation.
        This method provides the highest quality output by:
        - Reordering clauses in compound sentences
        - Converting between active and passive voice
        - Varying sentence beginnings with transitions
        - Using context-aware synonym replacement with POS tagging

        :param text: the text to be changed
        :param synonym_list: the list of synonyms to use (finnlp, zaibacu, custom)
        :param percent_synonyms: the percentage of words to change (if possible) - default 30%
        :param percent_reorder: percentage chance to reorder compound sentences (default 40%)
        :param percent_voice_change: percentage chance to change voice active/passive (default 20%)
        :param percent_beginning_vary: percentage chance to vary sentence beginnings (default 30%)
        :param ignore_quotes: whether to ignore words in quotes
        :param percent_adjectives: the percentage of adjectives to change emphasization on
        :param common_words: whether to only use common words
        :param adjective_list: the list of adjectives to use (normal, custom)
        :param use_pos_filtering: whether to filter synonyms by part of speech
        :return: the changed text with varied sentence structure
        """

        if synonym_list == "finnlp":
            synonyms = self.finnlp_together
        elif synonym_list == "zaibacu":
            synonyms = self.zaibacu
        elif synonym_list == "custom" and self.custom_synonyms is None:
            raise ValueError("Custom synonyms not set")
        elif synonym_list == "custom":
            synonyms = self.custom_synonyms
        else:
            raise ValueError("Invalid synonym list")

        if adjective_list == "normal":
            adjectives = self.adjectives
        elif adjective_list == "custom" and self.custom_adjectives is None:
            raise ValueError("Custom adjectives not set")
        elif adjective_list == "custom":
            adjectives = self.custom_adjectives
        else:
            raise ValueError("Invalid adjective list")

        if common_words:
            synonyms = {word: synonyms[word] for word in synonyms if word in self.common_words}
            synonyms = {word: syn_list for word, syn_list in synonyms.items() if word in self.common_words and syn_list}

        return combined_transformation(
            text, synonyms, adjectives,
            percent_synonyms=percent_synonyms,
            percent_reorder=percent_reorder,
            percent_voice_change=percent_voice_change,
            percent_beginning_vary=percent_beginning_vary,
            percent_adjectives=percent_adjectives,
            ignore_quotes=ignore_quotes,
            use_pos_filtering=use_pos_filtering
        )

    def vary_structure_only(self, text, percent_reorder=40, percent_voice_change=20,
                           percent_beginning_vary=30, ignore_quotes=True):
        """
        Apply only sentence structure variations without synonym replacement.
        Useful if you want to maintain vocabulary but change sentence patterns.

        :param text: the text to be changed
        :param percent_reorder: percentage chance to reorder compound sentences
        :param percent_voice_change: percentage chance to change voice active/passive
        :param percent_beginning_vary: percentage chance to vary sentence beginnings
        :param ignore_quotes: whether to ignore quoted text
        :return: text with varied sentence structure
        """
        return vary_sentence_structure(
            text,
            percent_reorder=percent_reorder,
            percent_voice_change=percent_voice_change,
            percent_beginning_vary=percent_beginning_vary,
            ignore_quotes=ignore_quotes
        )

    def custom_synonyms_from_url(self, url):
        """
        Loads custom synonyms from a URL

        Must be in JSON format with the word as the key and a list of synonyms as the value
        """

        response = urllib.request.urlopen(url)
        synonyms = json.loads(response.read().decode('utf-8'))
        self.custom_synonyms = synonyms

    def custom_adjectives_from_url(self, url):
        """
        Loads custom adjectives from a URL

        Must be an array of adjectives
        """

        response = urllib.request.urlopen(url)
        adjectives = json.loads(response.read().decode('utf-8'))
        self.custom_adjectives = adjectives

    def custom_synonyms_from_file(self, path):
        """
        Loads custom synonyms from a file

        Must be in JSON format with the word as the key and a list of synonyms as the value
        """

        with open(path, "r") as f:
            synonyms = json.load(f)
        self.custom_synonyms = synonyms

    def custom_adjectives_from_file(self, path):
        """
        Loads custom adjectives from a file

        Must be an array of adjectives
        """

        with open(path, "r") as f:
            adjectives = json.load(f)
        self.custom_adjectives = adjectives

    def custom_synonyms_from_dict(self, synonyms):
        """
        Loads custom synonyms from a dictionary

        Must be in JSON format with the word as the key and a list of synonyms as the value
        """

        self.custom_synonyms = synonyms

    def custom_adjectives_from_list(self, adjectives):
        """
        Loads custom adjectives from a list

        Must be an array of adjectives
        """

        self.custom_adjectives = adjectives