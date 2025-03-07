#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rule Engine Module

This module handles rule-based response generation for the Health Coach chatbot.
It matches user intents and entities to predefined rules to generate appropriate responses.
"""

import random

class RuleEngine:
    """Handles rule-based response generation for the chatbot."""
    
    def __init__(self, knowledge_base):
        """Initialize the rule engine with a knowledge base.
        
        Args:
            knowledge_base: An instance of KnowledgeBase containing wellness information
        """
        self.knowledge_base = knowledge_base
        
        # Define response templates for different intents
        self.response_templates = {
            'nutrition': [
                "Based on wellness guidelines, {advice}.",
                "For better nutrition, consider {advice}.",
                "A healthy diet typically includes {advice}.",
                "Nutritionists often recommend {advice}.",
                "To improve your nutrition, try {advice}."
            ],
            'fitness': [
                "For effective exercise, {advice}.",
                "To improve your fitness, try {advice}.",
                "A good workout routine includes {advice}.",
                "Fitness experts recommend {advice}.",
                "For better results, consider {advice}."
            ],
            'sleep': [
                "To improve your sleep quality, {advice}.",
                "Sleep experts suggest {advice}.",
                "For better rest, try {advice}.",
                "To address sleep issues, consider {advice}.",
                "Healthy sleep habits include {advice}."
            ],
            'stress': [
                "To manage stress effectively, {advice}.",
                "Stress reduction techniques include {advice}.",
                "Mental health experts recommend {advice}.",
                "For better stress management, try {advice}.",
                "To feel more relaxed, consider {advice}."
            ],
            'general': [
                "For overall wellness, {advice}.",
                "Health experts generally recommend {advice}.",
                "A balanced approach to health includes {advice}.",
                "For better wellbeing, consider {advice}.",
                "Wellness practices often include {advice}."
            ],
            'unknown': [
                "I'm not sure I understand. Could you ask about nutrition, fitness, sleep, or stress management?",
                "I'm specialized in wellness topics. Can I help you with nutrition, exercise, sleep, or stress?",
                "I don't have information on that topic. Would you like advice on healthy eating, exercise, sleep, or stress management?",
                "I'm designed to help with wellness questions. Could you ask something related to health, nutrition, or fitness?"
            ]
        }
    
    def match_rule(self, processed_input):
        """Match the processed input to a specific rule.
        
        Args:
            processed_input (dict): Processed user input with intent and entities
            
        Returns:
            dict: Matched rule information with response template and confidence
        """
        intent_type = processed_input['intent']['type']
        intent_confidence = processed_input['intent']['confidence']
        entities = processed_input['entities']
        
        # If we have a recognized intent with reasonable confidence
        if intent_type != 'unknown' and intent_confidence > 0.3:
            # Get relevant advice from knowledge base based on intent and entities
            advice = self.knowledge_base.get_advice(intent_type, entities)
            
            # Select a response template for the intent
            templates = self.response_templates.get(intent_type, self.response_templates['general'])
            template = random.choice(templates)
            
            return {
                'matched': True,
                'intent_type': intent_type,
                'template': template,
                'advice': advice,
                'confidence': intent_confidence
            }
        
        # Fall back to unknown intent handling
        return {
            'matched': False,
            'intent_type': 'unknown',
            'template': random.choice(self.response_templates['unknown']),
            'advice': None,
            'confidence': 0.0
        }
    
    def get_response(self, processed_input):
        """Generate a response based on processed input.
        
        Args:
            processed_input (dict): Processed user input with intent and entities
            
        Returns:
            dict: Response information with text and confidence
        """
        # Match to a rule
        rule_match = self.match_rule(processed_input)
        
        # Generate response text
        if rule_match['matched']:
            response_text = rule_match['template'].format(advice=rule_match['advice'])
        else:
            response_text = rule_match['template']
        
        return {
            'response': response_text,
            'intent_type': rule_match['intent_type'],
            'confidence': rule_match['confidence']
        }