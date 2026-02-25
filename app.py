from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from collections import Counter
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'veerbot-admin-v3-2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
CORS(app)

BOT_FILE = 'botfile.txt'
UNKNOWN_FILE = 'unknown_questions.txt'

# ============================================================================
# DATABASE UTILITIES
# ============================================================================
def load_db():
    db = {}
    if os.path.exists(BOT_FILE):
        with open(BOT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    k, v = line.split(':', 1)
                    keys = [item.strip().lower() for item in k.split('|')]
                    for key in keys: db[key] = v.strip()
    return db

def save_to_db(keyword, answer):
    with open(BOT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n{keyword}:{answer}")

def get_smart_unknowns():
    """Sirf wo sawal jo 1 se zyada baar puche gaye hain unhe frequency ke sath dikhaye"""
    if not os.path.exists(UNKNOWN_FILE): return []
    with open(UNKNOWN_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    counts = Counter(lines)
    # Sirf wahi questions jo > 1 baar puche gaye hain
    popular = [q for q, count in counts.items() if count > 1]
    return popular

def clear_unknowns():
    if os.path.exists(UNKNOWN_FILE):
        open(UNKNOWN_FILE, 'w').close()

# ============================================================================
# MAIN CHAT & ADMIN LOGIC
# ============================================================================
@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('question', '').strip()
    db = load_db()

    # --- ADMIN TRIGGER ---
    if user_input.lower() == 'admin':
        return jsonify({'answer': "ADMIN MODE: Username:Password bhejiye (e.g. veer123:veerbot123)"})

    # --- ADMIN LOGIN ---
    if ':' in user_input and 'veer123' in user_input:
        parts = user_input.split(':')
        if parts[0] == 'veer123' and parts[1] == 'veerbot123':
            session['admin_active'] = True
            session.pop('mode', None)
            return jsonify({'answer': "Welcome Veer! 🕶️\n\n1. View New Questions List\n2. Update Old Data\n3. Add New Data\n\nKaunsa option chunenge?"})

    # --- ADMIN PROCESSOR ---
    if session.get('admin_active'):
        
        # 1. LOGOUT (Poori safai ke sath)
        if user_input.lower() == 'logout':
            clear_unknowns() # Aapne kaha tha ek baar dekhne ke baad delete ho jaye
            session.clear()
            return jsonify({'answer': "Admin Logged Out. Unknown questions file saaf kar di gayi hai. Ab aap normal chat kar sakte hain."})

        # 2. SHOW LIST (Option 1)
        if user_input == '1':
            questions = get_smart_unknowns()
            if not questions:
                return jsonify({'answer': "Abhi koi aise sawal nahi hain jo baar-baar puche gaye hon. Admin menu: 1, 2, 3"})
            
            session['current_list'] = questions
            session['mode'] = 'selecting_q'
            
            msg = "Ye rahe wo sawal jo baar-baar puche gaye hain:\n\n"
            for i, q in enumerate(questions, 1):
                msg += f"{i}. {q}\n"
            msg += "\nKiske liye answer add karna hai? Number type karein."
            return jsonify({'answer': msg})

        # 3. SELECT QUESTION FROM LIST
        if session.get('mode') == 'selecting_q' and user_input.isdigit():
            idx = int(user_input) - 1
            q_list = session.get('current_list', [])
            if 0 <= idx < len(q_list):
                session['selected_q'] = q_list[idx]
                session['mode'] = 'writing_ans'
                return jsonify({'answer': f"Selected: '{q_list[idx]}'\n\nAb iska jawab likhiye format mein -> keyword:answer"})
            else:
                return jsonify({'answer': "Galat number! List mein se sahi number chunein."})

        # 4. SAVE ANSWER & RETURN TO LIST
        if session.get('mode') == 'writing_ans' and ':' in user_input:
            kw, ans = user_input.split(':', 1)
            save_to_db(kw.strip().lower(), ans.strip())
            session['mode'] = 'selecting_q' # Wapas selection mode mein
            return jsonify({'answer': f"'{kw}' save ho gaya! ✅\n\nAb agla number type karein ya 'logout' likhein list khatam karne ke liye."})

        # 5. DIRECT ADD (Option 2/3)
        if user_input in ['2', '3']:
            session['mode'] = 'direct_add'
            return jsonify({'answer': "Direct Add Mode: keyword:answer bhejiye."})
        
        if session.get('mode') == 'direct_add' and ':' in user_input:
            kw, ans = user_input.split(':', 1)
            save_to_db(kw.strip().lower(), ans.strip())
            return jsonify({'answer': "Data saved! Aur add karna hai? (Ya logout likhein)"})

    # --- NORMAL CHAT LOGIC ---
    user_q = user_input.lower()
    
    # 1. Admin Options Logic
    if user_q == "admin":
        res = ("Admin Mode Active! Please choose an option:\n"
               "1. Add answer to Today's new question\n"
               "2. Update old data\n"
               "3. Add new data")
        return jsonify({'answer': res})

    # 2. Holiday/Leave Logic (Chutti ke liye)
    holiday_keywords = ["holiday", "chutti", "leave"]
    if any(word in user_q for word in holiday_keywords):
        res = "Bot: Aaj chutti ki jaankari ke liye admin se sampark karein ya 'admin' type karke data update karein."
        return jsonify({'answer': res})

    # 3. Database Search (Purana Logic)
    if user_q in db:
        return jsonify({'answer': db[user_q]})

    for k, v in db.items():
        if k in user_q:
            return jsonify({'answer': v})

    # 4. Naya Default Message aur Unknown Question Save karna
    default_res = "Maaf kijiye abhi mujhe iss baare me koi jaankari nahi hai, mai aage aapko update karunga."
    with open(UNKNOWN_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{user_q}\n")

    return jsonify({'answer': default_res})
@app.route('/')
def home(): return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))