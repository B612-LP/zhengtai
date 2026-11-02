# -*- coding: utf-8 -*-
# 两版设计级 HTML 幻灯片（横向翻页·高信息密度版）：校赛版(13) + 分享会版(16)
import html as H

CSS = r''':root{--bg:#f2f5f7;--card:#ffffff;--ink:#182130;--muted:#66738a;--line:#e3e8ef;--accent:#0e7a63;--accent2:#c98a2d;--danger:#b3423a;--accentsoft:#e3f0ec;--warnsoft:#fbf0dd;--shadow:0 8px 24px rgba(16,32,48,.06)}
@media (prefers-color-scheme:dark){:root{--bg:#0f1319;--card:#181e28;--ink:#e9edf3;--muted:#96a1b5;--line:#2a3140;--accent:#4fc3a5;--accent2:#dba54e;--danger:#e08a82;--accentsoft:#15251f;--warnsoft:#2a2318;--shadow:0 8px 24px rgba(0,0,0,.35)}}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
body{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink)}
.slide{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:4.5vh 4vw;opacity:0;visibility:hidden;transform:translateX(70px);transition:transform .5s cubic-bezier(.2,.7,.2,1),opacity .5s ease,visibility .5s}
.slide.lft{transform:translateX(-70px)}
.slide.active{opacity:1;visibility:visible;transform:none;z-index:2}
.wrap{width:100%;max-width:1460px;max-height:92vh;overflow-y:auto}
.kicker{font-size:13px;letter-spacing:.18em;color:var(--accent);font-weight:700;margin-bottom:10px;text-transform:uppercase}
h1{font-size:clamp(30px,4vw,48px);line-height:1.22;letter-spacing:.01em}
h2{font-size:clamp(23px,2.9vw,34px);line-height:1.25;margin-bottom:18px}
h2 em{font-style:normal;color:var(--accent)}
.sub{font-size:clamp(14px,1.6vw,19px);color:var(--muted);line-height:1.7}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:var(--shadow)}
.card p,.card li{font-size:clamp(12.5px,1.35vw,15.5px);color:var(--ink);line-height:1.65}
.card p b,.card li b{color:var(--accent)}
.card .tag{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.08em;padding:2px 9px;border-radius:999px;background:var(--accentsoft);color:var(--accent);margin-bottom:8px}
.card .tag.w{background:var(--warnsoft);color:var(--accent2)}
.card .extra{margin-top:8px;padding-top:8px;border-top:1px dashed var(--line);font-size:clamp(11.5px,1.2vw,13.5px);color:var(--muted)}
.kpi{font-size:clamp(24px,3vw,36px);font-weight:800;letter-spacing:-.01em}
.kpi small{font-size:.42em;font-weight:600;color:var(--muted);margin-left:4px}
.kpi .up{color:var(--accent)} .kpi .warn{color:var(--accent2)}
.klabel{font-size:clamp(11.5px,1.25vw,14px);color:var(--muted);margin-top:5px;line-height:1.55}
ul.b{font-size:clamp(14px,1.6vw,18px);line-height:1.85;padding-left:1.2em}
ul.b li{margin:8px 0}
ul.b li::marker{color:var(--accent)}
.bar-row{display:grid;grid-template-columns:110px 1fr 76px;gap:12px;align-items:center;margin:9px 0}
.bar-row .bl{font-size:clamp(12.5px,1.4vw,15px);color:var(--muted);text-align:right}
.bar-track{height:13px;background:var(--line);border-radius:7px;overflow:hidden}
.bar-fill{height:100%;border-radius:7px;background:var(--accent);width:0;transition:width .9s cubic-bezier(.2,.7,.2,1)}
.bar-fill.a2{background:var(--accent2)}
.bar-row .bv{font-size:clamp(12.5px,1.4vw,15px);font-variant-numeric:tabular-nums;font-weight:700}
table{width:100%;border-collapse:separate;border-spacing:0;font-size:clamp(12.5px,1.4vw,15.5px);background:var(--card);border-radius:12px;overflow:hidden;border:1px solid var(--line)}
th,td{padding:9px 12px;text-align:center;border-bottom:1px solid var(--line)}
th{background:var(--accentsoft);color:var(--accent);font-weight:700}
tr:last-child td{border-bottom:none}
td.hl{background:var(--accentsoft);color:var(--accent);font-weight:800}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:4px 0 18px}
.chip{font-size:clamp(12px,1.35vw,14.5px);font-weight:600;padding:5px 14px;border-radius:999px;background:var(--accentsoft);color:var(--accent);border:1px solid var(--line)}
.chip.w{background:var(--warnsoft);color:var(--accent2)}
.chiprow{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.chip.s{font-size:clamp(11px,1.2vw,13px);padding:3px 10px;font-weight:600}
.banner{background:var(--warnsoft);border:1px solid color-mix(in srgb,var(--accent2) 45%,transparent);color:var(--ink);border-radius:12px;padding:12px 18px;font-size:clamp(13px,1.5vw,16px);line-height:1.7;margin-bottom:18px}
.banner b{color:var(--accent2)}
.qbanner{background:var(--accentsoft);border:1px solid var(--accent);color:var(--ink);border-radius:12px;padding:14px 20px;font-size:clamp(16px,2.1vw,23px);font-weight:800;line-height:1.6;margin-bottom:16px}
.qbanner b{color:var(--accent)}
.note{margin-top:14px;font-size:clamp(12px,1.35vw,14.5px);color:var(--muted);line-height:1.7}
.note b{color:var(--accent)}
.foot{margin-top:16px;padding-top:10px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:14px;font-size:clamp(11px,1.2vw,13px);color:var(--muted)}
.foot b{color:var(--accent);font-weight:700}
.vtrack{position:relative;height:10px;background:var(--line);border-radius:5px;margin:10px 0 4px}
.vmark{position:absolute;top:-4px;width:4px;height:18px;background:var(--accent);border-radius:2px}
.vlabels{display:flex;justify-content:space-between;font-size:11px;color:var(--muted)}
.bigend{font-size:clamp(34px,5.5vw,72px);font-weight:900;color:var(--accent);letter-spacing:.02em}
.cover{background:linear-gradient(135deg,var(--accent) 0%,color-mix(in srgb,var(--accent) 72%,#08201a) 100%)}
.cover .wrap{color:#fff}
.cover h1{color:#fff;margin:16px 0 18px;max-width:24em}
.cover .kicker{color:rgba(255,255,255,.75)}
.cover .sub{color:rgba(255,255,255,.85);max-width:34em}
.cover .chips .chip{background:rgba(255,255,255,.14);color:#fff;border-color:rgba(255,255,255,.28)}
.cover .meta{margin-top:34px;font-size:clamp(13px,1.5vw,17px);color:rgba(255,255,255,.8)}
#bar{position:fixed;top:0;left:0;height:4px;background:var(--accent);width:0;z-index:30;transition:width .3s}
#meta{position:fixed;left:22px;bottom:16px;font-size:12px;color:var(--muted);z-index:30}
#cnt{position:fixed;left:50%;transform:translateX(-50%);bottom:18px;font-size:13px;font-variant-numeric:tabular-nums;color:var(--muted);background:var(--card);border:1px solid var(--line);border-radius:999px;padding:5px 14px;z-index:30}
#nav{position:fixed;right:20px;bottom:14px;display:flex;gap:8px;z-index:30}
#nav button{width:44px;height:44px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--ink);font-size:22px;line-height:1;cursor:pointer;box-shadow:var(--shadow);opacity:.9;transition:opacity .15s,border-color .15s,color .15s}
#nav button:hover{opacity:1;color:var(--accent);border-color:var(--accent)}
#nav button:active{transform:scale(.94)}
#nav #fs{font-size:14px}
'''

