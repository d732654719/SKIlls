---
name: case-to-script
description: |
  将测试用例转换为可执行的Python测试脚本。适用于已有测试用例，需要生成自动化测试脚本的场景。
  常用触发词：转脚本 / md转脚本 / 生成脚本 / 用例转脚本 / md生成脚本 / python脚本
  工作流程：读取用例 → 理解接口文档(如果有) → 分析框架代码 → 生成测试脚本
---

## 适用场景

- 用户提供测试用例文件
- 用户需要生成可运行的Python测试脚本


## 工作流程

### 第一步：找到测试用例文件

1. **确认测试用例路径**
   - 如果用户没提供完整路径，在目录`E:\项目`搜索,如果没有这个目录,再询问用户提供路径

2. **读取用例**


### 第二步：找到并阅读接口文档（PDF）

1. **查找同目录下的PDF文件**
   - 如果有的话,在同目录下找PDF文件
   ```python
   import os
   folder = os.path.dirname(excel_path)
   pdf_file = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')][0]
   ```

2. **读取PDF内容**
   ```python
   from pypdf import PdfReader
   reader = PdfReader(os.path.join(folder, pdf_file))
   for page in reader.pages:
       print(page.extract_text())
   ```
   - 记录接口地址
   - 记录请求参数字段
   - 记录返回参数格式

### 第三步：分析测试框架代码

####参照学习已有的测试框架
框架路径即**当前工作目录**（项目根目录），分析并准备生成项目脚本
比如以下一些内容,不代表全部你要参照的
1. dsp服务初始化,使用Interface/dsp_interface.py中的dsp_add_ip_list_init
2. **进出场模拟函数**
   - 查找 `dsp_interface.py` 中的 `dspip_car_pass()` 函数
   - 了解参数：`dsp_ip`, `car_no`, `car_style`, `pass_time`
3. **车牌生成**：使用框架已有的 `getdif_carno()` 函数
4. **查费缴费**
 - 使用Interface\testfee_interface.py中的getorder查询车辆费用,使用Interface\platform_interface.py中的pay_fee_force缴费
 - 在出场前,要调用查费与缴费,要不然调出场的时候如果有待缴的费用,车子就不能出场
5. **工具函数**
   - 查找 `Utils/commonUtils.py` 中的 `getdif_carno()` 等函数
6. **配置文件**
   - 读取 `settings.py` 了解接口地址、场站配置等
7. **模拟进出场程序DspServer**
   -  所有进出场的调用,都需要先打开DspServer,程序位置:{项目根目录}/DspServer/DspServer.exe 脚本最前面实现如果检测到该程序没打开,则打开它
8. **创建内部车接口**
   - 接口位置:Interface/web_interface.py中的`add_valid_lotcar_info`函数
9. **创建预约车**
   - 接口位置:Interface/ReserveSpace_unit_api.py
   - 添加时间不能请晚于离场时间,否则认为离场后添加的预约车,不生效,添加时间不能改变,所以离场时间要注意控制
10. **使用抵扣券**
   - 接口位置:Interface/platform_interface.py中的`ticket`函数
11 .**修改定制功能配置**
   - Interface\dingzhigongneng.py
####业务的大致流程
确保dspserver打开并初始化->进场->查费->缴费->出场,总之出场前要缴费,因为出场时间是模拟的时间可能不是现在,可能是以前可能是以后, 如果在出口后才去缴费,可能会失败
### 第四步：生成测试脚本

1.脚本路径规则,文件命名规则:
在项目根目录的testCases目录下创建文件夹,文件名是:"test_"+测试用例文件的名字FB后面,-前面的那串数字,比如用例叫比亚迪集团-充电优惠减免对接FB95446-用例(常规模板),则文件名是:test_95446

2.代码风格:
 - 所有函数调用，必须使用关键字传参，禁止仅使用位置传参
 - 保存日志：需要有日志的存储,每次执行不覆盖旧日志，使用 `"a"` 模式
 - 时间格式：`YYYY-MM-DD HH:MM:SS`
 - 等待生效：进场后等待1-2秒再调用接口
 - 注意解决命令行中文乱码问题,通常要添加UTF-8 编码设置
 - 代码结构要利于单独注释不想执行的用例
#### 脚本结构参考

