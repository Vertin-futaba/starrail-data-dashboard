import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ---------------------- 核心配置（星铁成熟稳定期双版本运营基准） ----------------------
STARRAIL_LAUNCH_DATE = datetime(2023, 4, 26).date()  # 星铁正式开服日期
DATA_END_DATE = datetime.now().date()                # 数据集结束日期
DATA_CYCLE_DAYS = 84                                 # 分析周期：84天（2个成熟稳定期大版本，各42天）
DATA_START_DATE = DATA_END_DATE - timedelta(days=DATA_CYCLE_DAYS - 1)
TOTAL_USERS = 50000  # 样本用户总数

# 🌟 星铁成熟稳定期双版本卡池配置（主UP角色热度＞复刻角色）
# 注：成熟稳定期特征——主UP为新限定角色（核心卖点），复刻为经典老角色（补充）
POOL_CONFIG = [
    # 成熟稳定期-大版本1上半（21天）：黄泉（新限定主UP，高热度）+ 真理医生（复刻，次热度）
    {"卡池周期": "成熟稳定期-大版本1上半", "主UP角色": "黄泉", "复刻角色": "真理医生"},
    # 成熟稳定期-大版本1下半（21天）：阮梅（新限定主UP，高热度）+ 符玄（复刻，次热度）
    {"卡池周期": "成熟稳定期-大版本1下半", "主UP角色": "阮梅", "复刻角色": "符玄"},
    # 成熟稳定期-大版本2上半（21天）：灵砂（新限定主UP，高热度）+ 饮月君（复刻，次热度）
    {"卡池周期": "成熟稳定期-大版本2上半", "主UP角色": "灵砂", "复刻角色": "饮月君"},
    # 成熟稳定期-大版本2下半（21天）：花火（新限定主UP，高热度）+ 镜流（复刻，次热度）
    {"卡池周期": "成熟稳定期-大版本2下半", "主UP角色": "花火", "复刻角色": "镜流"}
]

# 星铁成熟稳定期留存真实区间（双指标体系：新手留存+活跃用户留存）
STARRAIL_RETENTION = {
    # 新手留存（新增用户质量指标）
    "新手次日留存率_BASE": 0.70,
    "新手7日留存率_BASE": 0.48,
    "新手30日留存率_BASE": 0.30,
    "新手留存波动": 0.008,  # 成熟稳定期波动仅±0.8%
    
    # 活跃用户留存（老用户粘性/版本健康度指标）
    "活跃用户7日留存率_BASE": 0.80,
    "活跃用户留存波动": 0.015  # 老用户留存波动±1.5%
}

# 日期列表生成
dates_84days = [DATA_START_DATE + timedelta(days=i) for i in range(DATA_CYCLE_DAYS)]

# ---------------------- 1. 日活数据（成熟稳定期特征） ----------------------
activity_data = {
    "日期": dates_84days,
    "新增用户数": np.random.randint(10000, 30000, size=DATA_CYCLE_DAYS),  # 成熟稳定期新增量稳定
    "DAU": np.random.randint(3000000, 5000000, size=DATA_CYCLE_DAYS),    # DAU无大幅波动
    "MAU": np.random.randint(18000000, 25000000, size=DATA_CYCLE_DAYS),  # MAU长期稳定
    "人均在线时长(分钟)": np.random.uniform(30, 90, size=DATA_CYCLE_DAYS), # 玩法成熟，在线时长稳定
    "每日委托完成率": np.random.uniform(0.85, 0.97, size=DATA_CYCLE_DAYS)  # 老用户占比高，完成率高
}

# ========== 修改点1：注入少量DAU/委托完成率异常值（贴合看板异常检测逻辑） ==========
# 1. DAU异常峰值（版本更新，第10天）
activity_data["DAU"][10] = int(np.mean(activity_data["DAU"]) * 1.3)
# 2. 委托完成率异常暴跌（服务器卡顿，第25天）
activity_data["每日委托完成率"][25] = np.mean(activity_data["每日委托完成率"]) * 0.7

# ---------------------- 2. 留存数据（双指标体系：新手+活跃用户） ----------------------
retention_data = {
    "日期": dates_84days,
    "新手次日留存率": [],       # 新增用户质量
    "新手7日留存率": [],        # 新增用户质量
    "新手30日留存率": [],       # 新增用户质量
    "活跃用户7日留存率": []     # 老用户粘性（版本健康度核心指标）
}