JS = r'''
const ss=[...document.querySelectorAll('.slide')];let cur=0,lock=0;
const cnt=document.getElementById('cnt'),bar=document.getElementById('bar');
document.body.insertAdjacentHTML('beforeend','<div id="nav"><button id="pv" title="上一页（←↑）">&#8249;</button><button id="nx" title="下一页（→↓ 空格）">&#8250;</button><button id="fs" title="全屏（F）">&#x26F6;</button></div>');
function paint(){ss.forEach((s,i)=>{s.classList.toggle('active',i===cur);s.classList.toggle('lft',i<cur);});
 cnt.textContent=(cur+1)+' / '+ss.length;bar.style.width=((cur+1)/ss.length*100)+'%';
 ss[cur].querySelectorAll('.bar-fill').forEach(b=>{b.style.width='0';requestAnimationFrame(()=>requestAnimationFrame(()=>{b.style.width=b.dataset.w;}));});
 const w=ss[cur].querySelector('.wrap');if(w)w.scrollTop=0;}
function go(n){n=Math.max(0,Math.min(ss.length-1,n));if(n!==cur)cur=n;paint();}
function step(d){const t=Date.now();if(t-lock<150)return;lock=t;go(cur+d);}
document.getElementById('pv').onclick=()=>step(-1);
document.getElementById('nx').onclick=()=>step(1);
document.getElementById('fs').onclick=()=>{document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();};
document.addEventListener('keydown',e=>{const k=e.key;
 if(['ArrowRight','ArrowDown','PageDown',' '].includes(k)){e.preventDefault();step(1);}
 else if(['ArrowLeft','ArrowUp','PageUp'].includes(k)){e.preventDefault();step(-1);}
 else if(k==='Home'){go(0);}else if(k==='End'){go(ss.length-1);}
 else if(k==='f'||k==='F'){document.getElementById('fs').click();}});
addEventListener('wheel',e=>{e.preventDefault();const t=Date.now();if(t-lock>400){lock=t;go(cur+((e.deltaY||e.deltaX)>0?1:-1));}else{lock=t;}},{passive:false});
let tx=0,ty=0;addEventListener('touchstart',e=>{tx=e.touches[0].clientX;ty=e.touches[0].clientY;},{passive:true});
addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-tx,dy=e.changedTouches[0].clientY-ty;if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy))step(dx<0?1:-1);},{passive:true});
paint();
'''