```python
# -*- coding: utf-8 -*-
"""
萧山区原朝晖初中停车场-免费时间非标-历史BI优化 FB96815 测试用例
测试接口: DSP模拟进出场 + testfee查费接口

流程: 先进场(dspip_car_pass) -> 等待 -> 出场(dspip_car_pass) -> 查费(getorder) -> 断言

依赖:
- Interface.dsp_interface: dspip_car_pass (模拟车辆进出场)
- Interface.testfee_interface: getorder (查询停车费用)
- Interface.dsp_interface: dsp_add_ip_list_init (DSP初始化)
- settings.ktdn: 场站配置信息

测试用例: E:\项目\萧山区原朝晖初中停车场-免费时间非标-历史BI优化FB96815\萧山区原朝晖初中停车场-免费时间非标-历史BI优化FB96815-用例(常规模板)

计费规则:
- 计费单位: 10分钟
- 收费标准: 1元/10分钟，不足10分钟向上取整
- 免费时间: ≤60分钟 -> 30分钟免费; >60分钟 -> 15分钟免费
"""

import sys
import os
import time
import json
import io
import datetime

# 自动推导项目根目录（脚本在 testCases/test_xxx/ 下，往上两级即项目根）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
sys.path.insert(0, PROJECT_ROOT)

# 解决 Windows 命令行中文乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

from Interface.dsp_interface import dspip_car_pass, dsp_add_ip_list_init
from Interface.testfee_interface import getorder
from Interface.platform_interface import pay_fee_force
from settings import ktdn
from Utils.commonUtils import getdif_carno

# ==================== 配置 ====================
DSP_SERVER_EXE = os.path.join(PROJECT_ROOT, 'DspServer', 'DspServer.exe')

def check_and_start_dsp_server():
    """检测DspServer.exe是否在运行，若未运行则启动它"""
    import subprocess
    proc_name = "DspServer"
    # 检测进程是否在运行
    try:
        result = subprocess.run(
            ['tasklist'], capture_output=True, text=True, encoding='utf-8', errors='ignore'
        )
        if proc_name in result.stdout:
            print("[DspServer] 检测到进程已运行")
            return True
    except Exception as e:
        print("[DspServer] 检测进程失败: {}".format(e))

    # 未运行则启动
    print("[DspServer] 未检测到进程，准备启动...")
    try:
        subprocess.Popen(
            ['start', 'cmd', '/c', DSP_SERVER_EXE],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("[DspServer] 已启动，请等待3秒...")
        time.sleep(3)
        return True
    except Exception as e:
        print("[DspServer] 启动失败: {}".format(e))
        return False

# 测试车场
PARK_ID = "280025530"

# 计费规则: 1元/10分钟
CHARGE_UNIT_MINUTES = 10      # 计费单位（分钟）
CHARGE_PER_UNIT = 100         # 每单位金额（分）= 1元

# 免费时间配置
FREE_THRESHOLD_MINUTES = 60   # 免费时间分档阈值（分钟）
FREE_TIME_SHORT = 30 * 60      # ≤60分钟，免费30分钟（秒）
FREE_TIME_LONG  = 15 * 60     # >60分钟，免费15分钟（秒）

# 日志文件（放在脚本同目录）
LOG_DIR = SCRIPT_DIR
LOG_FILE = os.path.join(LOG_DIR, 'test_96815.log')

os.makedirs(LOG_DIR, exist_ok=True)

# ==================== 日志函数 ====================
def log(msg: str):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    line = "[{}] {}".format(timestamp, msg)
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def log_section(title: str):
    log("")
    log("=" * 60)
    log(title)
    log("=" * 60)

# ==================== 辅助函数 ====================
def calc_parking_duration(entry_time_str: str, exit_time_str: str) -> int:
    """计算停车时长（秒）"""
    fmt = '%Y-%m-%d %H:%M:%S'
    s = datetime.datetime.strptime(entry_time_str, fmt)
    e = datetime.datetime.strptime(exit_time_str, fmt)
    return int((e - s).total_seconds())

def calc_expected_fee(parking_seconds: int) -> dict:
    """
    根据停车时长计算预期费用
    规则:
    - ≤60分钟: 固定减免30分钟
    - >60分钟: 固定减免15分钟
    计费单位: 10分钟, 不足10分钟向上取整
    """
    if parking_seconds <= FREE_THRESHOLD_MINUTES * 60:
        free_seconds = FREE_TIME_SHORT
        tier = "≤60分钟"
    else:
        free_seconds = FREE_TIME_LONG
        tier = ">60分钟"

    billable_seconds = max(0, parking_seconds - free_seconds)
    # 不足10分钟向上取整
    units = -(-billable_seconds // (CHARGE_UNIT_MINUTES * 60))
    fee_cents = units * CHARGE_PER_UNIT
    fee_yuan = fee_cents / 100.0

    return {
        "parking_seconds": parking_seconds,
        "free_seconds": free_seconds,
        "billable_seconds": billable_seconds,
        "billable_units": units,
        "fee_cents": fee_cents,
        "fee_yuan": fee_yuan,
        "tier": tier
    }

def car_entry(car_no: str, pass_time: str = None):
    """车辆进场"""
    if pass_time is None:
        pass_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log("【进场】车牌: {}, 时间: {}".format(car_no, pass_time))
    result = dspip_car_pass(dsp_ip=ktdn.in_dsp, car_no=car_no, car_style=0, pass_time=pass_time)
    log("【进场结果】: {}".format(result))
    return pass_time

def car_exit(car_no: str, pass_time: str = None):
    """车辆出场"""
    if pass_time is None:
        pass_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log("【出场】车牌: {}, 时间: {}".format(car_no, pass_time))
    result = dspip_car_pass(dsp_ip=ktdn.out_dsp, car_no=car_no, car_style=0, pass_time=pass_time)
    log("【出场结果】: {}".format(result))
    return pass_time

def query_fee(car_no: str, exit_time: str) -> dict:
    """查询停车费用"""
    log("【查费】车牌: {}, 出场时间: {}".format(car_no, exit_time))
    try:
        result = getorder(car_no, exit_time, mode="test")
        pay_money = result.get("payMoney", 0)
        order_no = result.get("orderNo", "")
        log("【查费结果】订单号: {}, 应付金额: {}分({:.2f}元)".format(
            order_no, pay_money, int(pay_money) / 100.0))
        return {"payMoney": pay_money, "orderNo": order_no}
    except Exception as e:
        log("【查费异常】: {}".format(str(e)))
        return {"payMoney": -1, "orderNo": ""}

def pay_parking_fee(car_no: str, exit_time: str, order_info: dict):
    """缴纳停车费"""
    pay_money = order_info.get("payMoney", 0)
    order_no = order_info.get("orderNo", "")
    actual_fee_yuan = float(pay_money) / 100
    
    log("【缴费】车牌: {}, 订单号: {}, 金额: {} 元 ({} 分)".format(
        car_no, order_no, actual_fee_yuan, pay_money))
    
    if float(pay_money) != 0:
        pay_result = pay_fee_force(
            car_no=car_no,
            etc_no='',
            order_no=order_no,
            pay_source=4000,
            pay_channel=1002,
            pay_method=1001,
            total_money=pay_money,
            paid_money=pay_money,
            free_money=0,
            free_time=0,
            free_details=[],
            payment_ext={},
            pay_time=exit_time
        )
        log("【缴费结果】: {}".format(pay_result))
        return pay_result
    else:
        log("【缴费】金额为0，跳过缴费")
        return None

# ==================== 测试用例 ====================
def run_case(no: int, parking_minutes: int, expected_fee_cents: int, expected_tier: str, description: str):
    """执行单个测试用例"""
    log_section("用例{} - {}".format(no, description))

    # 生成车牌
    car_no = getdif_carno()
    log("测试车牌: {}".format(car_no))

    # 计算进出时间（基准时间: 今天 12:00:00）
    base = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    entry_time = base.strftime('%Y-%m-%d %H:%M:%S')
    exit_seconds = parking_minutes * 60
    exit_time = (base + datetime.timedelta(seconds=exit_seconds)).strftime('%Y-%m-%d %H:%M:%S')

    # 1. 进场
    entry_result = car_entry(car_no, entry_time)
    time.sleep(1)

    # 2. 查费
    fee_result = query_fee(car_no, exit_time)
    actual_fee = int(fee_result["payMoney"])

    # 3. 缴费
    pay_parking_fee(car_no, exit_time, fee_result)

    # 4. 出场
    exit_result = car_exit(car_no, exit_time)
    time.sleep(2)

    # 5. 计算预期
    parking_seconds = parking_minutes * 60
    expected = calc_expected_fee(parking_seconds)

    log("【预期结果】档位: {}, 停车{}分钟, 免费{}秒, 计费{}秒, {}单位, {}分({:.2f}元)".format(
        expected_tier,
        parking_minutes,
        expected["free_seconds"],
        expected["billable_seconds"],
        expected["billable_units"],
        expected_fee_cents,
        expected_fee_cents / 100.0
    ))
    log("【实际结果】应付金额: {}分({:.2f}元)".format(actual_fee, actual_fee / 100.0))

    # 5. 断言
    passed = (actual_fee == expected_fee_cents)
    if passed:
        log("【断言结果】✅ PASS - 实际={}分, 预期={}分".format(actual_fee, expected_fee_cents))
    else:
        diff = actual_fee - expected_fee_cents
        log("【断言结果】❌ FAIL - 实际={}分, 预期={}分, 差异={}分({:.2f}元)".format(
            actual_fee, expected_fee_cents, diff, diff / 100.0))
    return {
        "testNo": no,
        "description": description,
        "car_no": car_no,
        "entry_time": entry_time,
        "exit_time": exit_time,
        "expected_fee": str(expected_fee_cents),
        "actual_fee": str(actual_fee),
        "passed": passed,
        "error": ""
    }



### Excel结果写回

每个生成的脚本需内置Excel结果写回能力。

**新增导入**（追加到现有import末尾）：
```python
try:
    import openpyxl
    from openpyxl.styles import Alignment, Font
    _HAS_OPENPYXL = True
