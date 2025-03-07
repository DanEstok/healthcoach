#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Health Coach Chatbot - Web Interface

This module provides a Flask web interface for the Health Coach chatbot.
It allows users to interact with the chatbot through a browser.
"""

import os
import uuid
from flask import Flask, render_template, request, jsonify, session
from app import HealthCoachChatbot

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24).hex())

# Dictionary to store chatbot instances for each user
user_chatbots = {}

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Process user query and return chatbot response."""
    user_input = request.form['user_input']
    feedback = request.form.get('feedback', None)
    
    if not user_input.strip():
        return jsonify({'response': 'Please enter a question about health, nutrition, or fitness.'})
    
    # Get or create user session ID
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_id = session['user_id']
    
    # Get or create chatbot instance for this user
    if user_id not in user_chatbots:
        user_chatbots[user_id] = HealthCoachChatbot(user_id=user_id)
    
    # Get response from chatbot
    response = user_chatbots[user_id].process_input(user_input, feedback)
    
    return jsonify({'response': response})

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080, debug=True)