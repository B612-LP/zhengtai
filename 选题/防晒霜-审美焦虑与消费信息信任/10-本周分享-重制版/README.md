# 防晒实验室｜本周分享重制版

## 打开与演示

- 直接打开 [index.html](<index.html>)，无需服务器、网络或额外资源。
- 页面默认跟随系统明暗；手机可纵向阅读。
- 顶栏「全屏演示」进入单页模式；支持方向键、空格、PageUp / PageDown、Home / End、Esc。浏览器不允许全屏时仍保留单页演示。
- 「打印 / 存为PDF」输出全部14页。普通阅读模式中可展开每页「讲者提示与节奏」。
- [分享展示.pptx](<分享展示.pptx>) 为14页可编辑版本：原生文字、形状和形状图表，无整页截图；每页含讲者notes。
- 建议主体约23分钟＋讨论5分钟；40分钟延展点已写在末页notes。

## 可复跑

在工作区根目录执行：

```bash
"/Users/b612-lp/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/bin/python3" "选题/防晒霜-审美焦虑与消费信息信任/10-本周分享-重制版/build_showcase.py"
```

生成器只写本目录；不修改旧Office或上游数据。依赖环境为DSH的Python和python-pptx，不需要安装第三方前端库。

## 数据与边界

- [build_showcase.py](<build_showcase.py>) 读取上一级真实采集目录中的 [products_clean.csv](<../数据/正式采集01-2026-10-30/products_clean.csv>) 和 [stats_real.json](<../数据/正式采集01-2026-10-30/stats_real.json>)，交叉检查价格带、店铺交叉表、标题词频等值，输出共享数据 [source_data.json](<source_data.json>)。
- HTML内嵌同份共享数据，PPTX按同份数据绘制，避免离线file协议fetch限制。
- 119是苏宁单次搜索快照去重商品链接，不是品牌数或市场总体；39到手价、80标价，不是等容量价格。
- 价格带延续原清洗口径：0<p≤50、50<p≤100、100<p≤200、p>200；图中“200+”统一展示为“>200元”。
- χ²与V只作本表描述，期望频数稀疏；模拟385不验证真实假设，H1原跨构念比较无效，模拟价格情境与旧问卷不一致。
- 抗老0只指标题字面；SPF/PA标题未写不等于产品无参数。
- 新问卷候选版待审核；真实需求侧未回收；备案、评论正文、跨平台未完成，本轮暂缓。

## 验证状态

[validation.json](<validation.json>) 是生成时自动重建的结构检查记录：14页、14页notes、无整页图片、形状处于画布内，119条唯一product_id及CSV/JSON统计对照通过。脚本检查不代表文字视觉适配或浏览器功能验收。

按分工，本目录作者未做浏览器或Office视觉检查，由Lead统一验收。旧版17页PPTX未覆盖；没有commit或push。
