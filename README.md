# 简介
Rasa自定义中文组件

# 已实现功能
1. 实体提取绝对匹配
```json
{
  "entities": [
    {
      "start": 3,
      "end": 5,
      "value": "北京",
      "entity": "city",
      "confidence": 1,
      "extractor": "MatchEntityExtractor"
    }
  ]
}
```

# TODO
1. 