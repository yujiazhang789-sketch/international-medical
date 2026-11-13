"""鼎优乐中国国际医疗政策证据看板。

运行：pip install -r requirements.txt && streamlit run app.py
数据：与 app.py 同目录的 dingyoule_data.csv，可用表格软件维护。
"""
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="鼎优乐｜国际医疗政策证据地图", page_icon="🏥", layout="wide")
st.markdown("""<style>
.stApp {background:#f5f8fc;color:#17324f}
.block-container {padding-top:2rem}
h1,h2,h3 {color:#0065a8}
[data-testid="stMetric"] {background:white;border:1px solid #dce8f4;border-radius:12px;padding:14px}
</style>""", unsafe_allow_html=True)

PROVINCES = "北京 天津 河北 山西 内蒙古 辽宁 吉林 黑龙江 上海 江苏 浙江 安徽 福建 江西 山东 河南 湖北 湖南 广东 广西 海南 重庆 四川 贵州 云南 西藏 陕西 甘肃 青海 宁夏 新疆".split()
DATA = Path(__file__).with_name("dingyoule_data.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA, dtype=str).fillna("")
    for col in df.columns:
        df[col] = df[col].str.strip()
    return df

df = load_data()
st.title("鼎优乐® 中国国际医疗政策证据地图")
st.caption("2026-11-13 核查版本 · 政策支持 ≠ 产品入院 ≠ 医保或商保支付 · 仅展示可追溯公开证据")

with st.container(border=True):
    st.warning("本工具不宣称已完成全国逐院药品准入排查。31个省级行政区全部纳入核查台账，但尚无已核验政策的地区显示为『待核实』，绝不自动标为『不支持』。")

c1,c2,c3,c4=st.columns(4)
c1.metric("内地省级地区",len(PROVINCES))
c2.metric("已录入证据",len(df))
c3.metric("有地方层级证据的省级地区",df.loc[df.level.isin(["省级","城市","医院"]),"province"].nunique())
c4.metric("鼎优乐院内准入已公开核证",int((df.product_verified=="是").sum()))

tab1,tab2,tab3,tab4=st.tabs(["全国政策台账","医院与支付路径","政策原文证据","分析框架与更新说明"])
with tab1:
    coverage=pd.DataFrame({"省级地区":PROVINCES})
    grouped=df[df.province.isin(PROVINCES)].groupby("province").agg(政策证据数=("id","count"),市县与医院=("city",lambda s:"、".join(sorted(set(x for x in s if x))))).reset_index()
    coverage=coverage.merge(grouped,how="left",left_on="省级地区",right_on="province").drop(columns="province")
    coverage["政策证据数"]=coverage["政策证据数"].fillna(0).astype(int)
    coverage["核查状态"]=coverage["政策证据数"].apply(lambda n:"有部分政策证据（非全面核实）" if n else "待核实")
    coverage["市县与医院"]=coverage["市县与医院"].fillna("")
    selected=st.multiselect("筛选省级地区",PROVINCES,default=[])
    st.dataframe(coverage[coverage["省级地区"].isin(selected)] if selected else coverage,hide_index=True,use_container_width=True)
    st.caption("政策证据数只代表纳入本库的原文条目，不代表政策覆盖率或产品准入率。")
    st.download_button("下载31省区市核查台账 CSV",coverage.to_csv(index=False).encode("utf-8-sig"),"province_review.csv","text/csv")
with tab2:
    st.subheader("真实医院证据（不等于鼎优乐准入）")
    hospital=df[df.level=="医院"]
    st.dataframe(hospital[["province","city","hospital","topic","evidence","implication","product_verified","source_url"]],hide_index=True,use_container_width=True,column_config={"source_url":st.column_config.LinkColumn("官方来源")})
    st.info("院内产品准入须由医院药学部/抗菌药管理部门核实：药品供应目录、处方级别、ICU/感染科使用权限、采购渠道、库存和药费支付。")
    st.markdown("**建议核查字段**：医院名称｜国际医疗部是否有住院/ICU服务｜鼎优乐是否院内目录｜采购方式｜医院抗菌药分级｜临采机制｜实际库存｜商业险直付协议｜药品是否理赔｜最近核验日期｜核验人｜证据截图/链接。")
with tab3:
    q=st.text_input("检索政策标题、城市、医院和条款")
    region=st.selectbox("地区",["全部"]+sorted(set(df.province)-{""}))
    level=st.selectbox("层级",["全部","国家","省级","城市","医院"])
    show=df.copy()
    if region!="全部":show=show[show.province==region]
    if level!="全部":show=show[show.level==level]
    if q:show=show[show.astype(str).apply(lambda x:x.str.contains(q,case=False,regex=False)).any(axis=1)]
    st.dataframe(show[["id","level","province","city","hospital","topic","policy_title","publisher","evidence","implication","status","source_url"]],hide_index=True,use_container_width=True,column_config={"source_url":st.column_config.LinkColumn("打开官方原文")})
    st.download_button("下载当前筛选证据 CSV",show.to_csv(index=False).encode("utf-8-sig"),"dingyoule_filtered.csv","text/csv")
with tab4:
    st.markdown("""### 四道独立判断门槛
1. **政策门槛**：国际医疗及药品采购有关政策存在吗？
2. **药事门槛**：医院允许采购、列入供应目录，并符合抗菌药物分级吗？
3. **临床门槛**：患者符合获批适应证，检验和处方流程可落实吗？
4. **支付门槛**：患者自费、基本医保、商业险直付和药品责任范围分别是什么？

### 维护规则
- 每行只放一条可独立核验的事实，必须填写 `source_url`、`publisher` 和 `evidence`。
- `product_verified` 只有在医院或官方采购证据**明确指向鼎优乐/舒巴坦钠-度洛巴坦钠**时才能改为「是」。
- 政策发布时间若未从原文核对则留空，不能用网页爬取日期代替。
- 「待核实」不是「无政策」；保险直付也不是所有药品均可理赔。
- 每月复核新增地方政策和医保目录，每季度核实目标医院用药现状。
- 用户自主维护 CSV 即可刷新小程序，避免把销售推测当成政府规定。
""")
    st.download_button("下载全量原始证据 CSV",df.to_csv(index=False).encode("utf-8-sig"),"dingyoule_data.csv","text/csv")
