# TrendRadar - 不可抗力事件监控系统

基于 [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) 定制的**全球重大不可抗力事件实时监控**系统。

## 功能概述

- **监控范围**: 全球重大/特大不可抗力事件
- **推送时间**: 08:00 - 21:00（夜间静默）
- **轮询间隔**: 10 分钟
- **推送方式**: ntfy (`http://www.chaofan.online:8081/global-alerts`)
- **运行模式**: 增量监控（有新增才推送）

## 监控事件类型

### 1. 自然灾害
- **地震**: 6级以上地震
- **气象**: 台风、暴雨、暴雪、寒潮、洪水、溃坝等
- **地质**: 山体滑坡、泥石流、海啸
- **火灾**: 重大森林/草原火灾

### 2. 重大事故
- **交通事故**: 坠机、列车脱轨、沉船等
- **矿难/建筑事故**: 坍塌、爆炸、被困
- **危化品事故**: 泄漏、爆炸、中毒
- **基础设施**: 大规模停供、桥梁/隧道垮塌

### 3. 公共卫生
- **疫情**: 全球大流行、传染病爆发
- **食品药品**: 重大安全事件

### 4. 社会安全
- **恐怖袭击**: 爆炸、枪击、砍人
- **群体性事件**: 骚乱、暴动、冲突

### 5. 地缘政治
- **战争冲突**: 宣战、空袭、导弹、边境冲突
- **政治动荡**: 政变、政权倒台、制裁、紧急状态

## 项目结构

```
TrendRadar/
├── config/
│   ├── config.yaml              # 主配置（ntfy 推送、调度系统）
│   ├── timeline.yaml            # 时间线配置（08:00-21:00 推送窗口）
│   ├── frequency_words.txt      # 不可抗力事件关键词（6大类）
│   ├── ai_analysis_prompt.txt   # AI 分析提示词
│   └── ai_translation_prompt.txt # AI 翻译提示词
├── trendradar/                   # 核心代码
├── output/                       # 输出目录
│   ├── html/                    # HTML 报告
│   ├── news/                    # 新闻数据库
│   └── rss/                     # RSS 数据库
├── run-monitor.ps1              # 监控脚本（带单例保护）
├── create-shortcut.bat          # 快捷方式生成器
└── .monitor.lock                # 运行锁文件
```

## 快速启动

### 方式 1：双击桌面快捷方式

桌面上的 `TrendRadar Monitor.lnk` - 双击即可启动

### 方式 2：命令行启动

```powershell
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\TrendRadar\run-monitor.ps1"
```

### 方式 3：重新生成快捷方式

```batch
cd TrendRadar
create-shortcut.bat
```

## 配置说明

### 推送时间窗口

| 时间段 | 行为 |
|--------|------|
| **08:00 - 21:00** | 采集 + 推送（有新增立即推送） |
| **21:00 - 08:00** | 仅采集（不推送） |

### 修改配置

**推送时间** → 编辑 `config/timeline.yaml`

**关键词配置** → 编辑 `config/frequency_words.txt`

**ntfy 服务器** → 编辑 `config/config.yaml`:
```yaml
notification:
  channels:
    ntfy:
      server_url: "http://your-server:port"
      topic: "your-topic"
```

## 运行状态检查

```powershell
# 检查锁文件（存在表示正在运行）
cat "C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\TrendRadar\.monitor.lock"

# 检查 Python 进程
tasklist | findstr python

# 查看最新报告
Get-ChildItem "C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\TrendRadar\output\html" -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

## 停止监控

```powershell
# 方式 1：通过锁文件中的 PID
$pid = Get-Content "C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\TrendRadar\.monitor.lock"
Stop-Process -Id $pid -Force

# 方式 2：直接停止所有 TrendRadar 相关 Python 进程
Get-Process python | Where-Object {$_.CommandLine -like '*trendradar*'} | Stop-Process -Force
```

## ntfy 订阅

### 手机端

1. 下载 ntfy App（iOS/Android）
2. 添加服务器：`http://www.chaofan.online:8081`
3. 订阅主题：`global-alerts`
4. 开启通知权限

### Web 浏览器

访问：`http://www.chaofan.online:8081/global-alerts`

## 依赖环境

- **Python**: >= 3.10
- **虚拟环境**: `C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\.venv`
- **依赖包**: 见 `requirements.txt`

## 注意事项

1. **单例保护**: 同一时间只能运行一个监控实例
2. **锁文件**: 运行时会创建 `.monitor.lock`，退出时自动删除
3. **自动清理**: 重启后旧锁文件会被自动检测并清理
4. **后台运行**: 默认隐藏窗口运行，不干扰正常使用

## 数据存储

- **本地存储**: SQLite 数据库（`output/news/`, `output/rss/`）
- **HTML 报告**: `output/html/latest/current.html`
- **保留策略**: 永久保留（可配置）

## 相关链接

- 原项目: [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)
- 数据源 API: [ourongxing/newsnow](https://github.com/ourongxing/newsnow)
- ntfy 官网: [ntfy.sh](https://ntfy.sh/)

---

**配置日期**: 2026-03-04
**版本**: 基于 TrendRadar v6.0.0 定制
