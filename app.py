import streamlit as st
import json
import os
import time
from pathlib import Path

from chain_utils import get_balance, buy_item_on_chain, check_connection
from agent import run_agent_reasoning

# ---------------- 0. Page Config ----------------
st.set_page_config(
    page_title="VibeBuyer Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- 1. 加载外部 CSS ----------------
def load_css(path: str = "style.css"):
    css_path = Path(path)
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )
    else:
        st.warning(f"CSS file not found: {path}")

load_css("style.css")

# ---------------- 2. 多语言字典 ----------------
LANGUAGES = {
    "🇺🇸 English": "en",
    "🇨🇳 中文": "zh",
    "🇯🇵 日本語": "ja",
}

UI_TEXT = {
    # ... 这里继续写你刚才那段 UI_TEXT 配置
}


UI_TEXT = {
    "en": {
        "hero_title_1": "Build Faster.",
        "hero_title_2": "Procure Smarter.",
        "hero_sub": "The AI-Native protocol for autonomous digital asset procurement.",
        "metric_agents": "Active Agents",
        "metric_volume": "Volume (BNB)",
        "metric_savings": "Avg. Savings",
        "metric_fee": "Protocol Fee",
        "input_placeholder": "e.g. “I want to build a SaaS MVP with Auth and DB”",
        "btn_generate": "Generate Stack ⚡",
        "wallet_connected": "Connected",
        "wallet_disconnected": "Wallet Disconnected",
        "ai_thinking": "🧠 AI Architect is analyzing requirements...",
        "ai_note": "Architect's Note",
        "roi_label": "Target ROI",
        "rec_stack": "Recommended Stack",
        "buy_all": "Purchase All",
        "buy_now": "Buy Now",
        "buy_now_short": "Buy",
        "all_products_title": "All Assets",
        "explore_title": "Explore Ecosystem",
        "success_msg": "Transaction Complete!",
        "processing": "Initiating Smart Contracts...",
        "acquiring": "Acquiring",
        "protocol_stats": "Protocol at a glance",
    },
    "zh": {
        "hero_title_1": "开发更极速。",
        "hero_title_2": "采购更智能。",
        "hero_sub": "专为独立开发者打造的原生 AI 自动化采购协议。",
        "metric_agents": "活跃智能体",
        "metric_volume": "交易量 (BNB)",
        "metric_savings": "平均节省",
        "metric_fee": "协议费率",
        "input_placeholder": "例如：“我想做一个带用户系统的 SaaS MVP”",
        "btn_generate": "生成技术栈方案 ⚡",
        "wallet_connected": "已连接",
        "wallet_disconnected": "钱包未连接",
        "ai_thinking": "🧠 AI 架构师正在分析需求...",
        "ai_note": "架构师备注",
        "roi_label": "预估 ROI",
        "rec_stack": "推荐组合方案",
        "buy_all": "一键购买全套",
        "buy_now": "立即购买",
        "buy_now_short": "购买",
        "all_products_title": "全部资产",
        "explore_title": "探索生态系统",
        "success_msg": "交易完成！",
        "processing": "正在启动智能合约...",
        "acquiring": "正在获取",
        "protocol_stats": "协议全局概览",
    },
    "ja": {
        "hero_title_1": "開発を加速。",
        "hero_title_2": "調達を賢く。",
        "hero_sub": "自律的なデジタル資産調達のためのAIネイティブプロトコル。",
        "metric_agents": "アクティブAgent",
        "metric_volume": "取引高 (BNB)",
        "metric_savings": "平均節約率",
        "metric_fee": "プロトコル手数料",
        "input_placeholder": "例：「認証とDBを備えたSaaS MVPを作りたい」",
        "btn_generate": "スタック生成 ⚡",
        "wallet_connected": "接続済み",
        "wallet_disconnected": "未接続",
        "ai_thinking": "🧠 AIアーキテクトが分析中...",
        "ai_note": "アーキテクトのメモ",
        "roi_label": "目標 ROI",
        "rec_stack": "推奨スタック",
        "buy_all": "一括購入",
        "buy_now": "今すぐ購入",
        "buy_now_short": "購入",
        "all_products_title": "すべてのアセット",
        "explore_title": "エコシステムを探索",
        "success_msg": "取引完了！",
        "processing": "スマートコントラクトを開始中...",
        "acquiring": "取得中",
        "protocol_stats": "プロトコル概要",
    },
}



# ---------------- 3. 侧边栏逻辑 (多语言切换) ----------------
with st.sidebar:
    # 新增：包一层重一点的卡片
    st.markdown('<div class="sidebar-inner">', unsafe_allow_html=True)

    st.markdown("### ⚡ VibeBuyer")
    st.caption("Pro Edition v3.0")
    st.markdown("---")

    selected_lang_label = st.selectbox("Language / 语言", list(LANGUAGES.keys()))
    lang_code = LANGUAGES[selected_lang_label]
    t = UI_TEXT[lang_code]

    st.markdown("---")

    if check_connection():
        bal = get_balance()
        st.success(f"**{t['wallet_connected']}**  \n`{bal:.4f} BNB`")
    else:
        st.error(t["wallet_disconnected"])

    st.markdown("---")
    st.info("💡 Pro Tip:\nAsk for “Full Stack” to get a curated bundle.")

    st.markdown('</div>', unsafe_allow_html=True)  # 结束 sidebar-inner