def esc(x): return H.escape(str(x))
def bars(items):
    mx = max(v for _, v, *_ in items) or 1
    out = []
    for it in items:
        lab, val = it[0], it[1]
        cls = 'bar-fill a2' if (len(it) > 2 and it[2] == 'a2') else 'bar-fill'
        shown = it[3] if len(it) > 3 else val
        out.append(f'<div class="bar-row"><div class="bl">{esc(lab)}</div><div class="bar-track"><div class="{cls}" data-w="{val/mx*100:.0f}%"></div></div><div class="bv">{esc(shown)}</div></div>')
    return ''.join(out)
def kpis(items):
    return '<div class="cols">' + ''.join(
        f'<div class="card"><div class="kpi">{v}</div><div class="klabel">{l}</div></div>' for v, l in items) + '</div>'
def cards(items):
    parts = []
    for it in items:
        t, b = it[0], it[1]
        e = it[2] if len(it) > 2 else None
        tag = f'<span class="tag">{esc(t)}</span>' if t else ''
        ex = f'<div class="extra">{e}</div>' if e else ''
        parts.append(f'<div class="card">{tag}<p>{b}</p>{ex}</div>')
    return '<div class="cols">' + ''.join(parts) + '</div>'
def table(rows, hl=()):
    out = ['<table><tr>' + ''.join(f'<th>{esc(c)}</th>' for c in rows[0]) + '</tr>']
    for ri, r in enumerate(rows[1:], 1):
        tds = []
        for ci, c in enumerate(r):
            cls = ' class="hl"' if (ri, ci) in hl else ''
            tds.append(f'<td{cls}>{esc(c)}</td>')
        out.append('<tr>' + ''.join(tds) + '</tr>')
    return ''.join(out + ['</table>'])
def sec(kicker, title, body, note=None, foot=None):
    n = f'<div class="note">{note}</div>' if note else ''
    f = f'<div class="foot"><span>{esc(foot[0])}</span><span>{foot[1]}</span></div>' if foot else ''
    return f'<div class="wrap"><div class="kicker">{esc(kicker)}</div><h2>{title}</h2>{body}{n}{f}</div>'
def cover(title, sub, chips, meta):
    ch = '<div class="chips">' + ''.join(f'<span class="chip">{esc(c)}</span>' for c in chips[1:]) + '</div>'
    return f'<div class="wrap"><div class="kicker">{esc(chips[0])}</div><h1>{title}</h1><div class="sub">{sub}</div>{ch}<div class="meta">{esc(meta)}</div></div>'
FT = lambda l, r: (l, r)

# ═══════════ Deck A 校赛版（13页·高密度） ═══════════
A = []
A.append(cover('防晒霜购买中的<br>审美焦虑与消费信息信任',
    '基于供给端公开数据与问卷调查的混合研究 · 一条流水线跑通"概述→方案→问卷→抽样→采集→清洗→分析→交付"',
    ['第十七届正大杯 · 校赛模拟版', '匿名评审', '119 款真实商品数据', '28 题问卷', '2026-10-30'],
    '汇报人：____（匿名）　｜　指导老师：____（匿名）　｜　材料包：08-校赛模拟材料包（报告·PPT·附录A–D·QA预案）'))
A.append(sec('AGENDA', '本次汇报 <em>五部分</em>，对应六个交付文件',
    cards([
        ('01 背景', '<b>两套信息体系</b>为什么打架：参数 vs 宣传/种草，审美焦虑是杠杆', '文件：01 市场调查概述'),
        ('02 设计', '供给端爬取 × 需求端问卷的<b>混合方法</b>，n≈385', '文件：02 调查方案（含抽样）'),
        ('03 供给端', '<b>真实公开数据</b>：119 款商品、价格、宣称、渠道', '文件：数据/正式采集01'),
        ('04 需求端', '信任三维度＋焦虑＋门槛量表；本版为<b>标注模拟演示</b>，11-08 起换真数据', '文件：06 问卷终稿'),
        ('05 结论', '对消费者 / 品牌 / 平台三层建议＋<b>方法论</b>沉淀', '文件：07 报告＋附录A–D'),
    ]),
    foot=FT('材料包：08-校赛模拟材料包/（6 类交付物）', '对应网考考纲：第 1/2/3/4/6/7 章')))
