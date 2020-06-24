from collections import deque, Counter
from rasa.nlu.components import Component
from rasa.nlu.training_data import Message
from typing import Any, Dict, Optional, Text, List, Type
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.classifiers.classifier import IntentClassifier


class EntityEditIntent(IntentClassifier):
    """实体修改意图

    属于意图分类器，若匹配多个实体则优先取前者
    """
    provides = ["intent"]

    defaults = {
        "entity": [],  # 根据下标一一对应
        "intent": [],
        "min_confidence": 1,  # 置信度阈值，预设为绝对修改
        "max_entitiy_count": 5,  # 实体允许出现的最大数量
        "max_entitiy_type": 2,  # 实体类型允许出现的最大数量
        "edit_intent_ranking": True  # 是否修改intent_ranking
    }

    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        return [EntityExtractor]

    def __init__(self, component_config=None):
        super(EntityEditIntent, self).__init__(component_config)
        self.entity = self.component_config.get("entity")
        self.intent = self.component_config.get("intent")
        self.min_confidence = self.component_config.get("min_confidence")
        self.max_entitiy_count = self.component_config.get("max_entitiy_count")
        self.max_entitiy_type = self.component_config.get("max_entitiy_type")
        self.edit_intent_ranking = self.component_config.get("edit_intent_ranking")

        # 实体或意图为空
        if not self.entity:
            raise ValueError("entity can not be empty.")
        if not self.intent:
            raise ValueError("intent can not be empty.")
        # 实体和意图长度要一致
        if len(self.entity) != len(self.intent):
            raise ValueError("length of entity and intent should be same.")

    def process(self, message, **kwargs):
        entities = message.get("entities", [])
        intent = message.get("intent", {})
        intent_ranking = message.get("intent_ranking", [])

        entitiy_count = len(entities)
        type_counter = Counter([i['entity'] for i in entities if 'entity' in i])
        entitiy_type = len(type_counter)
        # 太多实体
        if entitiy_count > self.max_entitiy_count:
            return
        # 太多实体类型
        if entitiy_type > self.max_entitiy_type:
            return
        # 没有实体
        if entitiy_count == 0:
            return

        # 现有置信度最高的意图达不到阈值，修改意图
        match_intent = []
        if intent["confidence"] <= self.min_confidence:
            for entity in entities:
                entity_name = entity["entity"]
                if entity_name in self.entity:
                    entity_index = self.entity.index(entity_name)  # 根据下标一一对应
                    intent_name = self.intent[entity_index]
                    match_intent.append(intent_name)
        # 优先选靠前的意图
        for i in self.intent:
            if i in match_intent:
                _intent = {"name": i, "confidence": 1.0}
                message.set("intent", _intent, add_to_output=True)

                # 修改intent_ranking
                if self.edit_intent_ranking and intent_ranking:
                    name = _intent["name"]
                    for i in intent_ranking:
                        i["confidence"] = 0.0
                        if i["name"] == name:
                            remove = i
                    intent_ranking.remove(remove)
                    intent_ranking = deque(intent_ranking)
                    intent_ranking.appendleft(_intent)
                    intent_ranking = list(intent_ranking)
                    message.set("intent_ranking", intent_ranking, add_to_output=True)
                break
