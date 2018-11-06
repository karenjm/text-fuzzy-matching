#! /usr/bin/env python

# -*- coding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import jieba
from gensim import corpora,models,similarities


class FuzzyMatching(object):
    def __init__(self, templates_build, templates_status, text):
        self.templates_build = templates_build
        self.templates_status = templates_status
        self.texts = self._append_companion_for_text(text)
        self.texts_list = self._split_texts(self.texts)

    def _append_companion_for_text(self, text):
        companion_text = 'shanghai'
        texts = list()
        texts.append(text)
        texts.append(companion_text)
        return texts

    def _split_text(self, text):
        return [word for word in jieba.cut(text)]

    def _split_texts(self, texts):
        all_texts_list = list()
        for text in texts:
            text_list = self._split_text(text)
            all_texts_list.append(text_list)
        return all_texts_list

    def _text_is_matching_template(self, template):
        # Generate bag-of-words
        # dictionary.token2id could show the relation between dictionary key and word
        dictionary = corpora.Dictionary(self.texts_list)
        corpus = [dictionary.doc2bow(doc) for doc in self.texts_list]

        template_list = self._split_text(template)
        template_list_vec = dictionary.doc2bow(template_list)

        tfidf = models.TfidfModel(corpus)

        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
        sim = index[tfidf[template_list_vec]]

        result = sorted(enumerate(sim), key=lambda item: -item[1])[0]
        if result[0] == 0 and result[1] > 0.7:
            return result[1]
        else:
            return -1

    def _get_matching_index(self, templates):
        max_index = 0
        for template in templates:
            index = self._text_is_matching_template(template)
            if index != -1 and index > max_index:
                max_index = index
        return max_index

    def text_analyzed(self):
        build_index = self._get_matching_index(self.templates_build)
        status_index = self._get_matching_index(self.templates_status)
        print('build_index={}, status_index={}'.format(build_index, status_index))

        if build_index == 0 and status_index == 0:
            return 'no_match'
        elif build_index >= status_index:
            return 'build'
        else:
            return 'status'