A.append(sec('01 · 背景与痛点', '为什么是<em>防晒霜</em>：四个痛点都有"信息"成分',
    cards([
        ('全年刚需化', '防光老化教育推动防晒从夏季单品变为日常刚需，决策频次升高 → <b>信息依赖升高</b>', '挂钩：问卷 S1 甄别"近6个月购买/使用"'),
        ('两套信息打架', '参数/成分/检测报告（可验证）vs 广告/种草（不可验证）——消费者夹在中间', '挂钩：问卷 B2 信息来源频率矩阵'),
        ('备案无人查', '防晒属特殊化妆品，"国妆特字"公开可查；但查询动作本身有门槛', '挂钩：问卷 D2 是否主动查过备案'),
        ('审美焦虑杠杆', '"美白/抗老"话术把功能品做成容貌管理品，情绪可能压过参数判断', '挂钩：问卷 E 模块焦虑简版 5 题'),
    ]),
    note='四条痛点分别落到问卷的具体模块——痛点不是背景故事，是可测量的变量。', foot=FT('来源：01-市场调查概述.md §一/§二', '考纲挂钩：第 1 章 市场调查概述')))
A.append(sec('01 · 研究问题', '核心问题与<em>假设</em>',
    '<div class="qbanner">消费者购买防晒产品时，更相信<b>专业参数</b>，还是<b>品牌宣传和社交媒体推荐</b>？</div>'
    + cards([
        ('RQ1', '信任结构：对参数/宣传/社媒的信任排序与人群构成'),
        ('RQ2', '审美焦虑与理解门槛如何改变信任路径'),
        ('RQ3', '信任结构如何影响渠道、价格带与溢价意愿'),
        ('RQ4', '商品页宣称与药监局备案的一致性（供给侧核查）'),
    ]) + '<div class="chiprow"><span class="chip s">H1 态度—行为缺口</span><span class="chip s">H2 焦虑↑→边缘路径依赖↑</span><span class="chip s">H3 门槛↑→参数信任↓</span><span class="chip s">H4 价格↑→品质感知↑</span><span class="chip s">H5 性别×身份×肤质差异</span><span class="chip s w">理论锚：信息不对称 · ELM · 信息源可信度 · 社会比较 · 价格—感知质量</span></div>',
    foot=FT('假设的问卷映射：C↔RQ1 · E↔H2 · F↔H3 · G↔H4（见 06 问卷终稿）', '考纲挂钩：第 3 章 调查设计')))
A.append(sec('02 · 研究设计', '混合方法：一硬一软两条<em>证据线</em>',
    cards([
        ('供给端 · 客观', '电商平台公开商品数据：价格/双口径、SPF·PA 宣称、话术词频、店铺类型、评价数', '真实采集 n=119（2026-10-30 快照）'),
        ('需求端 · 主观', '结构化问卷 28 题：甄别/行为/信任三维度/情境/焦虑/门槛/价格感知', '目标有效 n≥385，11-08 起回收'),
        ('抽样设计', '非概率便利＋滚雪球；n=z²p(1−p)/e²≈385（95%、e=5%、p=0.5）→ 发放 ≥460', '学生:职场≈6:4，性别均衡'),
        ('质量控制', '甄别题 · 时长<180s 剔除 · 注意力校验题 · IP 去重 · 预调研 30–50 份 α≥0.7', '无效样本筛除规则随附录提交'),
    ]),
    foot=FT('关键事件访谈（8–10 人）为备选补充', '考纲挂钩：第 3 章 调查设计 ＋ 第 7 章 抽样估计')))
A.append(sec('02 · 数据来源', '两个数据源，两种<em>标注</em>',
    cards([
        ('真实公开数据 ✅', '苏宁"防晒霜"搜索页 119 款：标题/卖点/价格（标价·到手价）/店铺/评价数/SPF·PA 宣称<br>每条带 URL＋时间戳＋原始页面存档，清洗与统计脚本可复跑', '正式采集01 · 2026-10-30'),
        ('模拟演示数据 ⚠️', '正式问卷 11-08 起回收；本版以参数化生成数据（n=385，种子 42，规则公开）演示分析链路<br>文件名/CSV 列/报告/看板<b>四处标注隔离</b>', '模拟问卷-仅流程演示/'),
        ('采集工程', '静态字段 curl+python 一次解析；价格接口三次被拒（留痕）→ 浏览器渲染＋滚动懒加载兜底', 'AI 用于交付过程的实证案例'),
    ]),
    note='价格存在"标价/到手价"双口径（到手价 39/119）——所有价格比较均分层进行。', foot=FT('数据字典：03-数据采集字典.md（四库字段）', '考纲挂钩：第 2 章 数据收集')))
