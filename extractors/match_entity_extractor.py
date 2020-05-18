# -*- coding: utf-8 -*-
# @Author  : XerCis
# @Time    : 2020/5/15 15:33
# @Function: Extract entity

import os
from typing import Any, Text, Dict
from rasa.nlu.extractors import EntityExtractor


class MatchEntityExtractor(EntityExtractor):
    """绝对匹配提取实体"""
    provides = ["entities"]

    defaults = {
        "dictionary_path": None
    }

    def __init__(self, component_config=None):
        print("init")
        super(MatchEntityExtractor, self).__init__(component_config)
        self.dictionary_path = self.component_config.get("dictionary_path")
        self.data = {}  # 用于绝对匹配的数据
        for file_path in os.listdir(self.dictionary_path):
            if file_path.endswith(".txt"):
                file_path = os.path.join(self.dictionary_path, file_path)
                file_name = os.path.basename(file_path)[:-4]
                with open(file_path, mode="r", encoding="utf-8") as f:
                    self.data[file_name] = f.read().splitlines()

    def process(self, message, **kwargs):
        """绝对匹配提取实体词"""
        print("process")
        entities = []
        for entity, value in self.data.items():
            for i in value:
                start = message.text.find(i)
                if start != -1:
                    entities.append({
                        "start": start,
                        "end": start + len(i),
                        "value": i,
                        "entity": entity,
                        "confidence": 1
                    })
        extracted = self.add_extractor_name(entities)
        message.set("entities", extracted, add_to_output=True)

    @classmethod
    def load(cls, meta: Dict[Text, Any], model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        print("load")
        return cls(meta)
