# ⚠️ 模拟数据生成器：本目录全部数据为【模拟演示数据】，非真实调查数据，仅用于流程演练
# 生成规则完全透明可复算：固定种子 42，按 H1-H5 假设结构生成
import numpy as np, pandas as pd, json
rng=np.random.default_rng(42)
n=385
clip=lambda a: np.clip(a,1,5)
gender=rng.binomial(1,0.55,n)                      # 1=女
student=rng.binomial(1,0.6,n)                      # 1=学生
sensitive=rng.binomial(1,0.25,n)
anxiety=clip(rng.normal(3.3,0.9,n))                # 审美焦虑
underst=clip(rng.normal(3.0,1.0,n))                # 理解门槛（越高越懂）
param_trust=clip(2.2+0.35*underst+rng.normal(0,0.7,n))          # H3
ad_trust=clip(rng.normal(3.0,0.8,n))
social_trust=clip(1.4+0.35*anxiety+0.2*ad_trust+rng.normal(0,0.7,n))  # H2
param_use=clip(rng.normal(3.5,0.8,n))
social_use=clip(0.8+0.3*social_trust+0.25*anxiety+rng.normal(0,0.7,n))  # H1 行为面
price_tier=rng.choice([89,159,259],p=[0.35,0.4,0.25],size=n)
q_percep=np.where(price_tier==89,rng.normal(3.0,0.8,n),
          np.where(price_tier==159,rng.normal(3.6,0.7,n),rng.normal(4.2,0.6,n)))  # H4
df=pd.DataFrame(dict(s_gender=gender,s_student=student,s_sensitive=sensitive,
 s_anxiety=anxiety,s_understanding=underst,
 s_param_trust=param_trust,s_ad_trust=ad_trust,s_social_trust=social_trust,
 s_param_use=param_use,s_social_use=social_use,s_price_tier=price_tier,s_quality_percep=np.clip(q_percep,1,5)))
# 量表题项（每维度4题=共同因子+噪声），供信度/因子分析演示
for base,name in [('param_trust','pt'),('social_trust','st'),('ad_trust','at'),('anxiety','ax')]:
    for i in range(1,5):
        df[f'sim_{name}{i}']=clip(df[f's_{base}']+rng.normal(0,0.45,n))
df.insert(0,'data_flag','模拟演示数据-非真实调查-仅流程演练')
df.to_csv('survey_SIMULATED_n385.csv',index=False,encoding='utf-8-sig')

def pearson(a,b):
    a,b=a-a.mean(),b-b.mean(); return float((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()))
def alpha(items):
    v=items.var(ddof=1).sum(); tot=items.sum(1).var(ddof=1); k=items.shape[1]
    return round(k/(k-1)*(1-v/tot),3)
def ttest(a,b):
    d=a-b; return round(float(d.mean()/(d.std(ddof=1)/np.sqrt(len(d)))),2)
S=dict(n=n,
 H1=dict(param_trust_mean=round(float(param_trust.mean()),2), social_use_mean=round(float(social_use.mean()),2),
   param_use_mean=round(float(param_use.mean()),2), paired_t_param_vs_social_use=ttest(param_trust,social_use)),
 H2_r_anxiety_social=round(pearson(anxiety,social_trust),3),
 H3_r_understanding_param=round(pearson(underst,param_trust),3),
 H4=dict(zip([89,159,259],[round(float(q_percep[price_tier==t].mean()),2) for t in [89,159,259]])),
 alpha=dict(param=round(alpha(df[[f'sim_pt{i}' for i in range(1,5)]]),3),
            social=round(alpha(df[[f'sim_st{i}' for i in range(1,5)]]),3),
            ad=round(alpha(df[[f'sim_at{i}' for i in range(1,5)]]),3),
            anxiety=round(alpha(df[[f'sim_ax{i}' for i in range(1,5)]]),3)))
X=df[['s_param_trust','s_ad_trust','s_social_trust']].to_numpy()
X=(X-X.mean(0))/X.std(0)
c=X[rng.choice(n,3,replace=False)]
for _ in range(30):
    lab=((X[:,None,:]-c[None])**2).sum(2).argmin(1)
    c=np.array([X[lab==k].mean(0) if (lab==k).any() else c[k] for k in range(3)])
cents=df[['s_param_trust','s_ad_trust','s_social_trust']].to_numpy()
S['kmeans3']=dict(sizes=[int((lab==k).sum()) for k in range(3)],
 centroids=[[round(float(cents[lab==k,j].mean()),2) for j in range(3)] for k in range(3)])
json.dump(S,open('stats_sim.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(S,ensure_ascii=False,indent=1))
