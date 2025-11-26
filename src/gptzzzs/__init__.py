

import importlib.resources as resources
import json
import urllib.request

from gptzzzs.normal_change import change_text
from gptzzzs.context_aware import change_text_contextual
from gptzzzs.sentence_variation import vary_sentence_structure, combined_transformation
from gptzzzs.docx_modifier import modify_docx as modify_docx_file
from gptzzzs.docx_modifier import modify_docx_from_gptzzzs as modify_docx_from_gptzzzs_file
from gptzzzs.ollama_humanize import humanize_with_ollama, humanize_with_ollama_streaming
from gptzzzs.docx_processor import process_docx, batch_process_docx, process_docx_with_progress




class Gptzzzs:
    percent_synonyms = 50
    ignore_quotes = True
    percent_adjectives = 60
    synonym_list = "finnlp"
    custom_synonyms = None
    custom_adjectives = None
    ollama_url = "http://localhost:11434"
    ollama_model = "gpt-oss:120b-cloud"

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



    def set_ollama_config(self, url=None, model=None):
        """
        Configure Ollama connection settings.
        
        :param url: the URL of the Ollama API
        :param model: the default model to use
        """
        if url:
            self.ollama_url = url
        if model:
            self.ollama_model = model


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

    def modify_docx_from_gptzzzs(self, input_path, synonym_list="finnlp",
                                 percent_synonyms=30, ignore_quotes=True,
                                 percent_adjectives=60, common_words=False,
                                 adjective_list="normal", use_pos_filtering=True):
        """
        Convenience function to modify a DOCX using this Gptzzzs instance.

        :param input_path: Path to the input DOCX file
        :param synonym_list: the list of synonyms to use (finnlp, zaibacu, custom)
        :param percent_synonyms: the percentage of words to change
        :param ignore_quotes: whether to ignore words in quotes
        :param percent_adjectives: the percentage of adjectives to emphasize
        :param common_words: whether to only use common words
        :param adjective_list: the list of adjectives to use (normal, custom)
        :param use_pos_filtering: whether to filter synonyms by part of speech
        :return: Path to the output file
        """
        
        return modify_docx_from_gptzzzs_file(
            input_path=input_path,
            gptzzzs_instance=self,
            synonym_list=synonym_list,
            percent_synonyms=percent_synonyms,
            ignore_quotes=ignore_quotes,
            percent_adjectives=percent_adjectives,
            use_pos_filtering=use_pos_filtering
        )

    def modify_docx(self, input_path, synonym_list="finnlp",
                    percent_synonyms=30, ignore_quotes=True,
                    percent_adjectives=60, common_words=False,
                    adjective_list="normal", use_pos_filtering=True):
        """
        Convenience function to modify a DOCX using this Gptzzzs instance.

        :param input_path: Path to the input DOCX file
        :param synonym_list: the list of synonyms to use (finnlp, zaibacu, custom)
        :param percent_synonyms: the percentage of words to change
        :param ignore_quotes: whether to ignore words in quotes
        :param percent_adjectives: the percentage of adjectives to emphasize
        :param common_words: whether to only use common words
        :param adjective_list: the list of adjectives to use (normal, custom)
        :param use_pos_filtering: whether to filter synonyms by part of speech
        :return: Path to the output file
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
            synonyms = {word: syn_list for word, syn_list in synonyms.items() if
                        word in self.common_words and syn_list}

        return modify_docx_file(
            input_path=input_path,
            synonyms=synonyms,
            adjectives=adjectives,
            percent_synonyms=percent_synonyms,
            ignore_quotes=ignore_quotes,
            percent_adjectives=percent_adjectives,
            use_pos_filtering=use_pos_filtering
        )
    

    def humanize_with_ai(self, text, model=None, temperature=0.7, max_tokens=2000, streaming=False, callback=None):
        """
        Uses Ollama to humanize text by making it sound more natural and less AI-generated.
        
        :param text: the text to be humanized
        :param model: the Ollama model to use (default: uses self.ollama_model)
        :param temperature: controls randomness (0.0-1.0, higher = more creative)
        :param max_tokens: maximum number of tokens in the response
        :param streaming: whether to use streaming output
        :param callback: optional callback function for streaming mode
        :return: the humanized text
        """
        model = model or self.ollama_model
        
        if streaming:
            return humanize_with_ollama_streaming(
                text, 
                model=model, 
                ollama_url=self.ollama_url,
                temperature=temperature,
                max_tokens=max_tokens,
                callback=callback
            )
        else:
            return humanize_with_ollama(
                text,
                model=model,
                ollama_url=self.ollama_url,
                temperature=temperature,
                max_tokens=max_tokens
            )
        

    def combined_humanize(self, text, use_synonyms=True, use_ai=True, 
                         synonym_list="finnlp", percent_synonyms=50, 
                         ignore_quotes=True, percent_adjectives=60,
                         common_words=False, adjective_list="normal",
                         model=None, temperature=0.7, max_tokens=2000):
        """
        Combines basic text changes with AI humanization for best results.
        
        :param text: the text to be humanized
        :param use_synonyms: whether to apply synonym replacement first
        :param use_ai: whether to apply AI humanization
        :param synonym_list: the list of synonyms to use
        :param percent_synonyms: the percentage of words to change
        :param ignore_quotes: whether to ignore words in quotes
        :param percent_adjectives: the percentage of adjectives to change
        :param common_words: whether to only use common words
        :param adjective_list: the list of adjectives to use
        :param model: the Ollama model to use
        :param temperature: controls AI randomness
        :param max_tokens: maximum tokens in AI response
        :return: the humanized text
        """
        result = text
        
        if use_synonyms:
            result = self.basic_change_text(
                result,
                synonym_list=synonym_list,
                percent_synonyms=percent_synonyms,
                ignore_quotes=ignore_quotes,
                percent_adjectives=percent_adjectives,
                common_words=common_words,
                adjective_list=adjective_list
            )
        
        if use_ai:
            result = self.humanize_with_ai(
                result,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
        
        return result


    def process_document(self, input_path, model=None, temperature=0.7, max_tokens=2000, 
                        preserve_formatting=True, progress_callback=None):
        """
        Process a DOCX file to humanize text while preserving formatting.
        
        :param input_path: path to the input docx file
        :param model: the Ollama model to use (default: uses self.ollama_model)
        :param temperature: controls randomness (0.0-1.0)
        :param max_tokens: maximum tokens per request
        :param preserve_formatting: whether to preserve text formatting
        :param progress_callback: optional callback function(current, total, message)
        :return: path to the output file (filename_edited.docx)
        """
        model = model or self.ollama_model
        
        if progress_callback:
            return process_docx_with_progress(
                input_path=input_path,
                ollama_model=model,
                ollama_url=self.ollama_url,
                temperature=temperature,
                max_tokens=max_tokens,
                preserve_formatting=preserve_formatting,
                progress_callback=progress_callback
            )
        else:
            return process_docx(
                input_path=input_path,
                ollama_model=model,
                ollama_url=self.ollama_url,
                temperature=temperature,
                max_tokens=max_tokens,
                preserve_formatting=preserve_formatting
            )
    
    def batch_process_documents(self, directory, file_pattern="*.docx", model=None,
                               temperature=0.7, max_tokens=2000, preserve_formatting=True):
        """
        Process multiple DOCX files in a directory.
        
        :param directory: directory containing docx files
        :param file_pattern: pattern to match files (default: *.docx)
        :param model: the Ollama model to use (default: uses self.ollama_model)
        :param temperature: controls randomness
        :param max_tokens: maximum tokens per request
        :param preserve_formatting: whether to preserve formatting
        :return: list of output file paths
        """
        model = model or self.ollama_model
        
        return batch_process_docx(
            directory=directory,
            file_pattern=file_pattern,
            ollama_model=model,
            ollama_url=self.ollama_url,
            temperature=temperature,
            max_tokens=max_tokens,
            preserve_formatting=preserve_formatting
        )
        