A.append(sec('03 · 供给端发现', '发现① 价格<em>右偏</em>：中位数说话',
    kpis([('¥99.9<small>中位数</small>','均值 ¥128.7 —— 右偏分布，用中位数说话'),
          ('¥9.9–489<small>全距</small>','四分位 ¥59.0–178.5，标准差 ¥96.7'),
          ('27/33/33/26','四价格带款数：0–50 / 50–100 / 100–200 / 200+（元）'),
          ('39/119<small>到手价</small>','促销价占 33% —— "标价/到手价"必须分层比较')])
    + '<div class="chiprow"><span class="chip s">0–50 元 27 款 · 多为小样组合</span><span class="chip s">50–100 元 33 款 · 大众主流带</span><span class="chip s">100–200 元 33 款 · 品牌正装</span><span class="chip s">200+ 元 26 款 · 高端/进口</span></div>',
    foot=FT('真实数据 · products_clean.csv（可复算）', '考纲挂钩：第 6 章 单变量分析（集中度与比较）')))
A.append(sec('03 · 供给端发现', '发现② 渠道<em>垄断</em>价格带',
    table([['价格带','专营店','品牌旗舰','海外专营','苏宁自营'],
           ['0–50 元','10','3','0','14'],['50–100 元','14','0','5','14'],
           ['100–200 元','6','0','10','17'],['200 元以上','0','0','17','9']],
          hl={(4,2),(4,3)})
    + '<div class="vtrack"><div class="vmark" style="left:36.5%"></div></div><div class="vlabels"><span>0</span><span>0.2 弱</span><span>0.4 中等</span><span>0.6 强</span><span>1</span></div>',
    note='χ²=47.5（df=9），<b>Cramér V=0.365</b>（0.3–0.5 中等偏强）：海外专营 32 款中 27 款在 100 元以上（84%），200+ 价位带 65% 由其占据；国内专营店 30 款全部 <100 元 —— <b>渠道选择本身就是价格信号</b>，跨渠道直接比价会系统性误判。', foot=FT('真实数据 · stats_real.json（含交叉表）', '考纲挂钩：第 8 章 双变量关联分析（列联/卡方）')))
A.append(sec('03 · 供给端发现', '发现③ 宣称<em>同质</em>，焦虑话术不在商品层',
    bars([('隔离',69,'','69 款 · 58%'),('清爽',28,'','28 款'),('防水',17,'','17 款'),('美白',13,'a2','13 款'),('敏感肌',11,'a2','11 款'),('补水',10,'','10 款'),('男士',8,'','8 款'),('儿童',6,'','6 款'),('抗老',0,'','0 款')])
    + '<div class="chiprow"><span class="chip s">SPF50 系宣称 45%（54/119）</span><span class="chip s">PA++++ 仅 8%（10/119）</span><span class="chip s w">"抗老"宣称 = 0</span><span class="chip s">标题即广告位：参数与话术混排</span></div>',
    note='<b>参数同质 → 差异化挤进肤感/场景话术；焦虑话术的层位在社媒种草层而非商品标题层。</b>这一供给侧证据反过来收窄了 H2 的作用场景，让问卷的 E 模块更有针对性。', foot=FT('真实数据 · 标题＋卖点词频（清洗脚本可复算）', '考纲挂钩：第 6 章 结构分析 ＋ 第 2 章 数据收集')))
A.append(sec('04 · 需求端发现', '模拟演示数据 n=385',
    '<div class="banner">⚠️ <b>本页全部为标注隔离的模拟演示数据</b>（生成规则公开、种子 42，仅演示分析链路）；真实问卷 11-08 起回收后整章替换重算，不作为任何结论。</div>'
    + kpis([('r=0.352','H2 焦虑 ↔ 社媒信任 —— 支持'),
            ('r=0.485','H3 理解门槛 ↔ 参数信任 —— 支持'),
            ('3.00→4.29','H4 ¥89/159/259 三档品质感知单调上升 —— 支持'),
            ('<span class="warn">未支持</span>','H1 参数信任 3.14 vs 社媒使用 2.61（t=9.86）')])
    + '<div class="chiprow"><span class="chip s">量表信度 α=0.911–0.942（模拟题项结构使然）</span><span class="chip s">k-means k=3：氛围型 149 / 参数型 140 / 低卷入 96</span><span class="chip s w">方法论点：分析不必然验证假设</span></div>',
    foot=FT('模拟演示 · gen_survey_sim.py（种子 42 可复算）', '考纲挂钩：第 6/8 章 ＋ 第 10 章 聚类')))
