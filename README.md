# 简介
Rasa自定义中文组件





<br><br>
# 测试方法
将需要的组件代码复制到config.yml同一文件夹下，并配置config.yml

训练（改字符串不用训练，改数值要训练）
```bash
rasa train nlu
```

运行nlu组件测试
```bash
rasa shell nlu
```






<br><br>
# 意图分类(classifiers)
## 1. 实体修改意图

配置
```yaml
- name: "classifiers.entity_edit_intent.EntityEditIntent"
  entity: ["scene", "city"]  # 根据下标一一对应，实体scene对应意图ask_scene，且ask_scene优先级大于ask_city
  intent: ["ask_scene", "ask_city"]
  min_confidence: 1  # 置信度阈值，预设为绝对修改
  max_entitiy_count: 3  # 实体允许出现的最大数量
  max_entitiy_type: 2  # 实体类型允许出现的最大数量
  edit_intent_ranking: True  # 是否修改intent_ranking
```

输入
```text
我想去北京的故宫
```

输出。ask_scene优先级大于ask_city
```json
{
  "intent": {
    "name": "ask_scene",
    "confidence": 1.0
  }
}
```

输入
```text
我想去北京的故宫、长城、圆明园
```

输出。实体超过3个，不修改意图
```json
{
  "intent": {
    "name": "affirm",
    "confidence": 0.29089126967953416
  }
}
```

输入
```text
我今天想去北京的故宫
```

输出。实体类型超过2个，不修改意图
```json
{
  "intent": {
    "name": "affirm",
    "confidence": 0.29089126967953416
  }
}
```

若edit_intent_ranking为false，将不修改intent_ranking

输入
```text
我想去北京的故宫
```

输出。只修改了intent，没修改intent_ranking
```json
{
  "intent": {
    "name": "ask_scene",
    "confidence": 1.0
  },
  "intent_ranking": [
    {
      "name": "greet",
      "confidence": 0.34340366590002536
    },
    {
      "name": "affirm",
      "confidence": 0.2200067386424407
    }
  ]
}
```










<br><br>
# 仿真器(emulators)
暂无







<br><br>
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









<br><br>
# 特征提取(featurizers)
暂无







<br><br>
# 分词器(tokenizers)
暂无






<br><br>
# TODO
1. 








<br><br>
# 参考文献
1. [Choosing a Pipeline](https://rasa.com/docs/rasa/nlu/choosing-a-pipeline/)
2. [Rasa NLU GQ](https://github.com/GaoQ1/rasa_nlu_gq)