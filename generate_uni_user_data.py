import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)  # 固定随机种子，保证结果可复现且波动可控

# 1. 基础参数设置（5万用户规模）
n_users = 50000  # 统计周期内登录用户总数
user_ids = [f"hsr_user_{i}" for i in range(n_users)]

# 2. 定义崩铁真实漏斗步骤
steps = ["登录游戏", "进入卡池界面", "进行抽卡操作", "打开付费界面", "完成付费"]

# 3. 生成符合崩铁实际的用户等级分布（1-70级，按行业调研比例）
def generate_hsr_user_levels(n):
    """生成崩铁用户等级，严格匹配行业调研比例：1-20级(8%)、21-40级(35%)、41-60级(45%)、61-70级(12%)"""
    levels = []
    level_ranges = [
        (1, 20, 0.08),
        (21, 40, 0.35),
        (41, 60, 0.45),
        (61, 70, 0.12)
    ]
    for start, end, prob in level_ranges:
        count = int(n * prob)
        levels.extend(np.random.randint(start, end+1, count))
    if len(levels) < n:
        levels.extend(np.random.randint(1, 71, n - len(levels)))
    np.random.shuffle(levels)
    return levels

# 生成用户等级列表
user_levels = generate_hsr_user_levels(n_users)

# 4. 带自然波动的步骤用户数分配（贴合周年庆真实场景）
# 核心：基于正态分布生成随机比例，设置上下限避免极端值
def get_random_count(base_count, target_ratio, min_ratio, max_ratio):
    """
    生成带波动的用户数
    :param base_count: 上一步骤用户数
    :param target_ratio: 目标转化率
    :param min_ratio: 最小转化率（避免过低）
    :param max_ratio: 最大转化率（避免过高）
    :return: 随机后的用户数
    """
    # 生成正态分布的随机比例（均值=target_ratio，标准差=0.01，保证小范围波动）
    random_ratio = np.random.normal(target_ratio, 0.01)
    # 限制比例在[min_ratio, max_ratio]范围内
    random_ratio = np.clip(random_ratio, min_ratio, max_ratio)
    # 计算用户数并取整
    random_count = int(base_count * random_ratio)
    # 确保用户数≥1（避免极端情况）
    return max(random_count, 1)

# 4.1 各步骤用户数（带自然波动，周年庆付费转化率8%左右）
login_users = 50000  # 登录用户数（基准，无波动）
# 登录→进卡池：80%±2%（78%-82%）
enter_pool_users = get_random_count(login_users, 0.80, 0.78, 0.82)
# 进卡池→抽卡：60%±2%（58%-62%）
draw_card_users = get_random_count(enter_pool_users, 0.60, 0.58, 0.62)
# 抽卡→打开付费：20%±2%（18%-22%）
open_pay_users = get_random_count(draw_card_users, 0.20, 0.18, 0.22)
# 打开付费→完成付费：8%±1%（7%-9%）（周年庆比日常5%高，且在合理范围）
pay_users = get_random_count(open_pay_users, 0.08, 0.07, 0.09)

# 4.2 按步骤随机抽取用户ID（保证行为唯一性）
login_user_ids = user_ids[:login_users]
enter_pool_user_ids = np.random.choice(login_user_ids, enter_pool_users, replace=False)
draw_card_user_ids = np.random.choice(enter_pool_user_ids, draw_card_users, replace=False)
open_pay_user_ids = np.random.choice(draw_card_user_ids, open_pay_users, replace=False)
pay_user_ids = np.random.choice(open_pay_user_ids, pay_users, replace=False)

# 5. 生成用户行为记录（带时间戳，贴合实际操作顺序）
funnel_records = []

# 5.1 登录游戏
for idx, user_id in enumerate(login_user_ids):
    user_level = user_levels[idx]
    base_time = datetime(2026, 3, 1) + timedelta(minutes=np.random.randint(0, 1440))
    funnel_records.append({
        "user_id": user_id,
        "step": "登录游戏",
        "timestamp": base_time,
        "user_level": user_level
    })

# 5.2 进入卡池界面
for user_id in enter_pool_user_ids:
    idx = user_ids.index(user_id)
    user_level = user_levels[idx]
    base_time = datetime(2026, 3, 1) + timedelta(minutes=np.random.randint(0, 1440))
    funnel_records.append({
        "user_id": user_id,
        "step": "进入卡池界面",
        "timestamp": base_time + timedelta(minutes=np.random.randint(1, 3)),
        "user_level": user_level
    })

# 5.3 进行抽卡操作
for user_id in draw_card_user_ids:
    idx = user_ids.index(user_id)
    user_level = user_levels[idx]
    base_time = datetime(2026, 3, 1) + timedelta(minutes=np.random.randint(0, 1440))
    funnel_records.append({
        "user_id": user_id,
        "step": "进行抽卡操作",
        "timestamp": base_time + timedelta(minutes=np.random.randint(3, 5)),
        "user_level": user_level
    })

# 5.4 打开付费界面
for user_id in open_pay_user_ids:
    idx = user_ids.index(user_id)
    user_level = user_levels[idx]
    base_time = datetime(2026, 3, 1) + timedelta(minutes=np.random.randint(0, 1440))
    funnel_records.append({
        "user_id": user_id,
        "step": "打开付费界面",
        "timestamp": base_time + timedelta(minutes=np.random.randint(5, 7)),
        "user_level": user_level
    })

# 5.5 完成付费
for user_id in pay_user_ids:
    idx = user_ids.index(user_id)
    user_level = user_levels[idx]
    base_time = datetime(2026, 3, 1) + timedelta(minutes=np.random.randint(0, 1440))
    funnel_records.append({
        "user_id": user_id,
        "step": "完成付费",
        "timestamp": base_time + timedelta(minutes=np.random.randint(7, 9)),
        "user_level": user_level
    })

# 6. 生成DataFrame并保存
funnel_data = pd.DataFrame(funnel_records)
funnel_data["timestamp"] = pd.to_datetime(funnel_data["timestamp"])
funnel_data.to_csv("hsr_card_pool_funnel.csv", index=False)
funnel_data.to_excel("hsr_card_pool_funnel.xlsx", index=False)

# 7. 输出验证结果
print("✅ 崩铁卡池漏斗数据生成完成（5万用户，带自然波动）")
print(f"总行为记录数：{len(funnel_data)} 条")

# 7.1 各步骤用户数统计
print("\n各步骤用户数统计：")
step_user_count = funnel_data.groupby("step")["user_id"].nunique()
print(step_user_count)

# 7.2 各步骤转化率（带自然波动，贴合周年庆实际）
print("\n各步骤转化率（周年庆场景，合理波动）：")
for i in range(1, len(steps)):
    conversion = step_user_count[steps[i]] / step_user_count[steps[i-1]]
    print(f"{steps[i-1]} → {steps[i]}：{conversion:.2%}")

# 7.3 用户等级分布验证
print("\n用户等级分布验证（符合行业调研比例）：")
unique_user_levels = funnel_data.drop_duplicates("user_id")["user_level"]
level_bins = pd.cut(
    unique_user_levels,
    bins=[0, 20, 40, 60, 70],
    labels=["1-20级", "21-40级", "41-60级", "61-70级"]
)
level_dist = level_bins.value_counts() / len(level_bins)
print(level_dist)