# 🌍 Global Port Registry (GPR)

> **⚠️ 核心守则 (The Protocol)**
>
> 1.  **Sync First**: 开启新项目前必须先 `git pull`。
> 2.  **Check**: 寻找 `⚪️ Free` 状态的端口。
> 3.  **Lock**: 填入项目名，**立即 Push 到 GitHub**。
> 4.  **Code**: 只有在云端锁定成功后，才开始编写代码。

---

## 🎯 端口段规划 (Lucky High Port Zone)

| 端口范围 | 区域名称 | 适用项目 | 备注 |
|:---:|---|---|---|
| **50000-50009** | 🔴 Infrastructure Core | 网关, 核心后端 | 避开数字4区 |
| **50010-50099** | 🟢 Business Apps | 业务微服务 (爬虫, API 等) | 推荐使用 |
| **50100-50199** | 🟡 Middlewares | DB 面板, Redis 面板等 | - |
| **39000-39999** | 🔵 System Dashboards | 面板, 日志, 监控 | 基础设施区 |

---

## 📝 注册表 (Registry)

### 🔴 Core Zone (50000-50009)
| Port | Service ID | Project Path | Status |
|:---:|---|---|---|
| **50001** | demo-backend | `projects/Demo-Backend` | ✅ Active |
| **50002** | rss-backend | `projects/backend` | ✅ Active |
| **50003** | [VACANT] | - | ⚪️ Free |

### 🟢 Business Zone (50010-50099)
| Port | Service ID | Project Path | Status |
|:---:|---|---|---|
| **50010** | [VACANT] | - | ⚪️ Free |
| **50011** | [VACANT] | - | ⚪️ Free |

### 🔵 System Zone (39000-39999)
| Port | Service ID | Project Path | Status |
|:---:|---|---|---|
| **39999** | infra-dash | `server/infra-dash` | 🛡 SYSTEM |
| **39998** | dozzle | `server/` | 🛡 SYSTEM |
