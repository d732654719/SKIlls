---
name: write-help-doc
description: 项目使用说明书模板。当数据已收集完毕，需要按模板拼装说明书时使用此技能。定义了说明书各章节的数据来源映射关系。
---

# 项目使用说明书模板

此技能是一个说明书模板，定义说明书的结构以及每部分内容的数据来源。

Agent 在完成数据收集后，调用此 skill，传入已收集的数据，按模板拼装最终说明书。

## 数据来源一览
1.ZenTao 查询出的任务结果文中以zres指代
说明书内容由以下数据源填充(部分)：

| 数据项 | 来源 | 字段路径 |
|--------|------|----------|
| 项目名称 | zres | `zres.data.name` |
| 项目代码 | zres | `zres.data.code` |
| 项目描述 | zres | `zres.data.desc` |
| 需求标题 | zres | `zres.data.title` |
| 需求描述 | zres | `zres.data.spec` |
| 需求状态 | zres | `zres.data.status` |
| 说明书模板 | 帮助中心 MCP `loadDocTolls` 返回 | `data.data.md` |
| 模板文件名 | 帮助中心 MCP `loadDocTolls` 返回 | `data.data.text` |
| 操作场景 | case-to-spec skill 输出 | 场景 MD 文件内容 |
| 日志分析 | agent-browser + Chrome DevTools MCP（预留） | 日志分析结果 |
2.调用 case-to-spec skills 生成的内容以spec指代
## 说明书章节模板
文档名称:{data.name}FB{data.id}
---
文档内容:

# 版本说明

| 禅道需求编号 | 变更人 | 版本号 | 更新内容 | 更新时间 | 附件 |
|:----|:-------|:---|:---|:---|:---|
| FB{data.id} | 如果zres中有【测试】,代表有测试任务,则填非标测试,如果没有,则填非标开发 | 运维中心版本号{data.id}<br/>中台版本号{data.id} | 更新内容<br/>更新配置项 | 当天日期,格式:YYYY-MM-DD | 第三方文档 |

---

# 1. 项目基本信息

收费系统6.X

---

# 2. 项目需求描述

## 需求编号{data.id}

zres.data.desc中关于需求描述的内容,需要自行判断,因为不是所有

---

# 3. 升级说明

## 3.1 功能模块名称

### 3.1.1 数据库脚本插件（第一顺序升级）

**升级位置**：运维中心 → 车场列表 → 服务管理 → 新非标服务

| 属性 | 值 |
|:---|:---|
| 应用名称 | 【应用名称】 |
| 应用代码 | KT_SQL |
| 版本号 | 最新的上架版本即可 |
| tapd | 禅道需求编号 |

---

### 3.1.2 统一接口-车场授权

**APPID**：xxxxx

车场授权-扩展信息请填写以下内容：

<font color='red'>**注意：扩展信息请从下图中复制后进行修改，不可使用中文符号**</font>

```json
{
  "parkId": "592011653",
  "parkCode": "592011653",
  "accessID": "TONG7c7301ec32aa12ca",
  "groupcode": "12E11A1747758"
}
```

**字段说明**：

| 字段 | 说明 |
|:---|:---|
| `parkId` | 科拓车场ID |
| `parkCode` | 停车场编码，第三方定义并提供 |
| `accessID` | 第三方提供的固定值，**不需要修改** |
| `groupcode` | 单位注册时发送到指定邮箱的企业标识码，**不需要修改** |

---

### 3.1.3 计费非标插件

**升级位置**：运维中心 → 车场列表 → 服务管理 → 新非标服务

| 应用名称 | 应用代码 | 版本号 | tapd |
|:---|:---|:---|:---|
| 【应用名称】 | callfee | 最新的上架版本即可 | 禅道需求编号 |
| 【应用名称】 | carOut | 最新的上架版本即可 | 禅道需求编号 |

---

### 3.1.4 进出口非标插件

**升级位置**：运维中心 → 车场列表 → 应用管理 → 通道服务升级 → 运维客户端通道服务

**步骤一：安装 lua 依赖包**

| 属性 | 值 |
|:---|:---|
| 应用名称 | lua依赖包安装 |
| 应用代码 | channelservice |
| 版本号 | 1.1.4.2 |

