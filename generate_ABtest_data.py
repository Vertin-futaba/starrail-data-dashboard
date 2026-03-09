import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)  # 固定随机种子，保证可复现

# 1. 基础参数调整（5万用户，匹配之前的用户分层数据规模）
n_users = 50000  # 崩铁全服周年庆活动触达用户数
user_ids = [f"hsr_user_{i}" for i in range(n_users)]

# 2. 随机分组（对照组:实验组 = 1:1）
groups = np.random.choice(["control", "test"], size=n_users, p=[0.5, 0.5])

# 3. 生成核心指标（删除服务器/用户等级字段，聚焦付费核心指标）
## 3.1 付费转化率（对照组8%，实验组13%）
conversion = np.where(
    groups == "control",
    np.random.binomial(1, 0.08, n_users),
    np.random.binomial(1, 0.13, n_users)
)

## 3.2 ARPU（人均付费，贴合崩铁礼包档位：68/128/328/648）
# 对照组付费金额分布：68元(60%)、128元(25%)、328元(10%)、648元(5%)
control_arpu = np.where(
    conversion[groups=="control"] == 1,
    np.random.choice([68, 128, 328, 648], size=sum(groups=="control"), p=[0.6, 0.25, 0.1, 0.05]),
    0
)
# 实验组付费金额分布（累计奖励拉动高档位）：68元(45%)、128元(25%)、328元(20%)、648元(10%)
test_arpu = np.where(
    conversion[groups=="test"] == 1,
    np.random.choice([68, 128, 328, 648], size=sum(groups=="test"), p=[0.45, 0.25, 0.2, 0.1]),
    0
)
# 合并ARPU数据
arpu = np.zeros(n_users)
arpu[groups=="control"] = control_arpu
arpu[groups=="test"] = test_arpu
arpu = arpu.round(2)

## 3.3 高价值用户标识（单月充值≥328元，崩铁"重氪用户"定义）
high_value = np.where(arpu >= 328, 1, 0)

## 3.4 7日留存率（对照组40%，实验组58%）
retention_7 = np.where(
    groups == "control",
    np.random.binomial(1, 0.40, n_users),
    np.random.binomial(1, 0.58, n_users)
)

# 4. 生成DataFrame（仅保留核心字段，删除服务器/用户等级）
ab_test_data = pd.DataFrame({
    "user_id": user_ids,
    "group": groups,
    "conversion": conversion,
    "arpu": arpu,
    "high_value": high_value,
    "retention_7": retention_7
})

# 保存为CSV/Excel（兼容看板上传）
ab_test_data.to_csv("hsr_anniversary_ab_test.csv", index=False)
ab_test_data.to_excel("hsr_anniversary_ab_test.xlsx", index=False)

print("✅ 崩铁周年庆A/B测试数据生成完成（5万用户）")
print(f"数据规模：{len(ab_test_data)} 条用户记录")
print("\n核心指标对比：")
print(ab_test_data.groupby("group")[["conversion", "arpu", "high_value", "retention_7"]].mean())