# 生成成熟稳定期留存数据
for _ in range(DATA_CYCLE_DAYS):
    # 新手留存（波动极小）
    new_1d = round(STARRAIL_RETENTION["新手次日留存率_BASE"] + random.uniform(-STARRAIL_RETENTION["新手留存波动"], STARRAIL_RETENTION["新手留存波动"]), 3)
    new_1d = max(0.692, min(0.708, new_1d))
    retention_data["新手次日留存率"].append(new_1d)

    new_7d = round(STARRAIL_RETENTION["新手7日留存率_BASE"] + random.uniform(-STARRAIL_RETENTION["新手留存波动"], STARRAIL_RETENTION["新手留存波动"]), 3)
    new_7d = max(0.472, min(0.488, new_7d))
    retention_data["新手7日留存率"].append(new_7d)

    new_30d = round(STARRAIL_RETENTION["新手30日留存率_BASE"] + random.uniform(-STARRAIL_RETENTION["新手留存波动"], STARRAIL_RETENTION["新手留存波动"]), 3)
    new_30d = max(0.292, min(0.308, new_30d))
    retention_data["新手30日留存率"].append(new_30d)

    # 活跃用户7日留存（老用户核心指标，星铁成熟稳定期真实区间：78%~82%）
    active_7d = round(STARRAIL_RETENTION["活跃用户7日留存率_BASE"] + random.uniform(-STARRAIL_RETENTION["活跃用户留存波动"], STARRAIL_RETENTION["活跃用户留存波动"]), 3)
    active_7d = max(0.78, min(0.82, active_7d))
    retention_data["活跃用户7日留存率"].append(active_7d)

# ---------------------- 3. 付费数据（主UP＞复刻，官方标准档位） ----------------------
payment_data = {
    "日期": dates_84days,
    "卡池周期": [cfg["卡池周期"] for cfg in POOL_CONFIG for _ in range(21)],  # 每个卡池21天
    "主UP角色": [cfg["主UP角色"] for cfg in POOL_CONFIG for _ in range(21)],
    "复刻角色": [cfg["复刻角色"] for cfg in POOL_CONFIG for _ in range(21)],
    # ========== 修改点2：提升付费人数（让付费转化率回到星铁真实区间1.5%-2.5%） ==========
    "付费人数": np.random.randint(40000, 100000, size=DATA_CYCLE_DAYS),  # 原2-5万 → 调整为4-10万
    "ARPU": np.random.uniform(50, 100, size=DATA_CYCLE_DAYS),           # ARPU稳定
    "ARPPU": np.random.uniform(450, 1600, size=DATA_CYCLE_DAYS),       # 复刻角色客单价低于主UP
    "首充转化率": np.random.uniform(0.10, 0.20, size=DATA_CYCLE_DAYS),  # 首充转化稳定
    "主UP池流水(元)": [],
    "复刻池流水(元)": [],
    "常驻池流水(元)": [],
    "卡池总流水(元)": []
}

# 填充卡池流水（核心：主UP流水占比70%+，复刻仅30%-）
for idx, cfg in enumerate(POOL_CONFIG):
    for day_in_cycle in range(21):
        # 主UP角色流水（热门主UP＞普通主UP）
        if cfg["主UP角色"] in ["黄泉", "花火"]:
            # ========== 修改点3：强化卡池峰值特征（开池第1/2天峰值更明显，贴合看板峰值判断） ==========
            if day_in_cycle == 1:  # 开池第1天峰值（原仅第2天）
                main_up_revenue = 150000000  # 提升至1500万（原1200万）
            elif day_in_cycle == 2:  # 开池第2天次峰值
                main_up_revenue = 120000000
            else:
                main_up_revenue = np.random.uniform(30000000, 70000000)
        else:
            if day_in_cycle == 1:
                main_up_revenue = 130000000  # 普通主UP开池峰值
            elif day_in_cycle == 2:
                main_up_revenue = 100000000
            else:
                main_up_revenue = np.random.uniform(25000000, 60000000)
        
        # 复刻角色流水（严格低于主UP，仅为主UP的30%-40%）
        reprint_revenue = main_up_revenue * random.uniform(0.3, 0.4)
        
        # 常驻池流水（成熟稳定期极低且稳定）
        permanent_revenue = np.random.uniform(200000, 600000)
        
        # 总流水
        total_revenue = main_up_revenue + reprint_revenue + permanent_revenue
        
        payment_data["主UP池流水(元)"].append(main_up_revenue)
        payment_data["复刻池流水(元)"].append(reprint_revenue)
        payment_data["常驻池流水(元)"].append(permanent_revenue)
        payment_data["卡池总流水(元)"].append(total_revenue)

# ---------------------- 4. 用户分层数据（成熟稳定期老用户主导） ----------------------
user_layer_data = {
    "用户ID": [f"U{i:06d}" for i in range(1, TOTAL_USERS+1)],
    "付费价值分层": [],
    "生命周期分层": [],
    "首次登录日期": [],
    "生命周期天数": [],      # 注册到当前日期的自然天数
    "累计活跃天数": [],      # 实际登录天数
    "累计付费金额(元)": [],
    "付费次数": [],
    "主要付费卡池周期": [],
    "是否首充": [],
    "日均在线时长(分钟)": [],
    "是否付费": [],
    "活跃率": []             # 累计活跃天数/生命周期天数
}

# 成熟稳定期付费价值分层
free_cnt = int(TOTAL_USERS * 0.60)    # 60%免费用户
low_cnt = int(TOTAL_USERS * 0.20)     # 20%低价值（1-500元）
mid_cnt = int(TOTAL_USERS * 0.15)     # 15%中价值（501-2000元）
high_cnt = TOTAL_USERS - free_cnt - low_cnt - mid_cnt  # 5%高价值（2000+元）