A.append(sec('04 · 需求端发现', '人群画像（k-means，k=3）',
    cards([
        ('氛围型 · 149 人', '社媒信任 <b>3.83</b> 最高、广告 3.61、参数 3.30 —— 种草层主受众<br><b>治理与教育重点人群</b>'),
        ('参数型 · 140 人', '参数信任 <b>3.59</b>、社媒仅 2.64 —— 成分党/备案党<br><b>信息素养较高的理性层</b>'),
        ('低卷入型 · 96 人', '三维均低（2.25–2.94）—— 信息回避或低涉入<br><b>升级潜力人群</b>'),
    ]),
    note='三类画像来自三维信任的标准化 k-means；正式问卷回收后同一份代码直接出真实画像与人群规模。', foot=FT('模拟演示 · stats_sim.json', '考纲挂钩：第 10 章 多变量分析（聚类）')))
A.append(sec('05 · 结论与建议', '四类受众，四个<em>动作</em>',
    cards([
        ('消费者','按渠道分层比价；把备案查询（国妆特字）作为<b>零成本验证动作</b>；对种草层焦虑话术保持警觉', '对应交付：报告 §7'),
        ('品牌','参数同质化下，差异化转向<b>合规、具体</b>的场景沟通；宣称与备案一致本身就是信任资产', '对应交付：RQ4 核查表'),
        ('平台 / 监管','软广标注治理重点在<b>种草层</b>；热度排序与品质信号解耦展示（ρ=−0.156：热度≠品质）', '对应交付：发现②③'),
        ('方法贡献','供给端爬取 × 需求端问卷双源互证；全流程 AI 协同且<b>留痕可审计</b>', '对应交付：附录A＋数据包'),
    ]),
    foot=FT('详见 07-分析报告v1.md §5', '考纲挂钩：第 5 章 调查报告撰写')))
A.append(sec('06 · 局限与声明', '把边界<em>说清楚</em>',
    cards([
        ('供给端局限','单平台 · 单关键词 · 单时点；SPF/PA 为标题宣称，备案一致性核查进行中；品牌字段粗解析'),
        ('需求端局限','本版为模拟演示数据，外推无效；正式版待真人问卷（11-08 起回收 ≥460）'),
        ('真实度红线','AI 不生成任何原始数据；模拟数据四处标注隔离；AI 全程留痕（附录A）'),
    ]) + '<div class="bigend" style="margin-top:26px">谢谢！欢迎提问</div>',
    foot=FT('附录：A AI说明 · B 文献 · C 隐私 · D 变量 · QA预案', '格式基准：十六届省赛口径（十七届以正式通知为准）')))
A_html = f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>答辩PPT · 校赛模拟版</title><style>{CSS}</style></head><body><div id="bar"></div><div id="meta">防晒霜信息信任 · 校赛模拟版</div><div id="cnt">1 / {len(A)}</div>' + ''.join(f'<section class="slide{" cover" if i==0 else ""}">{s}</section>' for i, s in enumerate(A)) + f'<script>{JS}</script></body></html>'
open('答辩PPT-校赛版.html','w').write(A_html)

# ═══════════ Deck B 分享会版（16页·高密度） ═══════════
B = []
B.append(cover('一个防晒霜课题的<br>全流程演练复盘','AI 主跑 × 人工把关 · 从选题到校赛材料包 · 跑给全队看的"模拟考"',
    ['第十七届正大杯', '模拟考彩排', '8 环节 × 考纲 10 章', '2026-11-03 · 40 min'],
    '分享人：韩之凡　｜　文件索引：选题/防晒霜-审美焦虑与消费信息信任/'))
B.append(sec('WHY', '为什么做这次演练', cards([
    ('会议方向落地','10-28 会议：把 AI 能力用到<b>交付过程</b>中，而不是死磕落地结果 —— 这次是实打实跑了一遍'),
    ('考纲＝流程','网考 10 章 ≈ 项目全流程：概述/方案/问卷/抽样/采集/清洗/分析/报告，<b>跑项目＝把 10 章全实操</b>'),
    ('跑给全队看','终点是"校赛要交的全套材料"：报告 docx / PPT / 附录 / QA 预案，<b>每人可复用同一条流水线</b>'),
]), foot=FT('方向来源：2026-10-28 会议纪要', '对照：网考提纲 10 章章节表')))
B.append(sec('MAP', '全流程地图：8 环节 × 考纲 10 章',
    table([['环节','考纲章节','交付物','状态'],['①概述','第1章','01 市场调查概述','✅'],['②方案','第3章','02 调查方案（含抽样 n≈385）','✅'],['③问卷','第4章','06 问卷终稿 28 题','✅'],['④抽样','第7章','样本量公式＋发放计划 ≥460','✅'],['⑤采集','第2章','真实 119 商品（正式采集01）','✅'],['⑥清洗','第5章','clean CSV＋stats_real.json','✅'],['⑦分析','第6/8/9/10章','描述/卡方/相关/聚类＋报告','✅'],['⑧交付','第5章','报告/PPT×2/看板/材料包','✅']]),
    foot=FT('一套流程三份收益：备考 × 作品 × 方法论', '文件：00-全流程方案 §二 映射表')))
