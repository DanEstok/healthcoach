#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NLP Processor Module

This module handles natural language processing tasks for the Health Coach chatbot.
It processes user input to extract intents and entities.
"""

import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class NLPProcessor:
    """Handles natural language processing for the chatbot."""
    
    def __init__(self):
        """Initialize the NLP processor with necessary resources."""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Health and wellness related keywords for intent recognition
        self.intent_keywords = {
            'nutrition': ['eat', 'food', 'diet', 'nutrition', 'meal', 'protein', 'carb', 'fat',
                         'vitamin', 'mineral', 'calorie', 'vegetable', 'fruit', 'meat', 'meats', 'dairy'],
            'fitness': ['exercise', 'workout', 'fitness', 'gym', 'cardio', 'strength', 'weight',
                       'run', 'jog', 'swim', 'bike', 'yoga', 'stretch', 'muscle', 'train'],
            'sleep': ['sleep', 'rest', 'insomnia', 'nap', 'tired', 'fatigue', 'bed', 'wake',
                     'dream', 'snore', 'night'],
            'stress': ['stress', 'anxiety', 'relax', 'calm', 'meditation', 'mindfulness',
                      'worry', 'tension', 'pressure', 'overwhelm'],
            'general': ['health', 'wellness', 'wellbeing', 'advice', 'tip', 'suggestion',
                       'recommendation', 'improve', 'better', 'help']
        }
        
        # Comparative and superlative terms that indicate ranking or comparison
        self.comparative_terms = ['best', 'better', 'worst', 'higher', 'highest', 'lower', 'lowest',
                                 'most', 'least', 'more', 'less', 'top', 'greatest', 'optimal']
        
    def preprocess(self, text):
        """Preprocess the text by tokenizing, removing punctuation and stopwords, and lemmatizing.
        
        Args:
            text (str): The input text to preprocess
            
        Returns:
            list: A list of preprocessed tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        processed_tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                           if token not in self.stop_words]
        
        return processed_tokens
    
    def extract_intent(self, tokens):
        """Extract the primary intent from preprocessed tokens.
        
        Args:
            tokens (list): Preprocessed tokens from user input
            
        Returns:
            dict: Intent information with type and confidence score
        """
        intent_scores = {intent: 0 for intent in self.intent_keywords}
        
        # Count matches for each intent category
        for token in tokens:
            for intent, keywords in self.intent_keywords.items():
                if token in keywords:
                    intent_scores[intent] += 1
        
        # Find the intent with the highest score
        max_score = max(intent_scores.values()) if intent_scores else 0
        if max_score == 0:
            return {'type': 'unknown', 'confidence': 0.0}
        
        # Get the intent with the highest score
        primary_intent = max(intent_scores, key=intent_scores.get)
        
        # Calculate confidence (simple ratio of matched keywords to total tokens)
        confidence = min(1.0, max_score / len(tokens)) if tokens else 0.0
        
        return {'type': primary_intent, 'confidence': confidence}
    
    def extract_entities(self, tokens):
        """Extract relevant entities from preprocessed tokens.
        
        Args:
            tokens (list): Preprocessed tokens from user input
            
        Returns:
            dict: Extracted entities by category
        """
        # Simple entity extraction based on keyword matching
        # In a more advanced implementation, this could use named entity recognition
        
        entities = {
            'food_items': [],
            'activities': [],
            'time_periods': [],
            'health_conditions': [],
            'comparative_terms': []
        }
        
        # Common food items
        food_items = ['protein', 'carb', 'fat', 'vegetable', 'fruit', 'meat', 'meats', 'dairy',
                     'egg', 'nut', 'seed', 'grain', 'bread', 'pasta', 'rice', 'fish',
                     'chicken', 'beef', 'pork', 'tofu', 'bean', 'legume', 'turkey', 'lamb',
                     'venison', 'bison', 'duck', 'goose', 'quail', 'rabbit', 'seafood',
                     'salmon', 'tuna', 'cod', 'halibut', 'shrimp', 'crab', 'lobster']
        
        # Common activities
        activities = ['run', 'jog', 'walk', 'swim', 'bike', 'yoga', 'gym', 'exercise',
                     'workout', 'lift', 'stretch', 'meditate', 'sleep', 'rest']
        
        # Time periods
        time_periods = ['morning', 'afternoon', 'evening', 'night', 'day', 'week',
                       'month', 'year', 'hour', 'minute', 'daily', 'weekly']
        
        # Common health conditions
        health_conditions = ['stress', 'anxiety', 'depression', 'insomnia', 'fatigue',
                           'pain', 'headache', 'migraine', 'allergy', 'diabetes',
                           'hypertension', 'obesity', 'overweight']
        
        # Extract entities by category
        for token in tokens:
            if token in food_items:
                entities['food_items'].append(token)
            if token in activities:
                entities['activities'].append(token)
            if token in time_periods:
                entities['time_periods'].append(token)
            if token in health_conditions:
                entities['health_conditions'].append(token)
            if token in self.comparative_terms:
                entities['comparative_terms'].append(token)
        
        # Special case for 'meat' and 'protein' related queries
        if ('meat' in tokens or 'meats' in tokens) and 'protein' in tokens:
            if 'meat' not in entities['food_items']:
                entities['food_items'].append('meat')
            if 'protein' not in entities['food_items']:
                entities['food_items'].append('protein')
        
        # Check for comparative queries about protein in meat
        if any(term in tokens for term in self.comparative_terms) and ('protein' in tokens or 'proteins' in tokens):
            if 'protein' not in entities['food_items']:
                entities['food_items'].append('protein')
            
            # If talking about best/highest protein and meat is mentioned or implied
            if ('meat' in tokens or 'meats' in tokens):
                if 'meat' not in entities['food_items']:
                    entities['food_items'].append('meat')
        
        return entities
    
    def process(self, text):
        """Process the input text and extract structured information.
        
        Args:
            text (str): The user's input text
            
        Returns:
            dict: Structured information extracted from the text
        """
        # Preprocess the text
        tokens = self.preprocess(text)
        
        # Extract intent
        intent = self.extract_intent(tokens)
        
        # Extract entities
        entities = self.extract_entities(tokens)
        
        # Special case handling for protein/meat queries
        if 'best' in text.lower() and 'meat' in text.lower() and 'protein' in text.lower():
            intent['type'] = 'nutrition'  # Force nutrition intent
            if 'meat' not in entities['food_items']:
                entities['food_items'].append('meat')
            if 'protein' not in entities['food_items']:
                entities['food_items'].append('protein')
        
        # Return structured information
        return {
            'original_text': text,
            'processed_tokens': tokens,
            'intent': intent,
            'entities': entities
        }