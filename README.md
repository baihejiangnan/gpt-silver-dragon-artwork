# GPT 白银龙娘 · 美术协作库

[在线预览](https://baihejiangnan.github.io/gpt-silver-dragon-artwork/) · [下载全部资源](https://github.com/baihejiangnan/gpt-silver-dragon-artwork/archive/refs/heads/main.zip) · [参与修改](CONTRIBUTING.md) · [辅助改图提示词](docs/EDIT_PROMPTS.md)

用于一起改进 GPT 拟人化白银龙娘及其卡牌美术。角色为白发、紫瞳、银色龙角、淡紫龙翼与银鳞龙尾，采用白银长礼服。网站沿用已评审的卡面预览，增加人物资产、历史试稿和协作入口。

这是独立素材仓库，从本地制作工程复制资源建立，不包含游戏工程、账号配置或原项目 Git 历史。

## 已收录内容

| 内容 | 数量 | 路径 |
| --- | ---: | --- |
| 人物采用视图、完整资产卡、原始参考 | 6张 | [assets/character](assets/character) |
| 普通展示组独立插画 | 23张 | [assets/cards/common-v1](assets/cards/common-v1) |
| 早期技能插画试稿 | 6张 | [assets/cards/experiments](assets/cards/experiments) |
| 历史未采用候选 | 3张 | [assets/archive](assets/archive) |
| 带牌名、费用与基础效果的完整卡面 | 23张 | [cards/common-v1](cards/common-v1) |
| 编号总览 | 4张 | [overviews](overviews) |

共 **38张原生素材图 + 27张卡面与总览图 = 65张PNG**。原生素材按原文件字节复制，尺寸与 SHA-256 见 [data/assets.json](data/assets.json)。不将完整四视图卡的裁切图冒充独立生成图。

人物原始提示词在 [prompts/character-original.json](prompts/character-original.json)，23张卡牌提示词在 [prompts/common-cards.v1.json](prompts/common-cards.v1.json)，早期试稿与被替换候选的提示词在 [prompts/experiments.v1.json](prompts/experiments.v1.json)。提示词记录实际生成要求，图片仍以实际可见内容为准；没有暴露的模型版本、随机种子不猜测填写。

## 从哪里修改

- 统一角色与画风：[风格规范及基础提示词](docs/STYLE_GUIDE.md)。
- 只改尾扫、龙爪、光效或人物局部：[辅助修改提示词](docs/EDIT_PROMPTS.md)。
- 对照卡牌名称、技能、构图与组合：[data/common-cards.v1.json](data/common-cards.v1.json)。
- 查看人物上游设定与制作记录：[records/character](records/character)。
- 提交改图、记录提示词和重建预览：[CONTRIBUTING.md](CONTRIBUTING.md)。

当前23张为3张基础牌和20张普通牌，按收到的截图名单包含“挑衅”、不含“放血”。11—15号基础数值因截图截断，暂用本地v0.98.3数据并注明待核对；16号消耗范围待核定。本轮不展示升级效果，未设计罕见、稀有或其他组。早期6张试稿属于旧探索方案，不计入正式85张单人牌池。

## 本地查看与重建

无需前端构建依赖。打开 `index.html`，或在仓库根目录运行：

```sh
python -m http.server 8000
```

修改模板、卡牌设计数据或文字后，重建网页：

```sh
python -m pip install -r requirements.txt
python scripts/build_site.py
```

修改独立插画或需要同步完整卡面的效果文字时，重建23张卡面、4张总览和网页：

```sh
python scripts/build_site.py --render-cards
```

卡面中文字体在 Windows 默认使用本机微软雅黑，仓库不分发该字体。其他系统需要指定已安装的中文字形字体，例如：

```sh
python scripts/build_site.py --render-cards --font /path/to/CJK-Regular.ttc --font-bold /path/to/CJK-Bold.ttc
```

GitHub Pages 使用 `main` 分支根目录发布，包含 `.nojekyll`。合并改图后，把重建的卡面和网页一起提交，Pages 随分支更新发布。

## 来源

人物图组沿用 [Mccrree/chatgpt-dragon-character-assets](https://github.com/Mccrree/chatgpt-dragon-character-assets/tree/14d824a4722731bf47cd7cffd28b041f2600ebc1)。卡牌新插画由内置 `image_gen` 生成，所有参考路径在公开副本中已改为仓库相对路径。

详细来源与使用边界见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本项目为非官方角色视觉探索，不代表 OpenAI 或《杀戮尖塔》官方。
