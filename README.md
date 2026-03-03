# TrendRadar - 不可抗力事件监控系统

基于 [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) 定制的**全球重大不可抗力事件实时监控**系统。

**支持平台**: Windows | Linux

## 功能概述

- **监控范围**: 全球重大/特大不可抗力事件
- **推送时间**: 08:00 - 21:00（夜间静默）
- **轮询间隔**: 10 分钟
- **推送方式**: ntfy (`http://www.chaofan.online:8081/global-alerts`)
- **运行模式**: 增量监控（有新增才推送）
- **单例保护**: 防止重复运行

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
│   └── frequency_words.txt      # 不可抗力事件关键词（6大类）
├── trendradar/                   # 核心代码
├── output/                       # 输出目录
│   ├── html/                    # HTML 报告
│   ├── news/                    # 新闻数据库
│   └── rss/                     # RSS 数据库
├── run-monitor.ps1              # Windows 监控脚本
├── run-monitor.sh               # Linux 监控脚本
├── install-linux.sh             # Linux 一键安装脚本
├── create-shortcut.bat          # Windows 快捷方式生成器
├── trendradar-monitor.service   # Linux systemd 服务模板
└── .monitor.lock                # 运行锁文件
```

---

## 快速启动

### Windows

#### 方式 1：双击桌面快捷方式

桌面上的 `TrendRadar Monitor.lnk` - 双击即可启动

#### 方式 2：PowerShell 命令行

```powershell
powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\path\to\TrendRadar\run-monitor.ps1"
```

#### 方式 3：重新生成快捷方式

```batch
cd TrendRadar
create-shortcut.bat
```

### Linux

#### 首次安装

```bash
cd TrendRadar
chmod +x install-linux.sh
./install-linux.sh
```

安装脚本会自动：
1. 检查 Python 版本
2. 创建虚拟环境（如不存在）
3. 安装依赖包
4. 设置脚本执行权限

#### 方式 1：直接运行（前台）

```bash
cd TrendRadar
chmod +x run-monitor.sh
./run-monitor.sh
```

#### 方式 2：后台运行

```bash
cd TrendRadar
nohup ./run-monitor.sh > monitor.log 2>&1 &
```

#### 方式 3：systemd 服务（开机自启）

```bash
# 1. 修改服务文件中的路径
sed -i 's|/path/to/TrendRadar|/your/actual/path|g' trendradar-monitor.service

# 2. 安装服务
sudo cp trendradar-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload

# 3. 启用并启动服务
sudo systemctl enable trendradar-monitor
sudo systemctl start trendradar-monitor

# 4. 查看状态
sudo systemctl status trendradar-monitor
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

**虚拟环境路径**（如需修改）:
- **Windows**: 编辑 `run-monitor.ps1` 中的 `$VenvPython`
- **Linux**: 编辑 `run-monitor.sh` 中的 `VENV_PYTHON`

## 运行状态检查

### Windows

```powershell
# 检查锁文件（存在表示正在运行）
cat "C:\path\to\TrendRadar\.monitor.lock"

# 检查 Python 进程
tasklist | findstr python

# 查看最新报告
Get-ChildItem "C:\path\to\TrendRadar\output\html" -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

### Linux

```bash
# 检查锁文件（存在表示正在运行）
cat /path/to/TrendRadar/.monitor.lock

# 检查进程
ps aux | grep trendradar

# 查看 systemd 服务状态
sudo systemctl status trendradar-monitor

# 查看日志
tail -f monitor.log          # 后台运行模式
sudo journalctl -u trendradar-monitor -f  # systemd 服务模式

# 查看最新报告
ls -lt /path/to/TrendRadar/output/html/ | head -10
```

## 停止监控

### Windows

```powershell
# 方式 1：通过锁文件中的 PID
$pid = Get-Content "C:\path\to\TrendRadar\.monitor.lock"
Stop-Process -Id $pid -Force

# 方式 2：直接停止所有 TrendRadar 相关 Python 进程
Get-Process python | Where-Object {$_.CommandLine -like '*trendradar*'} | Stop-Process -Force
```

### Linux

```bash
# 方式 1：通过锁文件中的 PID
pid=$(cat /path/to/TrendRadar/.monitor.lock)
kill $pid

# 方式 2：停止 systemd 服务
sudo systemctl stop trendradar-monitor

# 方式 3：查找并停止进程
pkill -f trendradar

# 禁用开机自启（systemd）
sudo systemctl disable trendradar-monitor
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

### 通用

- **Python**: >= 3.10
- **依赖包**: 见 `requirements.txt`

### Windows

- **虚拟环境**: `C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\.venv`
- **PowerShell**: 默认已安装

### Linux

```bash
# 安装 Python 虚拟环境
sudo apt install python3-venv  # Debian/Ubuntu
sudo yum install python3-venv  # CentOS/RHEL

# 创建虚拟环境（如果还没有）
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 注意事项

1. **单例保护**: 同一时间只能运行一个监控实例
2. **锁文件**: 运行时会创建 `.monitor.lock`，退出时自动删除
3. **自动清理**: 重启后旧锁文件会被自动检测并清理
4. **后台运行**:
   - **Windows**: 默认隐藏窗口运行（`-WindowStyle Hidden`）
   - **Linux**: 使用 `nohup` 或 `systemd` 实现后台运行
5. **日志文件**:
   - **Linux 后台模式**: 日志输出到 `monitor.log`
   - **Linux systemd**: 日志通过 `journalctl -u trendradar-monitor` 查看

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
