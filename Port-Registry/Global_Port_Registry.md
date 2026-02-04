# 🌍 Global Port Registry (GPR)

> **⚠️ 核心守则 (The Protocol)**
>
> 1.  **Sync First**: 在开启任何新项目前，必须先 `git pull` 确保拥有最新版本。
> 2.  **Check**: 查阅下表，寻找一个标记为 `[VACANT]` 的空闲端口。
> 3.  **Lock**: 将你的项目名称填入表格，**立即提交并推送到 GitHub**。
> 4.  **Code**: 只有在 Push 成功后，才开始编写 docker-compose 代码。

---

## 🎯 端口段规划 (Zone Allocation)

| 端口范围 | 区域名称 | 适用项目 | 负责人 |
|:---:|---|---|---|
| **8000-8009** | 🔴 Infrastructure Core | 核心网关、总控后端 | @Admin |
| **8010-8049** | 🟢 Business Applications | 各类业务微服务 (爬虫, API等) | @Dev |
| **8050-8079** | 🟡 Middlewares | 数据库面板, Redis, MQ 面板 | @Dev |
| **8080-8099** | 🔵 System Dashboards | 监控面板, 日志中心 | @Admin |

---

## 📝 注册表 (Registry)

### 🔴 Core Zone (8000-8009)
| Port | Service ID | Project Path | Status |
|:---:|---|---|---|
| **8000** | (Reserved) | - | 🚫 Reserved |
| **8001** | demo-backend | `projects/Demo-Backend` | ✅ Active |
| **8002** | rss-backend | `projects/backend` | ✅ Active |
| **8003** | [VACANT] | - | ⚪️ Free |
| **8004** | [VACANT] | - | ⚪️ Free |

### 🟢 Business Zone (8010-8049)
| Port | Service ID | Project Path | Status |
|:---:|---|---|---|
| **8010** | [VACANT] | - | ⚪️ Free |
| **8011** | [VACANT] | - | ⚪️ Free |
| **8012** | [VACANT] | - | ⚪️ Free |
| ... | ... | ... | ... |

### 🔵 System Zone (39990-39999)
| Port | Service ID | Project Path | Status |
|:---:|---|---|---|
| **39999** | infra-dash | `server/infra-dash` | 🛡 SYSTEM |
| **39998** | dozzle | `server/` | 🛡 SYSTEM |
