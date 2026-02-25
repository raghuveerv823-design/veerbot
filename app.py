"""
VEERBOT - Cloud Deployment Ready Flask App
Accessible 24/7 from anywhere without needing laptop running
Works completely standalone - reads knowledge from botfile.txt
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
import uuid
import re
from datetime import timedelta

app = Flask(__name__, template_folder='templates', static_folder='static')

# ============================================================================
# SESSION CONFIGURATION
# ============================================================================
app.config['SECRET_KEY'] = 'veerbot-cloud-2026-secret-key'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ============================================================================
# CORS - Allow all devices
# ============================================================================
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"],
    "supports_credentials": True
}})

# ============================================================================
# BOTFILE DATABASE - Read knowledge from botfile.txt
# ============================================================================
BOT_DATABASE = {}
BOT_FILE = 'botfile.txt'

def load_bot_database():
    """Load Q&A pairs from botfile.txt"""
    global BOT_DATABASE
    try:
        with open(BOT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.lower().strip()
                    # Add all keywords for this answer
                    keywords = [k.strip() for k in key.split('|')]
                    for kw in keywords:
                        BOT_DATABASE[kw] = value.strip()
    except FileNotFoundError:
        BOT_DATABASE['alert'] = 'Bot Knowledge base not found'
    except Exception as e:
        BOT_DATABASE['alert'] = f'Error loading database: {str(e)}'

def search_bot_response(question):
    """Find answer from botfile.txt knowledge base"""
    question_lower = question.lower().strip()
    
    # Direct keyword match
    if question_lower in BOT_DATABASE:
        return BOT_DATABASE[question_lower]
    
    # Partial keyword match
    for keyword, answer in BOT_DATABASE.items():
        if keyword in question_lower:
            return answer
    
    # Word-by-word search
    words = question_lower.split()
    for word in words:
        if word in BOT_DATABASE:
            return BOT_DATABASE[word]
    
    # Default response
    return "Mujhe ye question samajh nahi aaya. Kripaya college ke counter ya help desk se saraashan le sakte hain."

# Load database on startup
load_bot_database()

# ============================================================================
# USER SESSION TRACKING
# ============================================================================
user_sessions = {}

def get_user_session():
    """Get or create unique session for each user"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session.permanent = True
        user_sessions[session['user_id']] = {
            'created': str(timedelta()),
            'questions': 0
        }
    return session['user_id']

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve main HTML page or handle GET queries"""
    question = request.args.get('question', '')
    user_id = get_user_session()
    
    if question:
        # Handle bot query
        answer = search_bot_response(question)
        if user_id in user_sessions:
            user_sessions[user_id]['questions'] += 1
        return jsonify({
            'status': 'success',
            'answer': answer,
            'user_id': user_id
        })
    else:
        # Serve HTML page
        return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_bot():
    """Handle POST queries"""
    try:
        user_id = get_user_session()
        data = request.get_json()
        question = data.get('question', '') if data else ''
        
        if not question:
            return jsonify({
                'status': 'error',
                'answer': 'Koi question likhiye'
            }), 400
        
        answer = search_bot_response(question)
        if user_id in user_sessions:
            user_sessions[user_id]['questions'] += 1
        
        return jsonify({
            'status': 'success',
            'answer': answer,
            'user_id': user_id
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'answer': f'Error: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'VEERBOT',
        'version': '2.0'
    })

@app.route('/api/statistics', methods=['GET'])
def statistics():
    """Get bot statistics"""
    return jsonify({
        'status': 'success',
        'total_users': len(user_sessions),
        'total_questions': sum(u.get('questions', 0) for u in user_sessions.values()),
        'knowledge_entries': len(BOT_DATABASE)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'answer': 'Page not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'status': 'error', 'answer': 'Server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
