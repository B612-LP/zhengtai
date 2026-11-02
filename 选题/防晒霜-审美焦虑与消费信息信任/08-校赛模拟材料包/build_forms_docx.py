# 参赛承诺书＋报名表（模拟版 docx）
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
doc=Document(); st=doc.styles['Normal']
st.font.name='Times New Roman'; st.font.size=Pt(12)
st._element.rPr.rFonts.set(qn('w:eastAsia'),'宋体')
def p(t,size=12,bold=False,center=False,color=None):
    pp=doc.add_paragraph()
    if center: pp.alignment=1
    r=pp.add_run(t); r.font.size=Pt(size); r.bold=bold
    from docx.shared import RGBColor
    if color: r.font.color.rgb=RGBColor(*color)
    r.font.name='Times New Roman'; r._element.rPr.rFonts.set(qn('w:eastAsia'),'宋体')
def h(t): doc.add_heading(t,level=1)

p('参赛承诺书（模拟演练版）',18,True,True)
p('⚠ 本件为全流程演练用模拟文书；第十七届正式承诺书以校赛通知下发模板为准。',10,True,True,(183,65,14))
p('本团队报名参加第十七届全国大学生市场调查与分析大赛，郑重承诺：',12)
for t in ['一、参赛作品为团队独立完成，调查数据来源于真实调查与公开数据采集，不存在抄袭、剽窃他人成果的行为；',
          '二、问卷数据全部由受访者真实填写，未使用任何人工智能工具生成、伪造或批量填充调查数据；',
          '三、人工智能工具仅用于方案起草、代码编写、文本标注候选与图表制作等过程性环节，全部使用情况已如实记录并随作品提交；',
          '四、报告与演示材料按要求匿名处理，不出现学校、指导老师等身份信息；',
          '五、遵守大赛各项规则与学术规范，数据与受访者隐私保护措施见附录说明；',
          '六、如有违反，愿承担相应后果。']:
    p(t,12)
p('队长签名：________　　成员签名：________________________',12)
p('日期：2026年＿＿月＿＿日',12)
doc.add_page_break()
h('参赛报名表（模拟演练版）')
p('⚠ 正式报名表以校赛通知下发模板为准。',10,True,True,(183,65,14))
tb=doc.add_table(rows=8,cols=4); tb.style='Table Grid'
data=[['队名','____（待定）','课题名称','防晒霜购买中的审美焦虑与消费信息信任'],
 ['队长','韩之凡','联系方式','____'],
 ['成员1','韩之凡','分工','调查设计、数据采集、分析与报告'],
 ['成员2','____（宽）','分工','方法论与统计分析'],
 ['成员3','卢雨婷','分工','AI 工具路线与数据补充'],
 ['成员4','____（大一）','分工','创新视角与问卷修订'],
 ['指导老师','____','学院','____'],
 ['报名日期','2026年＿＿月＿＿日','备注','知识赛通过后进入实践赛']]
for i,row in enumerate(data):
    for j,val in enumerate(row):
        c=tb.cell(i,j); c.text=val
        for pp_ in c.paragraphs:
            for rn in pp_.runs:
                rn.font.size=Pt(10.5); rn.font.name='Times New Roman'
                rn._element.rPr.rFonts.set(qn('w:eastAsia'),'宋体')
doc.save('参赛承诺书与报名表-模拟版.docx')
print('saved 参赛承诺书与报名表-模拟版.docx')
