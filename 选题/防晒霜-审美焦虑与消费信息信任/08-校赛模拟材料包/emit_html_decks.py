# 两版 HTML 幻灯片：与 pptx 同内容；CSS 变量跟随系统明暗；键盘翻页
import html as H

CSS=''':root{--bg:#f6f7f9;--card:#fff;--ink:#1c2330;--muted:#68738a;--line:#e4e8ef;--accent:#0f6f5c;--warn:#b3423a;--warnbg:#fdf3e4}
@media (prefers-color-scheme:dark){:root{--bg:#14171d;--card:#1d222b;--ink:#e8ecf2;--muted:#9aa5b8;--line:#2c3340;--accent:#5fc4ab;--warn:#e08a82;--warnbg:#2b241a}}
*{box-sizing:border-box;margin:0}
html{scroll-snap-type:y mandatory;scroll-behavior:smooth}
body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink)}
section{min-height:100vh;scroll-snap-align:start;padding:56px 8vw;display:flex;flex-direction:column;justify-content:center;border-bottom:1px solid var(--line)}
section.cover{align-items:flex-start;background:linear-gradient(135deg,var(--card),var(--bg))}
h1{font-size:clamp(26px,4.2vw,44px);line-height:1.25;margin-bottom:12px}
h2{font-size:clamp(20px,3vw,32px);border-left:6px solid var(--accent);padding-left:14px;margin-bottom:22px}
ul{font-size:clamp(15px,1.6vw,20px);line-height:1.9;padding-left:1.3em}
li{margin:8px 0}
table{border-collapse:collapse;margin:10px 0;font-size:clamp(13px,1.4vw,17px)}
th,td{border:1px solid var(--line);padding:7px 14px;text-align:center}
th{background:var(--card);color:var(--muted)}
.sub{color:var(--muted);font-size:clamp(13px,1.5vw,18px)}
.note{margin-top:22px;font-size:clamp(12px,1.3vw,16px);color:var(--muted)}
.warnnote{margin-top:22px;padding:10px 16px;border-radius:10px;background:var(--warnbg);color:var(--warn);font-size:clamp(12px,1.3vw,16px)}
#cnt{position:fixed;right:18px;bottom:14px;font-size:13px;color:var(--muted);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:4px 12px}'''

def render(path,title,slides):
    secs=[]
    for i,s in enumerate(slides):
        kind='cover' if i==0 else ''
        inner=f'<h1>{H.escape(s["t"])}</h1>' if i==0 else f'<h2>{H.escape(s["t"])}</h2>'
        if s.get('b'):
            inner+='<ul>'+''.join(f'<li>{H.escape(b)}</li>' for b in s['b'])+'</ul>'
        if s.get('tb'):
            rows=s['tb']; inner+='<table><tr>'+''.join(f'<th>{H.escape(c)}</th>' for c in rows[0])+'</tr>'
            for r in rows[1:]: inner+='<tr>'+''.join(f'<td>{H.escape(c)}</td>' for c in r)+'</tr>'
            inner+='</table>'
        if s.get('n'):
            cls='warnnote' if s.get('w') else 'note'
            inner+=f'<div class="{cls}">{H.escape(s["n"])}</div>'
        secs.append(f'<section class="{kind}">{inner}</section>')
    JS='const ss=[...document.querySelectorAll("section")];let i=0;const go=n=>{i=Math.max(0,Math.min(ss.length-1,n));ss[i].scrollIntoView();document.getElementById("cnt").textContent=(i+1)+" / "+ss.length};addEventListener("keydown",e=>{if(["ArrowRight","ArrowDown","PageDown"].includes(e.key))go(i+1);if(["ArrowLeft","ArrowUp","PageUp"].includes(e.key))go(i-1);});addEventListener("scroll",()=>{i=ss.findIndex(s=>{const r=s.getBoundingClientRect();return r.top>-innerHeight/2&&r.top<innerHeight/2;});document.getElementById("cnt").textContent=(i+1)+" / "+ss.length;});go(0);'
    doc=f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body>{"".join(secs)}<div id="cnt"></div><script>'+JS+'</script></body></html>'
    open(path,'w').write(doc); print('saved',path)

