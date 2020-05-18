# 简介
Rasa自定义中文组件

# 意图分类(classifiers)

# 仿真器(emulators)

# 实体提取(extractors)
## 1. 绝对匹配

配置
```yaml
- name: "extractors.match_entity_extractor.MatchEntityExtractor"
  dictionary_path: "data/lookup_tables/"
  take_short: True  # 重复实体取短
#  take_long: True  # 重复实体取长
```

输入

```text
海西全称为海西蒙古族藏族自治州
```

输出

```json
{
  "entities": [
    {
      "start": 0,
      "end": 2,
      "value": "海西",
      "entity": "city",
      "confidence": 1,
      "extractor": "MatchEntityExtractor"
    }
  ]
}
```

# 特征提取(featurizers)

# 分词器(tokenizers)

# TODO
1. 

# 参考文献
1. [Choosing a Pipeline](https://rasa.com/docs/rasa/nlu/choosing-a-pipeline/)