B.append(sec('STEP 1–2', '怎么把"感觉"变成<em>可回答的问题</em>',
    cards([
        ('痛点 → 问题','审美焦虑 / 信息门槛 / 推荐影响 / 价格偏差 → 1 个总问题 ＋ 4 个子问题（RQ1–RQ4）'),
        ('假设从理论长出来','信息不对称 · ELM 双路径 · 信息源可信度 · 社会比较 · 价格—感知质量 → H1–H5'),
        ('先立标准再挖题','与选题池 v2"获奖基因对标"同源：<b>标准先行，不拍脑袋</b>'),
    ]), foot=FT('文件：01 概述 · 02 方案', '考纲挂钩：第 1、3 章')))
B.append(sec('STEP 3–4', '题项从假设<em>长出来</em>',
    cards([
        ('C 模块三维度','参数 / 宣传 / 社媒信任各 4 题 ↔ RQ1 信任结构（可做信度与因子）'),
        ('E·F·G 各管一个假设','焦虑简版 5 题 ↔ H2；理解门槛 ↔ H3；价格情境 ↔ H4'),
        ('样本量现场算','n = z²p(1−p)/e² = 1.96²×0.25/0.05² ≈ 385 → 按 85% 有效率发放 ≥460'),
    ]), foot=FT('文件：06 问卷终稿（28 题·可直接发放）', '考纲挂钩：第 4 章 问卷与量表 ＋ 第 7 章')))
B.append(sec('STEP 5 · 采集', '故事一：<em>脚本秒采</em>',
    kpis([('30/30','静态字段一次解析（curl＋python）'),('119/119','滚动触发懒加载后全字段到手'),
          ('3 份','原始 HTML / JSON / 脚本全部归档可复跑')]),
    '字段清单：标题 · 卖点 · 价格（标价/到手价）· 店铺类型 · 评价数 · SPF/PA 宣称 · URL ＋ 时间戳 —— 03 数据采集字典逐字段落地', foot=FT('文件：数据/正式采集01-2026-10-30/', '考纲挂钩：第 2 章 数据收集')))
B.append(sec('STEP 5 · 采集', '故事二：<em>反爬兜底</em>（现场演示位）',
    cards([
        ('撞墙','价格接口三种姿势全被拒："请求非法"（原始响应留痕 raw-suning-price.jsonp）'),
        ('换路','浏览器渲染 ＋ 滚动触发懒加载 → 价格 29/30 → 119/119'),
        ('留痕','每次尝试的原始响应都存档，失败也有记录，可审计'),
    ]),
    'takeaway：AI 碰壁会自己换路，但每一步留痕 —— 这就是会议说的"AI 用在交付过程"。　★ 现场演示：数据看板 ＋ 价格列前后对比'))
B.append(sec('REDLINE', '数据真实度三条<em>红线</em>', cards([
    ('不生成数据','AI 不生成任何原始数据：问卷必须真人填、商品必须真采'),
    ('显著标注','模拟演示数据四处标注隔离：文件名 / CSV 列 / 报告 / 看板'),
    ('全程留痕','AI 参与按日期记档于 资料/AI使用记录/，提交时按大赛要求脱敏导出'),
])))
B.append(sec('STEP 6–7', '清洗与分析：<em>统计量要会读</em>', cards([
    ('pandas 标准化','去重 · 价格数值化 · 评价数换算（1.2万+→12000）· 店铺分类 · SPF/PA 提取'),
    ('右偏分布','中位数 ≠ 均值：¥99.9 vs ¥128.7 —— 报告用中位数说话'),
    ('方法选对','类别变量 → χ²＋Cramér V；序变量 → Spearman；均数对比 → 配对 t；降维 → k-means'),
]), foot=FT('文件：clean_formal01.py · stats_real.json', '考纲挂钩：第 5/6 章')))
B.append(sec('真实发现 ①', '渠道<em>垄断</em>价格带',
    table([['价格带','专营店','品牌旗舰','海外专营','苏宁自营'],
           ['0–50 元','10','3','0','14'],['50–100 元','14','0','5','14'],
           ['100–200 元','6','0','10','17'],['200 元以上','0','0','17','9']],
          hl={(4,2),(4,3)}),
    'χ²=47.5（df=9），Cramér V=0.365：海外专营垄断 200+ 价位（17/26）；国内专营店全部 <100 元 —— 启示：<b>跨渠道直接比价会系统性误判</b>。', foot=FT('真实数据 · stats_real.json', '考纲挂钩：第 8 章 双变量列联分析')))
