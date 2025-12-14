import json
import requests
import os

def load_products_by_lang(lang_code="en"):
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

def run_agent_reasoning(user_query, lang="en", preferred_ids=None):
    if preferred_ids is None:
        preferred_ids = []
        
    products = load_products_by_lang("en") 
    
    preferred_context = ""
    if preferred_ids:
        p_names = [p['name'] for p in products if p['id'] in preferred_ids]
        preferred_context = f"\nUser explicitly PINNED/LIKED these tools: {', '.join(p_names)}. You MUST try to include them in the stack if they fit."


    prompt = f"""
    You are VibeBuyer, a Senior Solutions Architect.
    User Goal: "{user_query}"
    
    {preferred_context}
    
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