A=[
{'t':'防晒霜购买中的审美焦虑与消费信息信任','b':['基于供给端公开数据与问卷调查的混合研究','第十七届全国大学生市场调查与分析大赛 · 校赛模拟版','汇报人：____（匿名）']},
{'t':'目录','b':['① 背景与研究问题','② 研究设计与数据','③ 供给端发现（真实数据 n=119）','④ 需求端发现（模拟演示 n=385）','⑤ 结论与建议']},
{'t':'为什么是防晒霜','b':['全年刚需化：防光老化教育推动日常使用','两套信息体系打架：专业参数 vs 品牌宣传/社媒推荐','备案信息公开可查，但多数消费者不查','审美焦虑（美白/抗老话术）是营销核心杠杆'],'n':'痛点：审美焦虑 · 信息门槛 · 网络推荐 · 价格品质偏差'},
{'t':'研究问题与假设','b':['总问题：买防晒时，更相信专业参数，还是品牌宣传和社媒推荐？','RQ1 信任结构｜RQ2 焦虑与门槛的影响｜RQ3 行为结果｜RQ4 宣称一致性','H1 态度—行为缺口　H2 焦虑↑→边缘路径依赖↑　H3 门槛↑→参数信任↓','H4 价格↑→品质感知↑　H5 人群差异'],'n':'理论锚：信息不对称 · ELM双路径 · 信息源可信度 · 社会比较'},
{'t':'研究设计','b':['混合方法：供给端公开数据采集 ＋ 结构化问卷（28题）＋ 关键事件访谈（备选）','对象：18–35岁、近6个月购买/使用过防晒产品的消费者','抽样：非概率便利＋滚雪球，n≈385（95%置信、e=5%），发放≥460','质控：甄别题＋时长下限＋注意力校验＋预调研30–50份']},
{'t':'数据来源','b':['供给端：真实公开数据，119款商品（2026-10-30 快照，URL+时间戳+原始存档）','需求端：正式问卷 2026-11-08 起回收；本版以模拟演示数据（n=385）展示分析链路'],'n':'⚠ 需求端为模拟演示数据，非真实调查，回收后整体替换','w':True},
{'t':'发现① 价格右偏分布','b':['中位数 ¥99.9 ／ 均值 ¥128.7（右偏：报告用中位数说话）','区间 ¥9.9–489，四分位 ¥59.0–178.5','价格带四分均匀：27/33/33/26','到手价占 39/119 —— 标价/到手价双口径要分层比较']},
{'t':'发现② 渠道垄断价格带','tb':[['价格带','专营店','品牌旗舰','海外专营','苏宁自营'],['0–50元','10','3','0','14'],['50–100元','14','0','5','14'],['100–200元','6','0','10','17'],['200元以上','0','0','17','9']],'n':'χ²=47.5（df=9），Cramér V=0.365：海外专营垄断200+价位（65%），渠道选择=价格信号'},
{'t':'发现③ 宣称结构','b':['词频：隔离 58% ≫ 清爽 24% ＞ 防水 14% ＞ 美白 11% ＞ 敏感肌 9%','SPF50系宣称 45%；PA++++ 仅 8% —— 参数宣称高度同质','"抗老"宣称 = 0：焦虑话术不在商品层，在社媒种草层','标题即广告位：参数与宣传混编，消费者难以分离']},
{'t':'需求端发现（模拟演示）','b':['H2 焦虑↔社媒信任 r=0.352（支持）','H3 理解门槛↔参数信任 r=0.485（支持）','H4 价格89/159/259元 → 品质感知 3.00/3.52/4.29 单调上升（支持）','H1 未获支持：参数信任 3.14 vs 社媒使用 2.61（t=9.86）——分析不必然验证假设'],'n':'⚠ 本章为模拟演示数据，仅演示分析链路','w':True},
{'t':'人群画像（聚类演示）','b':['氛围型 149 人：社媒信任 3.83 最高——种草层主受众','参数型 140 人：参数 3.59、社媒 2.64——成分党','低卷入型 96 人：三维均低——升级潜力人群']},
{'t':'结论与建议','b':['消费者：按渠道分层比价；把备案查询作为低成本验证动作','品牌：参数同质化下，差异化转向合规、具体的场景沟通','平台/治理：软广标注治理重点在种草层；热度与品质解耦展示','方法：双源混合方法可由本科生团队一学期完成']},
{'t':'局限与真实度声明','b':['供给端：单平台、单关键词、单时点；SPF/PA为标题宣称（备案核验待办）','需求端：本版为模拟演示数据，外推无效；正式版待真人问卷（11-08起）','红线：AI 不生成任何原始数据；AI 过程留痕见附录A','谢谢！欢迎提问']},
]
B=[
{'t':'一个防晒霜课题的全流程演练复盘','b':['AI 主跑 × 人工把关 · 从选题到校赛材料包','第十七届正大杯 · 模拟考彩排','分享人：韩之凡 · 2026-11-03']},
{'t':'为什么做这次演练','b':['10-28 会议方向：把 AI 能力用到交付过程中，而不是死磕落地结果','网考考纲 10 章 ＝ 市场调查项目全流程：跑项目＝把 10 章全部实操一遍','目标：跑通到"校赛要交的全套材料"，队友每人可复用']},
{'t':'全流程地图（8环节 × 考纲10章）','tb':[['环节','考纲章节','交付物','状态'],['①概述','第1章','01 概述','✅'],['②方案','第3章','02 调查方案','✅'],['③问卷','第4章','06 问卷终稿28题','✅'],['④抽样','第7章','n≈385/发放≥460','✅'],['⑤采集','第2章','真实119商品+数据包','✅'],['⑥清洗','第5章','clean CSV+脚本','✅'],['⑦分析','第6/8/9/10章','统计+聚类+报告','✅'],['⑧交付','第5章','报告/PPT/看板/材料包','✅']]},
{'t':'环节①② 怎么把"感觉"变成可回答的问题','b':['痛点（审美焦虑/信息门槛/推荐影响/价格偏差）→ 总问题 → 4个子问题','假设从理论锚长出来：信息不对称 · ELM 双路径 · 信息源可信度','对照：选题池 v1.4/v2 的判定思路同源——先立标准再挖题']},
{'t':'环节③④ 题项从假设长出来','b':['C 模块三维度（参数/宣传/社媒信任各4题）↔ RQ1 信任结构','E 焦虑简版5题 ↔ H2；F 理解门槛 ↔ H3；G 价格情境 ↔ H4','样本量公式现场算：n=z²p(1−p)/e²=1.96²×0.25/0.05²≈385 → 发放≥460']},
{'t':'环节⑤ 采集 · 故事1：脚本秒采','b':['苏宁搜索页静态字段：curl+python 一次解析 30/30','滚动触发懒加载 → 119/119 全字段（标题/价格/店铺/评价数/SPF·PA宣称）','原始 HTML+JSON+脚本全部归档，可复跑']},
{'t':'环节⑤ 采集 · 故事2：反爬兜底（现场演示位）','b':['价格接口三种姿势全被拒："请求非法"（留痕 raw-suning-price.jsonp）','换路线：浏览器渲染＋滚动懒加载 → 价格 29/30 → 119/119','takeaway：AI 碰壁会换路，每一步留痕 —— 这就是"AI 用在交付过程"'],'n':'★ 现场演示：数据看板 + 价格列前后对比','w':True},
{'t':'数据真实度红线','b':['AI 不生成任何原始数据：问卷必须真人填、商品必须真采','模拟演示数据四处标注隔离（文件名/CSV/报告/看板）','AI 全程留痕：资料/AI使用记录/ 按日期记档']},
{'t':'环节⑥⑦ 清洗与分析','b':['pandas 标准化：去重/价格数值化/评价数换算/店铺分类/SPF·PA提取','统计量怎么读：右偏分布 → 用中位数不用均值','卡方+Cramér V：类别变量关联强度；Spearman：序变量相关']},
{'t':'真实发现① 渠道垄断价格带','b':['χ²=47.5，Cramér V=0.365（中等偏强）','海外专营垄断 200+ 价位（17/26）；国内专营店全部 <100 元','启示：跨渠道直接比价会系统性误判']},
{'t':'真实发现② 宣称同质 + 抗老=0','b':['"隔离"58% ≫ 其他；SPF50系 45%；PA++++ 仅 8%','"抗老"宣称 0 款 → 焦虑话术在种草层，不在商品层','反推 H2 的作用层位——问卷设计因此更有针对性']},
{'t':'需求侧：模拟数据的教训','b':['H2 r=.352 / H3 r=.485 / H4 单调：按生成结构验证（自证演示）','H1 未支持：参数信任 3.14 vs 社媒使用 2.61（t=9.86）','教训：分析不必然验证假设——真数据同样会打脸，这正常']},
{'t':'人群画像（聚类演示）','b':['k-means k=3：氛围型 149 / 参数型 140 / 低卷入 96','正式问卷回来，同一份代码直接出真实画像']},
{'t':'环节⑧ 交付物全家福','b':['报告 docx（校赛格式·匿名）＋一页摘要','答辩PPT校赛版 ＋ 本次分享版（pptx+html 双格式）','数据看板.html（真实/模拟分区）＋问卷终稿＋附录包＋QA预案']},
{'t':'队友怎么复用这套打法','b':['永彩洁：你的"素颜霜×知识点"概述+数据收集方案，可套 01/02 模板','多啦酱：方法链路（假设→量表→分析）可直接迁移','卢雨婷：AI 工具路线正好接 05 的采集/标注用法','大一A：创新视角加在 E/F 模块的题项和人群切分上']},
{'t':'下一步','b':['11-01 24:00 DDL：交接龙文件包','11-08 起真人问卷回收 → 报告需求侧整体替换重算','备案核验（国妆特字）+ 京东对照源 + 评价正文','知识赛：11-07 前考过（一起加油）']},
{'t':'Q&A','b':['全部文件：选题/防晒霜-审美焦虑与消费信息信任/','数据可复算：脚本+原始存档全归档','谢谢！']},
]
render('答辩PPT-校赛版.html','答辩PPT·校赛模拟版',A)
render('分享会PPT-全流程复盘版.html','分享会PPT·全流程复盘（40min）',B)
