# coding=utf-8
"""
HTML 报告渲染模块 - Force Majeure Monitor 定制版

监控指挥中心风格的不可抗力事件报告
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Callable

from trendradar.report.helpers import html_escape
from trendradar.utils.time import convert_time_for_display
from trendradar.ai.formatter import render_ai_analysis_html_rich


def render_html_content(
    report_data: Dict,
    total_titles: int,
    mode: str = "daily",
    update_info: Optional[Dict] = None,
    *,
    region_order: Optional[List[str]] = None,
    get_time_func: Optional[Callable[[], datetime]] = None,
    rss_items: Optional[List[Dict]] = None,
    rss_new_items: Optional[List[Dict]] = None,
    display_mode: str = "keyword",
    standalone_data: Optional[Dict] = None,
    ai_analysis: Optional[Any] = None,
    show_new_section: bool = True,
) -> str:
    """渲染HTML内容 - Force Majeure Monitor 定制版

    Args:
        report_data: 报告数据字典
        total_titles: 新闻总数
        mode: 报告模式
        update_info: 更新信息
        region_order: 区域显示顺序
        get_time_func: 获取当前时间的函数
        rss_items: RSS 统计条目
        rss_new_items: RSS 新增条目
        display_mode: 显示模式
        standalone_data: 独立展示区数据
        ai_analysis: AI 分析结果
        show_new_section: 是否显示新增热点区域

    Returns:
        渲染后的 HTML 字符串
    """
    # 默认区域顺序
    default_region_order = ["hotlist", "rss", "new_items", "standalone", "ai_analysis"]
    if region_order is None:
        region_order = default_region_order

    # 获取当前时间
    if get_time_func is None:
        get_time_func = datetime.now
    current_time = get_time_func()

    # 统计数据
    stats = report_data.get("stats", {})
    new_titles = report_data.get("new_titles", set())
    failed_ids = report_data.get("failed_ids", [])
    total_new_count = report_data.get("total_new_count", 0)

    # 模式名称映射
    mode_names = {
        "daily": "当日汇总",
        "current": "当前榜单",
        "incremental": "增量分析"
    }

    # 生成关键词分组 HTML
    keyword_sections = []
    for keyword, data in stats.items():
        news_list = data.get("news", [])
        count = len(news_list)

        # 根据事件类型设置警告级别颜色
        keyword_lower = keyword.lower()
        if any(x in keyword_lower for x in ["地震", "海啸", "洪水", "台风", "火灾", "爆炸", "袭击", "战争", "死亡"]):
            severity = "critical"
            color = "#ff3333"
            glow = "rgba(255, 51, 51, 0.3)"
        elif any(x in keyword_lower for x in ["暴雨", "高温", "预警", "事故", "冲突"]):
            severity = "warning"
            color = "#ff9933"
            glow = "rgba(255, 153, 51, 0.3)"
        else:
            severity = "info"
            color = "#00ff99"
            glow = "rgba(0, 255, 153, 0.2)"

        news_items_html = ""
        for idx, news in enumerate(news_list[:20]):  # 限制显示数量
            title = html_escape(news.get("title", ""))
            source = html_escape(news.get("source", ""))
            url = news.get("url", "")
            rank = news.get("rank", 0)
            is_new = news.get("is_new", False)

            new_badge = '<span class="new-badge">NEW</span>' if is_new else ''

            news_items_html += f'''
                <div class="news-item" data-severity="{severity}">
                    <span class="news-rank">{rank}</span>
                    <div class="news-content">
                        <a href="{url}" target="_blank" class="news-title">{title}</a>
                        <span class="news-meta">{source}{new_badge}</span>
                    </div>
                </div>
            '''

        keyword_sections.append(f'''
            <div class="section category-{severity}" style="--severity-color: {color}; --severity-glow: {glow};">
                <div class="section-header">
                    <div class="section-icon"></div>
                    <h2 class="section-title">{html_escape(keyword)}</h2>
                    <span class="section-count">{count}条</span>
                </div>
                <div class="section-content">
                    {news_items_html if news_items_html else '<div class="no-data">暂无数据</div>'}
                </div>
            </div>
        ''')

    # 头部信息
    header_info_html = f'''
        <div class="info-grid">
            <div class="info-item">
                <span class="info-label">报告类型</span>
                <span class="info-value">{mode_names.get(mode, mode)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">监控事件</span>
                <span class="info-value">{sum(len(d.get("news", [])) for d in stats.values())}条</span>
            </div>
            <div class="info-item">
                <span class="info-label">新增事件</span>
                <span class="info-value">{total_new_count}条</span>
            </div>
            <div class="info-item">
                <span class="info-label">生成时间</span>
                <span class="info-value">{current_time.strftime("%m-%d %H:%M")}</span>
            </div>
        </div>
    '''

    # 状态指示器
    status_indicators = f'''
        <div class="status-bar">
            <div class="status-item active">
                <span class="status-dot"></span>
                <span>监控系统</span>
            </div>
            <div class="status-item active">
                <span class="status-dot"></span>
                <span>数据采集</span>
            </div>
            <div class="status-item">
                <span class="status-dot"></span>
                <span>全球覆盖</span>
            </div>
        </div>
    '''

    html = f'''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TRENDRADAR // Force Majeure Monitor</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js" integrity="sha512-BNaRQnYJYiPSqHHDb58B0yaPfCu+Wgds8Gp/gU33kqBtgNS4tSPHuGibyoeqMV/TJlSKda6FXzoEyYGjTe+vXA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        <style>
            /* CSS 变量 - 深色监控主题 */
            :root {{
                --bg-primary: #0a0a0a;
                --bg-secondary: #111111;
                --bg-tertiary: #1a1a1a;
                --text-primary: #e0e0e0;
                --text-secondary: #888888;
                --text-muted: #444444;

                --color-critical: #ff3333;
                --color-warning: #ff9933;
                --color-info: #00ff99;
                --color-muted: #333333;

                --border-color: #222222;
                --border-glow: rgba(0, 255, 153, 0.1);

                --font-mono: 'JetBrains Mono', monospace;
                --font-display: 'Space Grotesk', sans-serif;

                --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }}

            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                font-family: var(--font-display);
                background: var(--bg-primary);
                color: var(--text-primary);
                line-height: 1.6;
                min-height: 100vh;
                position: relative;
                overflow-x: hidden;
            }}

            /* 背景网格效果 */
            body::before {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image:
                    linear-gradient(rgba(0, 255, 153, 0.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0, 255, 153, 0.03) 1px, transparent 1px);
                background-size: 50px 50px;
                pointer-events: none;
                z-index: 1;
            }}

            /* 扫描线动画 */
            body::after {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, transparent, var(--color-info), transparent);
                opacity: 0.5;
                animation: scan 4s linear infinite;
                pointer-events: none;
                z-index: 2;
            }}

            @keyframes scan {{
                0% {{ top: 0; }}
                100% {{ top: 100%; }}
            }}

            .container {{
                max-width: 900px;
                margin: 0 auto;
                padding: 40px 20px;
                position: relative;
                z-index: 10;
            }}

            /* 头部 */
            .header {{
                border: 1px solid var(--border-color);
                background: var(--bg-secondary);
                padding: 40px;
                margin-bottom: 30px;
                position: relative;
                overflow: hidden;
            }}

            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--color-critical), var(--color-warning), var(--color-info));
            }}

            .header-brand {{
                font-family: var(--font-mono);
                font-size: 11px;
                letter-spacing: 4px;
                color: var(--color-info);
                margin-bottom: 20px;
                text-transform: uppercase;
            }}

            .header-title {{
                font-family: var(--font-display);
                font-size: clamp(24px, 5vw, 36px);
                font-weight: 700;
                letter-spacing: -1px;
                margin-bottom: 10px;
                background: linear-gradient(135deg, #fff 0%, var(--text-secondary) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}

            .header-subtitle {{
                font-family: var(--font-mono);
                font-size: 12px;
                color: var(--text-secondary);
                letter-spacing: 2px;
            }}

            .save-buttons {{
                position: absolute;
                top: 20px;
                right: 20px;
                display: flex;
                gap: 10px;
            }}

            .save-btn {{
                font-family: var(--font-mono);
                font-size: 11px;
                padding: 8px 16px;
                background: transparent;
                border: 1px solid var(--color-info);
                color: var(--color-info);
                cursor: pointer;
                transition: var(--transition);
                letter-spacing: 1px;
            }}

            .save-btn:hover {{
                background: var(--color-info);
                color: var(--bg-primary);
                box-shadow: 0 0 20px var(--color-info);
            }}

            /* 信息网格 */
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 1px;
                background: var(--border-color);
                border: 1px solid var(--border-color);
                margin-bottom: 30px;
            }}

            .info-item {{
                background: var(--bg-secondary);
                padding: 20px;
                text-align: center;
            }}

            .info-label {{
                font-family: var(--font-mono);
                font-size: 10px;
                letter-spacing: 2px;
                color: var(--text-secondary);
                text-transform: uppercase;
                margin-bottom: 8px;
            }}

            .info-value {{
                font-family: var(--font-display);
                font-size: 20px;
                font-weight: 600;
                color: var(--text-primary);
            }}

            /* 状态栏 */
            .status-bar {{
                display: flex;
                gap: 30px;
                padding: 15px 0;
                margin-bottom: 30px;
                border-bottom: 1px solid var(--border-color);
            }}

            .status-item {{
                display: flex;
                align-items: center;
                gap: 8px;
                font-family: var(--font-mono);
                font-size: 11px;
                letter-spacing: 1px;
                color: var(--text-secondary);
            }}

            .status-dot {{
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--text-muted);
            }}

            .status-item.active .status-dot {{
                background: var(--color-info);
                box-shadow: 0 0 10px var(--color-info);
                animation: pulse 2s infinite;
            }}

            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}

            /* 内容区块 */
            .section {{
                border: 1px solid var(--border-color);
                background: var(--bg-secondary);
                margin-bottom: 20px;
                position: relative;
                transition: var(--transition);
            }}

            .section:hover {{
                border-color: var(--severity-color);
                box-shadow: 0 0 30px var(--severity-glow);
            }}

            .section-header {{
                display: flex;
                align-items: center;
                gap: 15px;
                padding: 20px 25px;
                border-bottom: 1px solid var(--border-color);
                background: var(--bg-tertiary);
            }}

            .section-icon {{
                width: 24px;
                height: 24px;
                position: relative;
            }}

            .section-icon::before {{
                content: '';
                position: absolute;
                width: 100%;
                height: 100%;
                border: 2px solid var(--severity-color);
                border-radius: 50%;
                animation: icon-pulse 2s infinite;
            }}

            .section-icon::after {{
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 8px;
                height: 8px;
                background: var(--severity-color);
                border-radius: 50%;
            }}

            @keyframes icon-pulse {{
                0%, 100% {{
                    transform: scale(1);
                    opacity: 1;
                }}
                50% {{
                    transform: scale(1.5);
                    opacity: 0.5;
                }}
            }}

            .section-title {{
                font-family: var(--font-display);
                font-size: 18px;
                font-weight: 600;
                color: var(--text-primary);
                flex: 1;
            }}

            .section-count {{
                font-family: var(--font-mono);
                font-size: 14px;
                color: var(--severity-color);
                padding: 5px 12px;
                border: 1px solid var(--severity-color);
            }}

            .section-content {{
                padding: 0;
            }}

            /* 新闻条目 */
            .news-item {{
                display: flex;
                align-items: flex-start;
                gap: 15px;
                padding: 18px 25px;
                border-bottom: 1px solid var(--border-color);
                transition: var(--transition);
            }}

            .news-item:hover {{
                background: var(--bg-tertiary);
            }}

            .news-item:last-child {{
                border-bottom: none;
            }}

            .news-rank {{
                font-family: var(--font-mono);
                font-size: 12px;
                color: var(--text-muted);
                min-width: 30px;
                padding-top: 2px;
            }}

            .news-content {{
                flex: 1;
                min-width: 0;
            }}

            .news-title {{
                font-family: var(--font-display);
                font-size: 15px;
                font-weight: 500;
                color: var(--text-primary);
                text-decoration: none;
                display: block;
                margin-bottom: 6px;
                line-height: 1.4;
                transition: var(--transition);
            }}

            .news-title:hover {{
                color: var(--severity-color);
            }}

            .news-meta {{
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--text-secondary);
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .new-badge {{
                font-size: 9px;
                padding: 2px 6px;
                background: var(--color-info);
                color: var(--bg-primary);
                letter-spacing: 1px;
            }}

            .no-data {{
                padding: 40px;
                text-align: center;
                font-family: var(--font-mono);
                font-size: 12px;
                color: var(--text-muted);
                letter-spacing: 2px;
            }}

            /* 页脚 */
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid var(--border-color);
                text-align: center;
                font-family: var(--font-mono);
                font-size: 11px;
                color: var(--text-muted);
                letter-spacing: 1px;
            }}

            /* 响应式 */
            @media (max-width: 640px) {{
                .container {{
                    padding: 20px 15px;
                }}

                .header {{
                    padding: 25px;
                }}

                .save-buttons {{
                    position: static;
                    margin-bottom: 20px;
                    justify-content: flex-end;
                }}

                .info-grid {{
                    grid-template-columns: 1fr 1fr;
                }}

                .section-header {{
                    padding: 15px 20px;
                }}

                .news-item {{
                    padding: 15px 20px;
                }}
            }}

            /* 关键词分组显示 - critical 级别特殊样式 */
            .category-critical {{
                --severity-color: #ff3333;
                --severity-glow: rgba(255, 51, 51, 0.2);
            }}

            .category-critical .section-icon::after {{
                background: #ff3333;
                box-shadow: 0 0 15px #ff3333;
            }}

            .category-critical .news-item:hover {{
                background: rgba(255, 51, 51, 0.05);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- 头部 -->
            <div class="header">
                <div class="save-buttons">
                    <button class="save-btn" onclick="saveAsImage()">[保存图片]</button>
                    <button class="save-btn" onclick="window.print()">[打印]</button>
                </div>
                <div class="header-brand">// GLOBAL ALERT MONITOR</div>
                <h1 class="header-title">FORCE MAJEURE</h1>
                <div class="header-subtitle">不可抗力事件监控系统 // TRENDRADAR</div>
            </div>

            <!-- 状态栏 -->
            {status_indicators}

            <!-- 信息网格 -->
            {header_info_html}

            <!-- 内容区块 -->
            {''.join(keyword_sections) if keyword_sections else '<div class="section"><div class="no-data">暂无监控数据</div></div>'}

            <!-- 页脚 -->
            <div class="footer">
                <p>// GENERATED AT {current_time.strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p style="margin-top: 5px;">// PUSH WINDOW: 08:00-21:00 // INTERVAL: 10MIN</p>
            </div>
        </div>

        <script>
            async function saveAsImage() {{
                const container = document.querySelector('.container');
                const canvas = await html2canvas(container, {{
                    backgroundColor: '#0a0a0a',
                    scale: 2,
                    useCORS: true,
                    logging: false
                }});

                const link = document.createElement('a');
                const now = new Date();
                const filename = `TrendRadar_ForceMajeure_${{now.getFullYear()}}{{String(now.getMonth() + 1).padStart(2, '0')}}{{String(now.getDate()).padStart(2, '0')}}_${{String(now.getHours()).padStart(2, '0')}}{{String(now.getMinutes()).padStart(2, '0')}}.png`;
                link.download = filename;
                link.href = canvas.toDataURL('image/png');
                link.click();
            }}
        </script>
    </body>
    </html>
    '''

    return html


def render_rss_stats_html(stats: List[Dict], title: str = "RSS 订阅更新") -> str:
    """渲染 RSS 统计 HTML - 保持原实现"""
    # 简化实现，保持原有逻辑
    return render_html_content(
        report_data={{"stats": {"RSS": {"news": stats}}}},
        total_titles=len(stats),
        mode="current"
    )


def render_standalone_html(data: Optional[Dict]) -> str:
    """渲染独立展示区 HTML - 保持原实现"""
    if not data:
        return '<div class="no-data">无数据</div>'
    return render_html_content(
        report_data={"stats": data},
        total_titles=sum(len(v.get("news", [])) for v in data.values()),
        mode="current"
    )