except ImportError:
    _HAS_OPENPYXL = False
```

**FB号提取**（紧跟SCRIPT_DIR之后）：
```python
FB_NUMBER = os.path.basename(SCRIPT_DIR).replace('test_', '')
```

**执行开始/结束标记**（`if __name__`块的首尾）：
```python
log("╔══════════════════════════════════════════════╗")
log("║          测 试 开 始 执 行                   ║")
log("╚══════════════════════════════════════════════╝")
# ... 所有用例执行 ...
log("╔══════════════════════════════════════════════╗")
log("║          测 试 执 行 结 束                   ║")
log("╚══════════════════════════════════════════════╝")
```

**主执行块**收集dict结果并调用Excel写回：
```python
case_results = []

for each case:
    result = run_case(case_no=..., ...)
    case_results.append(result)

# 汇总
pass_count = sum(1 for r in case_results if r["passed"])
fail_count = len(case_results) - pass_count
log("总用例数: {}".format(len(case_results)))
log("通过: {}".format(pass_count))
log("失败: {}".format(fail_count))

# === Excel结果写回 ===
xlsx_path = find_excel_file(FB_NUMBER, r"E:\项目")
if xlsx_path:
    write_results_to_excel(xlsx_path, case_results, LOG_FILE, FB_NUMBER)
else:
    log("【Excel写回】未找到Excel用例文件，请先用 testcase-md-to-excel 技能生成Excel后再运行脚本")
```

**新增函数**（插入在`if __name__`之前）：

`find_excel_file(fb_number, search_root)` — 在search_root下遍历子目录，找包含fb_number的目录及其内xlsx文件，返回路径或None。

`write_results_to_excel(xlsx_path, case_results, log_file_path, fb_number)` — 先检测`~$`锁文件判断Excel是否被打开，若被占用则log提示"请关闭WPS/Excel后重试"。打开Excel后调`_write_to_testcase_sheet`覆盖`测试结果`列，调`_write_to_caseresult_sheet`追加执行报告。保存时单独catch PermissionError，提示用户关闭文件后重新运行脚本。

`_write_to_testcase_sheet(ws, case_results)` — 在第1行找"测试结果"列头确定列号，通过第1列testNo匹配行号，写入"通过"或"失败"。

`_write_to_caseresult_sheet(wb, case_results, log_file_path, fb_number)` — 找到caseResult sheet（没有则创建），找到最后有内容行，向下空4行后写入：执行时间、汇总（总数/通过/失败/通过率）、明细表头+每行数据、完整日志内容。






