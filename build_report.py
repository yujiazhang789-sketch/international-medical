"""从可溯源 CSV 生成研究报告 DOCX。"""
import csv
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT=Path(__file__).parent
with (ROOT/'dingyoule_data.csv').open(encoding='utf-8-sig',newline='') as f:
    data=list(csv.DictReader(f))

doc=Document()
sec=doc.sections[0]
sec.top_margin=Inches(.72)
sec.bottom_margin=Inches(.7)
sec.left_margin=Inches(.8)
sec.right_margin=Inches(.8)
styles=doc.styles
styles['Normal'].font.name='Microsoft YaHei'
styles['Normal'].font.size=Pt(9)
styles['Normal'].paragraph_format.space_after=Pt(5)
for h in ['Title','Heading 1','Heading 2']:
    styles[h].font.name='Microsoft YaHei'
    styles[h].font.color.rgb=RGBColor(0,91,153)

doc.add_heading('鼎优乐 中国医院国际医疗政策分析',0)
doc.add_paragraph('全国政策证据与医院支付路径研究｜版本 2026年11月13日')
doc.add_heading('研究结论与适用范围',1)
doc.add_paragraph('本研究将国际医疗政策支持、药品院内准入、临床合理使用、患者支付责任拆成四项独立判断。政策允许发展国际医疗，不等于某医院已经采购鼎优乐；医院拥有商业保险直付服务，也不等于该药受保单保障。')
doc.add_paragraph('数据库覆盖中国内地31个省级行政区的核查框架，但本版本仅对已找到官方原文的地区录入证据。未发现或尚未核验的地区一律标注“待核实”，不等于不存在政策。香港、澳门、台湾不纳入本版本。')
doc.add_heading('产品定位与关键监管逻辑',1)
doc.add_paragraph('鼎优乐®（XACDURO，舒巴坦钠/度洛巴坦钠），用于治疗18岁及以上患者由鲍曼-醋酸钙不动杆菌复合体敏感分离株引起的医院获得性细菌性肺炎和呼吸机相关性细菌性肺炎。辉瑞与再鼎医药于2024年11月宣布中国内地商业化合作。产品信息依据再鼎医药官方网站：https://cn.zailaboratory.com/products/ 以及合作公告：https://zailab.gcs-web.com/zh-hans/news-releases/news-release-details/zaidingyiyaoyuhuiruijiuxinxingkangjunyaowudingyouler-shubatanna')
doc.add_paragraph('国家《抗菌药物临床应用管理办法》规定抗菌药物分级管理、医院供应目录备案、药学部门统一采购及适用的处方管理要求。不得因国际医疗区单独运营而默认豁免。具体是否属于特殊使用级应以当地现行抗菌药物分级目录核实。')
doc.add_heading('地方政策比较',1)
items=[
('上海','2025年国际医疗创新发展政策支持创新药械临床使用，优化药械采购使用政策指导，促进商业保险支付；不能推断鼎优乐实际采购。'),
('北京','2021年国际医疗与特需服务管理规定强调独立区域、规模控制、收费公示；公立医院国际医疗并非无条件扩张。'),
('湖南','2025年特需医疗价格管理文件明确该区域药品耗材不受集中带量采购政策限制，药品仍执行零差率；不免除抗菌药目录管理。'),
('广东深圳','2026年卫生健康工作要点推动国际医疗试点、国际医疗专区和创新药械应用；具体医院产品准入仍待核实。'),
('广东广州','2026年文件支持试点机构对接境外医疗保险与医疗救援；另有官方跨境支付平台发布报道，但不等于鼎优乐可直付。'),
('海南乐城','特许进口药械制度主要针对符合条件的境外临床急需产品；已在境内上市的鼎优乐不能直接据此判定适用特许进口。'),
('浙江','公开自主定价项目文件说明部分特需医疗服务定价安排，不直接决定药品准入或医保支付。'),
]
for place,note in items:
    doc.add_heading(place,2)
    doc.add_paragraph(note)
doc.add_heading('已核实的医院服务案例',1)
doc.add_paragraph('北京协和医院国际医疗部公布商业保险合作直付服务；北京大学国际医院公布国际医疗中心商保就诊说明；北京朝阳医院说明国际医疗部门诊结算系统可处理符合医保政策的费用。这些材料均只证明医院服务或支付流程，不证明鼎优乐药品目录准入和具体保险覆盖。')
doc.add_heading('全国政策证据清单及原文链接',1)
for row in data:
    doc.add_heading(f"{row['id']}  {row['province']} {row['city']}  {row['policy_title']}",2)
    doc.add_paragraph(f"发布方：{row['publisher']}｜证据层级：{row['level']}｜状态：{row['status']}")
    doc.add_paragraph('已核实事实：'+row['evidence'])
    doc.add_paragraph('鼎优乐相关解释：'+row['implication'])
    doc.add_paragraph('官方原文：'+row['source_url'])
doc.add_heading('执行建议与建议新增字段',1)
doc.add_paragraph('院级核查应覆盖国际医疗部实际诊疗范围、是否具备住院和ICU、药品供应目录、特殊采购方式、抗菌药分级与处方权限、临床微生物检测、商业保险直付协议、具体药品给付责任、证据发布日期及复核人。所有“未核实”状态必须保留，不可自动改为“否”。')
doc.add_paragraph('本报告是政策与公开信息研究，不替代医院采购确认、商业保险条款审核或药物临床决策。对外使用时应重新点击原文核实有效性及修订状态。')
out=ROOT/'鼎优乐_全国国际医疗政策分析_20261113.docx'
doc.save(out)
print(out)