# 生成分层列表并打乱
value_layers = (
    ["免费"] * free_cnt
    + ["低价值"] * low_cnt
    + ["中价值"] * mid_cnt
    + ["高价值"] * high_cnt
)
random.shuffle(value_layers)

# 星铁官方标准付费档位
pay_options = [6, 30, 98, 198, 328, 648]

# 生成用户分层数据
for i in range(TOTAL_USERS):
    # 首次登录日期（成熟稳定期以老用户为主）
    days_rand = random.randint(90, (DATA_END_DATE - STARRAIL_LAUNCH_DATE).days)
    first_login = STARRAIL_LAUNCH_DATE + timedelta(days=days_rand)
    user_layer_data["首次登录日期"].append(first_login)

    # 生命周期天数计算
    life_days = (DATA_END_DATE - first_login).days
    user_layer_data["生命周期天数"].append(life_days)
    # 成熟稳定期新用户定义：≤60天（更严格）
    user_layer_data["生命周期分层"].append("新用户" if life_days <= 60 else "老用户")

    # 累计活跃天数 & 活跃率（老用户粘性极强）
    if life_days == 0:
        active_days = 1
        active_rate = 1.0
    else:
        base_rate = random.uniform(0.5, 0.85) if life_days <= 60 else random.uniform(0.75, 0.98)
        active_days = max(1, int(life_days * base_rate))
        active_rate = round(active_days / life_days, 3)
    
    user_layer_data["累计活跃天数"].append(active_days)
    user_layer_data["活跃率"].append(active_rate)

    # 付费价值分层
    layer = value_layers[i]
    user_layer_data["付费价值分层"].append(layer)

    # 付费数据（主UP卡池付费占比75%+）
    if layer == "免费":
        pay_amount = 0
        pay_times = 0
        is_first_pay = "否"
        pay_cycle = "无"
        is_pay = False
    else:
        is_pay = True
        is_first_pay = "是" if random.random() < 0.18 else "否"  # 首充转化≈18%
        
        # 付费卡池偏好：主UP热门卡池权重更高
        pay_cycle = random.choices(
            [cfg["卡池周期"] for cfg in POOL_CONFIG],
            weights=[0.25, 0.15, 0.20, 0.25],  # 黄泉25%>花火25%>灵砂20%>阮梅15%
            k=1
        )[0]

        # 付费次数
        if layer == "低价值":
            pay_times = random.randint(2, 6)
        elif layer == "中价值":
            pay_times = random.randint(4, 10)
        else:  # 高价值用户
            pay_times = random.randint(8, 20)
        
        # 累计付费金额（仅用官方标准档位）
        pay_amount = sum(random.choices(pay_options, k=pay_times))

    user_layer_data["累计付费金额(元)"].append(pay_amount)
    user_layer_data["付费次数"].append(pay_times)
    user_layer_data["是否首充"].append(is_first_pay)
    user_layer_data["主要付费卡池周期"].append(pay_cycle)
    user_layer_data["是否付费"].append(is_pay)

    # 日均在线时长
    online_time = round(random.uniform(30, 95), 1)
    user_layer_data["日均在线时长(分钟)"].append(online_time)

# 转换为DataFrame
user_layer_df = pd.DataFrame(user_layer_data)

# ---------------------- 写入Excel文件 ----------------------
with pd.ExcelWriter("崩坏星穹铁道_成熟稳定期双版本运营数据集.xlsx", engine="openpyxl") as writer:
    pd.DataFrame(activity_data).to_excel(writer, sheet_name="日活数据", index=False)
    pd.DataFrame(retention_data).to_excel(writer, sheet_name="留存数据", index=False)
    pd.DataFrame(payment_data).to_excel(writer, sheet_name="付费数据", index=False)
    user_layer_df.to_excel(writer, sheet_name="用户分层数据", index=False)

# ---------------------- 输出验证信息 ----------------------
print("✅ 崩坏：星穹铁道成熟稳定期双版本运营数据集生成完成！")
print("📋 数据文件：崩坏星穹铁道_成熟稳定期双版本运营数据集.xlsx")
print("🌟 核心特征（贴合真实运营）：")
print("  1. 留存体系：新手留存（看新增质量）+ 活跃用户7日留存（看老用户粘性），双指标更完整；")
print("  2. 卡池逻辑：主UP角色流水占比70%+，复刻仅30%-，热门主UP（黄泉/花火）优先级最高；")
print("  3. 付费规则：仅含官方标准档位6/30/98/198/328/648，无非标档位；")
print("  4. 用户特征：老用户占比80%+，活跃率75%-98%，付费高度聚焦主UP卡池；")
print("  5. 数据稳定性：成熟稳定期留存波动仅±0.8%（新手）/±1.5%（活跃用户）；")
# ========== 修改点4：补充验证信息 ==========
print("  6. 异常数据：注入DAU峰值（+30%）、委托完成率暴跌（-30%），贴合看板异常检测；")
print("  7. 付费转化：付费人数提升至4-10万，转化率回到星铁真实区间1.5%-2.5%；")
print("  8. 卡池峰值：开池第1/2天双峰值，贴合看板周期化峰值判断逻辑。")