B.append(sec('真实发现 ②', '宣称同质 ＋ <em>抗老=0</em>',
    bars([('隔离',69,'','69 款 · 58%'),('清爽',28,'','28 款'),('防水',17,'','17 款'),('美白',13,'a2','13 款'),('敏感肌',11,'a2','11 款'),('抗老',0,'','0 款')])
    + '<div class="chiprow"><span class="chip s">SPF50 系 45%</span><span class="chip s">PA++++ 仅 8%</span><span class="chip s w">抗老宣称 0 款</span><span class="chip s">→ 焦虑话术在种草层，不在商品层</span></div>',
    note='反推 H2 的作用层位 —— 问卷 E 模块因此更有针对性。这个发现同时是<b>新命题</b>：下一步补采社媒数据验证。', foot=FT('真实数据 · 标题＋卖点词频', '考纲挂钩：第 6 章 结构分析')))
B.append(sec('需求侧 · 模拟演示', 'H1 被<em>打脸</em>，是好事',
    kpis([('r=0.352','H2 支持'),('r=0.485','H3 支持'),('单调↑','H4 支持'),('<span class="warn">未支持</span>','H1：3.14 vs 2.61（t=9.86）')]),
    '教训：分析不必然验证假设 —— 真数据同样会打脸，这正常。α=0.911–0.942（模拟结构使然，真数据不会这么高）。', foot=FT('模拟演示 · stats_sim.json', '考纲挂钩：第 6/8 章')))
B.append(sec('画像', 'k-means <em>三型人群</em>', cards([
    ('氛围型 · 149 人','社媒 3.83 最高 —— 种草层主受众，软广治理重点'),
    ('参数型 · 140 人','参数 3.59、社媒 2.64 —— 成分党，认备案和检测'),
    ('低卷入型 · 96 人','三维全低 2.25–2.94 —— 信息回避，升级潜力人群'),
]), foot=FT('模拟演示 · 同一份代码正式数据直接复用', '考纲挂钩：第 10 章 聚类分析')))
B.append(sec('STEP 8', '交付物<em>全家福</em>', cards([
    ('文档线','调查报告 docx（校赛匿名格式）· 一页项目说明 · 问卷终稿 28 题'),
    ('演示线','答辩 PPT 校赛版 · 分享会版（pptx＋html 双格式）· 数据看板'),
    ('数据线','真实 119 商品包 · 模拟问卷包（标注隔离）· 全部脚本可复跑'),
    ('合规线','承诺书/报名表（模拟）· 附录 A–D · AI 使用记录 · QA 预案 12 问'),
]), foot=FT('文件：08-校赛模拟材料包/（本目录）', '考纲挂钩：第 5 章 报告撰写')))
B.append(sec('REUSE', '队友怎么复用这条<em>流水线</em>', cards([
    ('永彩洁','"素颜霜×知识点"概述＋数据收集方案 → 套 01/02 模板，换品类即可；前四章笔记正好当理论底座'),
    ('多啦酱','方法链路（假设→量表→抽样→分析）直接迁移到社会调查方向；学术问题对接口'),
    ('卢雨婷','AI 工具路线接 05：采集脚本 / 文本标注候选 / 看板；"问卷为辅、爬虫为主"口径已验证'),
    ('大一 A','创新视角加在 E/F 模块题项与人群切分上；接龙任务可按同款流水线跑'),
]), foot=FT('每人认领的任务都能挂进同一套流程', '交叉学习：11-01~03 互看成果')))
B.append(sec('NEXT', '下一步', cards([
    ('11-01 24:00','DDL：交接龙文件包（00–08 ＋ 两个数据包）'),
    ('11-01~07','知识赛优先：每人考过（≥60 分，可考 2 次取高；模拟考到 11-10）'),
    ('11-08~18','真人问卷回收 ≥460 → 报告需求侧整体替换重算'),
    ('之后','备案核验（国妆特字）· 京东对照源 · 社媒层补采 · 访谈'),
])))
B.append(sec('Q&A', '', '<div class="bigend">Q&amp;A · 谢谢！</div>'
    + '<div class="sub" style="margin-top:20px">全部文件：选题/防晒霜-审美焦虑与消费信息信任/　·　数据可复算：脚本＋原始存档全归档　·　留痕：资料/AI使用记录/</div>'))
B_html = f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>分享会PPT · 全流程复盘（40min）</title><style>{CSS}</style></head><body><div id="bar"></div><div id="meta">防晒霜全流程复盘 · 分享会版</div><div id="cnt">1 / {len(B)}</div>' + ''.join(f'<section class="slide{" cover" if i==0 else ""}">{s}</section>' for i, s in enumerate(B)) + f'<script>{JS}</script></body></html>'
open('分享会PPT-全流程复盘版.html','w').write(B_html)
print('ok: 校赛版', len(A), '页 | 分享会版', len(B), '页（高密度版）')
