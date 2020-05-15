import pickle
from typing import Any, Text, Dict
from rasa.nlu.components import Component
from nltk.classify import NaiveBayesClassifier

SENTIMENT_MODEL_FILE_NAME = "sentiment_classifier.pkl"


class SentimentAnalyzer(Component):
    """自定义情感分析组件"""
    name = "sentiment"
    provides = ["entities"]
    requires = ["tokens"]
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(SentimentAnalyzer, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """从文本文件中加载情感标签，检索训练分词并格式化，形成情感分类器"""
        with open("labels.txt", "r") as f:
            labels = f.read().splitlines()
        training_data = training_data.training_examples  # list of Message objects
        tokens = [list(map(lambda x: x.text, t.get("tokens"))) for t in training_data]
        processed_tokens = [self.preprocessing(t) for t in tokens]
        labeled_data = [(t, x) for t, x in zip(processed_tokens, labels)]
        self.clf = NaiveBayesClassifier.train(labeled_data)

    def convert_to_rasa(self, value, confidence):
        """将模型输出转换为Rasa NLU的输出格式"""
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "sentiment_extractor"}
        return entity

    def preprocessing(self, tokens):
        """创建训练示例的词袋表示"""
        return ({word: True for word in tokens})

    def process(self, message, **kwargs):
        """检索新消息的分词，并将其传给分类器，将预测结果追加到message中"""
        if not self.clf:
            print("No training!")
        else:
            tokens = [t.text for t in message.get("tokens")]
            tb = self.preprocessing(tokens)
            pred = self.clf.prob_classify(tb)
            sentiment = pred.max()
            confidence = pred.prob(sentiment)
            entity = self.convert_to_rasa(sentiment, confidence)
            message.set("entities", [entity], add_to_output=True)

    def persist(self, file_name, model_dir):
        """将整个类持久化"""
        classifier_file = SENTIMENT_MODEL_FILE_NAME
        with open(classifier_file, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        return {"classifier_file": SENTIMENT_MODEL_FILE_NAME}

    @classmethod
    def load(cls, meta: Dict[Text, Any], model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        file_name = meta.get("classifier_file")
        classifier_file = file_name
        with open(classifier_file, "rb") as f:
            return pickle.load(f)
