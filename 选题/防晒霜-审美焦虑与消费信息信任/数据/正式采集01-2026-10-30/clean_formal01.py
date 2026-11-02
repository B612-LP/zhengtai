# 正式采集01 清洗脚本：浏览器原始 JSON → 标准商品表 + 统计摘要（真实数据）
import json, re, pandas as pd, numpy as np
BASE='选题/防晒霜-审美焦虑与消费信息信任/数据/正式采集01-2026-10-30'
raw=json.load(open(f'{BASE}/products_raw_browser.json'))
df=pd.DataFrame(raw['rows'])
df['product_id']=df['url'].str.extract(r'/(\d+)\.html')
df=df.drop_duplicates('product_id').copy()
df['price_cny']=pd.to_numeric(df['price'].str.extract(r'([\d.]+)')[0],errors='coerce')
df['price_type']=np.where(df['price'].str.contains('到手',na=False),'到手价',np.where(df['price_cny'].notna(),'标价','未取到'))
def evalnum(s):
    if not isinstance(s,str): return np.nan
    s=s.replace('评价','').strip()
    if '万' in s: return float(s.replace('万+','').replace('万',''))*10000
    return pd.to_numeric(re.sub(r'\D','',s) or 0,errors='coerce')
df['evaluate_num']=df['evaluate'].map(evalnum)
df['shop_type']=np.where(df['shop'].str.contains('自营'),'苏宁自营',
    np.where(df['shop'].str.contains('海外'),'海外专营',np.where(df['shop'].str.contains('旗舰'),'品牌旗舰','专营店')))
txt=df['title']
df['spf_claim']=txt.str.extract(r'(SPF\s?\d*\+?)',flags=re.I)[0].str.replace(' ','',regex=False).str.upper().fillna('')
df['pa_claim']=txt.str.extract(r'(PA\+{2,4})')[0].fillna('')
df['brand_raw']=txt.str.split(r'[\s(（]',n=1,regex=True).str[0].str.strip()
for kw in ['美白','抗老','清爽','敏感肌','儿童','补水','隔离','防水','男']:
    df['claim_'+kw]=txt.str.contains(kw).astype(int)
df['price_band']=pd.cut(df['price_cny'],[0,50,100,200,10000],labels=['0-50','50-100','100-200','200+'])
out=df[['product_id','brand_raw','title','spf_claim','pa_claim','price_cny','price_type','shop','shop_type','evaluate_num']+[c for c in df.columns if c.startswith('claim_')]+['price_band','url']]
out.insert(0,'data_flag','真实公开数据-苏宁搜索页')
out.to_csv(f'{BASE}/products_clean.csv',index=False,encoding='utf-8-sig')
p=df['price_cny'].dropna()
S=dict(
 n=int(len(df)), price_cov=int(p.notna().sum()),
 price_median=float(p.median()), price_mean=round(float(p.mean()),1), price_std=round(float(p.std()),1),
 price_min=float(p.min()), price_max=float(p.max()),
 price_q25=round(float(p.quantile(0.25)),1), price_q75=round(float(p.quantile(0.75)),1),
 bands={str(k):int(v) for k,v in df['price_band'].value_counts().sort_index().items()},
 daoshou=int((df['price_type']=='到手价').sum()),
 spf50=int(df.apply(lambda r:'SPF50' in (str(r['spf_claim'])+str(r['title'])).upper(),axis=1).sum()),
 pa4=int(df.apply(lambda r:'PA++++' in (str(r['pa_claim'])+str(r['title'])),axis=1).sum()),
 zy=int((df['shop_type']=='苏宁自营').sum()),
 shop_types={str(k):int(v) for k,v in df['shop_type'].value_counts().items()},
 claims={kw:int(df['claim_'+kw].sum()) for kw in ['美白','抗老','清爽','敏感肌','儿童','补水','隔离','防水','男']},
 top_brands={str(k):int(v) for k,v in df['brand_raw'].value_counts().head(8).items()},
 spearman_price_eval=round(float(df[['price_cny','evaluate_num']].corr(method='spearman').iloc[0,1]),3) if df['price_cny'].notna().sum()>10 else None,
)
# 交叉：价格带 × 店铺类型 卡方
ct=pd.crosstab(df['price_band'],df['shop_type'])
obs=ct.values; obs=obs[obs.sum(1)>0][:,obs.sum(0)>0]
exp=np.outer(obs.sum(1),obs.sum(0))/obs.sum()
chi2=float(((obs-exp)**2/exp).sum()); k=obs.shape; n=obs.sum()
cramerv=float(np.sqrt(chi2/(n*(min(k)-1))))
S['cross_band_shop']={'chi2':round(chi2,1),'df':int((k[0]-1)*(k[1]-1)),'cramers_v':round(cramerv,3),'table':{str(i):{str(j):int(ct.loc[i,j]) for j in ct.columns} for i in ct.index}}
json.dump(S,open(f'{BASE}/stats_real.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(S,ensure_ascii=False,indent=1)[:2200])