# ---------------- 4. Hero Section ----------------
st.markdown(
    f"""
<div class="hero-wrapper">
    <div class="hero-text">
        {t['hero_title_1']}<br/>
        <span class="hero-highlight">{t['hero_title_2']}</span>
    </div>
    <div class="hero-sub">
        {t['hero_sub']}
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------- 5. Dashboard Metrics ----------------
st.markdown(f"<div class='section-label'>{t['protocol_stats']}</div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric(t["metric_agents"], "1,024", "+12%")
c2.metric(t["metric_volume"], "450.2", "+5%")
c3.metric(t["metric_savings"], "34%", "High")
c4.metric(t["metric_fee"], "1.0%", "Live")

st.markdown("<br/>", unsafe_allow_html=True)

# ---------------- 工具函数：加载产品数据（带 cache） ----------------
@st.cache_data
def load_products(lang: str):
    data_file = f"data/products_{lang}.json"
    if not os.path.exists(data_file):
        data_file = "data/products_en.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------- 6. 输入区 + AI 逻辑与展示 ----------------
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)

    with st.form("main_input"):
        col_in, col_btn = st.columns([3, 1])

        with col_in:
            query = st.text_input(
                "",
                placeholder=t["input_placeholder"],
                label_visibility="collapsed",
            )

        with col_btn:
            submitted = st.form_submit_button(
                t["btn_generate"],
                use_container_width=True,
            )

    if submitted and query:
        st.markdown("<br/>", unsafe_allow_html=True)
        with st.spinner(t["ai_thinking"]):
            res = run_agent_reasoning(query, lang=lang_code)

        st.markdown(
            f"""
        <div class="ai-box">
            <h4>🤖 {t['ai_note']}</h4>
            <p>"{res.get('thought_process', 'Processing...')}"</p>
            <div class="ai-meta">
                <span>{t['roi_label']}:</span> {res.get('roi_analysis', 'N/A')}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(f"#### 📦 {t['rec_stack']}: {res.get('stack_name', 'Custom Bundle')}")
        st.markdown("<br/>", unsafe_allow_html=True)

        all_products = load_products(lang_code)
        selected_ids = res.get("selected_ids", [])
        stack_items = [p for p in all_products if p["id"] in selected_ids]

        if stack_items:
            cols = st.columns(len(stack_items))
            for idx, item in enumerate(stack_items):
                with cols[idx]:
                    st.markdown(
                        f"""
                    <div class="vibe-card">
                        <div class="vibe-tag">{item.get('vibe_score', 9.0)} Vibe Score</div>
                        <div class="card-title">{item['name']}</div>
                        <div class="card-desc">{item['description'][:90]}...</div>
                        <div class="card-price">{item['price']} BNB</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

            st.markdown("<br/>", unsafe_allow_html=True)

            total_price = sum(item["price"] for item in stack_items)
            buy_text = f"{t['buy_all']} ({total_price:.4f} BNB)"

            if st.button(buy_text, type="primary", use_container_width=True):
                prog_bar = st.progress(0, text=t["processing"])
                hashes = []
                for i, item in enumerate(stack_items):
                    time.sleep(0.5)
                    prog_bar.progress(
                        (i + 1) / len(stack_items),
                        text=f"{t['acquiring']} {item['name']}...",
                    )
                    r = buy_item_on_chain(item["id"], item["price"])
                    if r.get("status") == "success":
                        hashes.append(r["tx_hash"])

                prog_bar.empty()
                st.balloons()
                st.success(f"✅ {t['success_msg']}")
                for h in hashes:
                    tx_url = f"https://testnet.bscscan.com/tx/{h}"
                    st.markdown(f"🔗 [BSCScan Receipt]({tx_url})")
        else:
            st.warning("No matching items found via AI.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- 7. 底部商品展示：所有商品 + 单品购买 ----------------
st.markdown("<br/><br/>", unsafe_allow_html=True)
st.markdown(f"### {t.get('all_products_title', t['explore_title'])}")
st.markdown("---")

products = load_products(lang_code)

# 一行多少列可以自己调：3 / 4 看你产品多不多
num_cols = 4
cols = st.columns(num_cols)

for idx, p in enumerate(products):
    col = cols[idx % num_cols]
    with col:
        st.markdown(
            f"""
            <div class="vibe-card" style="margin-bottom: 16px;">
                <div class="vibe-tag">{p.get('vibe_score', 9.0)} Vibe Score</div>
                <div class="card-title">{p['name']}</div>
                <div class="card-desc">{p.get('description', '')[:80]}...</div>
                <div class="card-price">{p['price']} BNB</div>
                <div style="font-size:12px; color:#8E8E93; margin-top:4px;">
                    {p.get('category', 'General')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 单个商品购买按钮（注意 key，避免重复）
        if st.button(
            t.get("buy_now", "Buy Now"),
            key=f"buy_single_{p['id']}",
            use_container_width=True,
        ):
            with st.spinner(t["processing"]):
                res = buy_item_on_chain(p["id"], p["price"])
            if res.get("status") == "success":
                tx_url = f"https://testnet.bscscan.com/tx/{res['tx_hash']}"
                st.success(f"✅ {t['success_msg']}")
                st.markdown(f"🔗 [BSCScan Receipt]({tx_url})")
            else:
                st.error("Transaction failed, please try again.")
