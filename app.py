from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'veerbot-cloud-2026-master-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
CORS(app)

BOT_FILE = 'botfile.txt'
UNKNOWN_FILE = 'unknown_questions.txt'

# ============================================================================
# DATA HELPERS
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

def get_unknown_list():
    if os.path.exists(UNKNOWN_FILE):
        with open(UNKNOWN_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    return []

def clear_unknown_file():
    if os.path.exists(UNKNOWN_FILE):
        open(UNKNOWN_FILE, 'w').close()

# ============================================================================
# BOT LOGIC
# ============================================================================
@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get('question', '').strip()
    db = load_db()

    # 1. ADMIN TRIGGER & AUTH
    if user_input.lower() == 'admin':
        return jsonify({'answer': "Admin Mode: Username aur Password bhejiye (Format: user:pass)"})

    if ':' in user_input and 'veer123' in user_input:
        parts = user_input.split(':')
        if parts[0] == 'veer123' and parts[1] == 'veerbot123':
            session['admin_logged_in'] = True
            session.pop('unknown_index', None) # Reset unknown pointer
            return jsonify({'answer': "Welcome Veer!\n1. Add answer to Today's new questions\n2. Update old data\n3. Add new data\n\nKaunsa option chunenge? (Type 1, 2, ya 3)"})

    # 2. ADMIN ACTIONS LOGIC
    if session.get('admin_logged_in'):
        # --- Option 1: Unknown Questions Interactive ---
        if user_input == '1' or session.get('mode') == 'unknown':
            questions = get_unknown_list()
            if not questions:
                session.pop('mode', None)
                return jsonify({'answer': "Koi bhi naya sawal pending nahi hai. Admin menu: 1, 2, 3"})
            
            idx = session.get('unknown_index', 0)
            session['mode'] = 'unknown'

            # User gave answer for current question
            if ':' in user_input and session.get('waiting_ans'):
                kw, ans = user_input.split(':', 1)
                save_to_db(kw.strip().lower(), ans.strip())
                idx += 1
                session['unknown_index'] = idx
            elif user_input.lower() == 'cut':
                idx += 1
                session['unknown_index'] = idx

            if idx < len(questions):
                session['waiting_ans'] = True
                return jsonify({'answer': f"Question {idx+1}/{len(questions)}: '{questions[idx]}'\n\nReply karein (keyword:answer) ya skip karne ke liye 'cut' likhein."})
            else:
                clear_unknown_file()
                session.pop('mode', None)
                session.pop('unknown_index', None)
                return jsonify({'answer': "Saare questions khatam! File clean kar di gayi hai. Admin menu: 1, 2, 3"})

        # --- Option 2 & 3: Direct Update/Add ---
        if user_input in ['2', '3']:
            session['mode'] = 'manual_add'
            return jsonify({'answer': "Theek hai. Naya data is format mein bhejiye -> keyword:answer"})

        if session.get('mode') == 'manual_add' and ':' in user_input:
            kw, ans = user_input.split(':', 1)
            save_to_db(kw.strip().lower(), ans.strip())
            return jsonify({'answer': f"'{kw}' update ho gaya! Aur add karna hai? (Ya logout likhein)"})

        if user_input.lower() == 'logout':
            session.clear()
            return jsonify({'answer': "Admin Logged Out."})

    # 3. NORMAL CHAT LOGIC
    user_q = user_input.lower()
    if user_q in db:
        return jsonify({'answer': db[user_q]})
    
    for k, v in db.items():
        if k in user_q: return jsonify({'answer': v})

    # Log Unknown Question
    with open(UNKNOWN_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{user_input}\n")
    return jsonify({'answer': "Maaf kijiye abhi mujhe iss baare mein koi jaankari nahi hai, main aage aapko update karunga."})

@app.route('/')
def home(): return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))