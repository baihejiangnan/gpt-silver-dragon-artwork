# 来源与使用说明

## 人物图组

采用图、完整资产卡、参考图及一个未采用背面稿，来自用户指定的 [Mccrree/chatgpt-dragon-character-assets](https://github.com/Mccrree/chatgpt-dragon-character-assets)，固定提交 `14d824a4722731bf47cd7cffd28b041f2600ebc1`。原生PNG按原字节复制，人物原始提示词与记录保存在 `prompts/character-original.json` 和 `records/character/`。

公开副本将记录中的资源引用改为仓库相对路径，不保留本机用户名或制作工程绝对路径。这种整理不会改变图片字节。

## 卡牌插画

23张普通展示组插画、6张早期试稿及2张被替换的早期候选，由本项目制作过程中使用内置 `image_gen` 生成。实际提示词、所用参考及未知模型字段分别记录在 `prompts/common-cards.v1.json` 与 `prompts/experiments.v1.json`。

这些卡牌插画以采用的人物图组为参考。网页卡框、技能文字和总览为确定性排版产物。未收录《杀戮尖塔》原版卡牌插画或游戏源码。

## 人物资产卡工作流

上游制作方法参考 [GaryLauLGY/character-asset-card](https://github.com/GaryLauLGY/character-asset-card)，版本 `484d68e0503510df4d8625093dce763f74f993d2`。上游记录附带的 MIT 许可证原文保存在 `records/character/LICENSE.upstream.txt`，Copyright (c) 2026 Gary Lau。

该MIT许可对应上游工作流代码，不表示参考图片、人物形象或本仓库全部美术自动采用MIT许可。本仓库没有为整套美术另设统一商业授权条款；保留来源说明，通过Fork与PR协作提交改进。

## 主题与规则参考

GPT／ChatGPT作为非官方拟人化主题使用，本仓库不代表OpenAI。卡牌基础玩法及原牌对照参考《杀戮尖塔2》铁甲战士；普通组23张为视觉与命名初稿，含已标明的版本待核对数据，不代表原作官方资源或数值发布。

微软雅黑仅由重建脚本从使用者本机读取，不随仓库分发。其他系统可按README指定自己可使用的中文字形字体。
