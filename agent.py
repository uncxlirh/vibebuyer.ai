import json
import requests
import os

def load_products_by_lang(lang_code="en"):
    # 商业版逻辑：始终优先加载英文数据作为基础，防止翻译版字段缺失
    filename = f"data/products_{lang_code}.json"
    if not os.path.exists(filename):
        filename = "data/products_en.json"
    with open(filename, "r", encoding='utf-8') as f:
        return json.load(f)

def query_ollama(prompt, model="llama3.1"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.2,
        "format": "json" 
    }
    try:
        response = requests.post(url, json=data)
        return response.json().get('response', '')
    except Exception as e:
        return f'{{"error": "{str(e)}"}}'

def run_agent_reasoning(user_query, lang="en"):
    products = load_products_by_lang("en") # 强制给 AI 看英文数据，准确率最高
    
    # --- 商业级 Prompt：Solution Architect ---
    prompt = f"""
    You are VibeBuyer, a Senior Solutions Architect.
    User Goal: "{user_query}"
    
    Available Tools (Inventory):
    {json.dumps(products, ensure_ascii=False)}

    ### Your Task
    1. **Architect a Solution**: Don't just pick one item. Create a "Starter Stack" (Bundle) of 1-3 items that work together to solve the user's goal.
    2. **Calculate ROI**: Estimate how much time/money this stack saves compared to building from scratch.
    3. **Output Language**: {lang}

    ### Output JSON Format (Strict)
    {{
        "thought_process": "Brief analysis of technical requirements...",
        "stack_name": "e.g., 'SaaS MVP Starter Pack'",
        "selected_ids": [id1, id2...],
        "roi_analysis": "e.g., 'Saves ~40 hours of dev time vs manual setup.'",
        "total_vibe_score": "Average vibe score of items"
    }}
    """
    
    print(f"🧠 AI Architecting for: {user_query}...")
    raw_res = query_ollama(prompt)
    
    try:
        return json.loads(raw_res)
    except:
        return {
            "thought_process": "AI formatting error.", 
            "stack_name": "Error",
            "selected_ids": [], 
            "roi_analysis": "N/A"
        }