![lua依赖包安装截图1](https://yunwei-file.keytop.cn/pushHelpCenterToOos/image/2023-07-14/1689303335667image.png?AWSAccessKeyId=VO7WZH15RG3REYGD5FW4&Expires=1781149287&Signature=Xafp18wCnv%2FbRhLg5evl%2BJnVlyc%3D)

![lua依赖包安装截图2](https://yunwei-file.keytop.cn/pushHelpCenterToOos/image/2023-07-14/1689303393512image.png?AWSAccessKeyId=VO7WZH15RG3REYGD5FW4&Expires=1781149287&Signature=onmitinoval6myOqZu2%2FmWw8iGY%3D)

**步骤二：安装 KT_Lua 插件**

| 属性 | 值 |
|:---|:---|
| 应用名称 | 【应用名称】 |
| 应用代码 | KT_Lua |
| 版本号 | 最新的上架版本即可 |
| tapd | 禅道需求编号 |

---

### 3.1.5 报表插件

| 属性 | 值 |
|:---|:---|
| 应用名称 | 【应用名称】 |
| 应用代码 | 【应用代码】 |
| 版本号 | 最新的上架版本即可 |
| tapd | 禅道需求编号 |

---

### 3.1.6 定制功能配置页

**升级位置**：运维中心 → 车场列表 → 服务管理 → 标准服务

![定制功能配置页截图](https://yunwei-file.keytop.cn/pushHelpCenterToOos/image/2021-01-20/60079cab04eb2.png?AWSAccessKeyId=VO7WZH15RG3REYGD5FW4&Expires=1781149287&Signature=Sd3BQOQQ0cE2joLAf6IAIrkXAmA%3D)

---

# 4. 配置说明

## 4.1 功能模块名称1

### 4.1.1 定制功能-定制功能配置页面

| 属性 | 说明 |
|:---|:---|
| **配置名称** | 【一天一次免费时间收费标准编号】 |
| **配置描述** | 标准所有标准适用填：`0`<br/>部分收费标准适用（用分隔符 `\|`）填：`1\|2\|3\|4` |
| **配置值** | 【按描述配置】 |

<font color="red">**注：配置名称是固定值，不可自定义**</font>

![配置页面截图](https://yunwei-file.keytop.cn/pushHelpCenterToOos/image/2021-03-23/6059ad4ef1980.png?AWSAccessKeyId=VO7WZH15RG3REYGD5FW4&Expires=1781149287&Signature=0gRIA%2BX3FwmcInOL9OfoOrON6xs%3D)

---

# 5. 使用场景展示

spec填入到这里,里面的标题不要,只复制内容

---

# 6. 验证步骤说明

（待补充）

---

# 7. 流程图

（待补充）

---

# 8. 日志解析

## 8.1 日志路径-中台日志

**访问路径**：运维中心 → 非标中心 → 非标中台应用 → 搜索项目的tapd或应用名称 → 更多操作 → 中台日志

**PID**：（待补充）

---

## 8.2 日志路径-云端车场服务

**访问路径**：运维中心 → 日志中心 → 日志中心 → 云端车场服务

![云端车场服务日志截图](https://yunwei-file.keytop.cn/pushHelpCenterToOos/image/2023-08-22/1692694712040image.png?AWSAccessKeyId=VO7WZH15RG3REYGD5FW4&Expires=1781149287&Signature=EAqD1llUgASfksjM5D86rEs9NPQ%3D)

---

## 8.3 日志路径-场端车场服务

**访问路径**：运维中心 → 日志中心 → 日志中心 → 场端车场服务

![场端车场服务日志截图](https://yunwei-file.keytop.cn/pushHelpCenterToOos/image/2023-08-29/1693301086137image.png?AWSAccessKeyId=VO7WZH15RG3REYGD5FW4&Expires=1781149287&Signature=gRgWPHpYhUXqUgOe2%2Bh%2BK2IXEjs%3D)

---

## 8.4 日志解析

按照业务流程，提供日志排查步骤、日志关键词。

（待补充）

---

# 9. 常见问题排查说明

1. **车场是否已授权**

2. **统一接口是否推送**

3. **查看流程图**：要明确各个服务之间的关系，上下游关系要明确

4. **HTTP 状态码排查指南**

| 状态码 | 含义 | 排查方向 |
|:---|:---|:---|
| `4xx` | 客户端错误 | 请求发起方问题，由我方解决 |
| `401` | 未授权 | 请求未携带有效的认证信息，一般为请求参数 token 问题 |
| `400` | 请求参数错误 | 检查请求参数是否正确，确保请求格式符合要求 |
| `404` | 资源不存在 | 检查 URL 是否正确（接收方确认），以及资源是否存在（接收方确认） |
| `5xx` | 服务器错误 | 接收方服务器问题，询问第三方解决 |
| `500` | 服务器内部错误 | 请求接收方查看服务器日志，找到具体错误信息并修复 |
| `503` | 服务不可用 | 服务器正在维护或过载，等待后重试或请求接收方故障排除 |
| `504` | 网关超时 | 代理服务器向上游发送请求未及时收到响应，由请求接收方检查网络连接并重试 |

5. **无感抵扣超时**：无感支付需要超时限制，超过时间未响应即视作支付失败。如有其他无感则走下一个无感。长时间等待对车主体验不佳。若超过规定时间，排查接口调用过程中耗时的部分，想办法缩短。

6. **请求第三方接口延迟**：若非标没有明显报错，排查非标请求日志为正常，第三方收到日志确实延迟收到，可排查是否非标中台资源不足导致请求延迟。

---

# 10. 测试用例

（待补充）
