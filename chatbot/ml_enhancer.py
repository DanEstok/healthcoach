#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ML Enhancer Module

This module provides machine learning enhancements for the Health Coach chatbot.
It improves response personalization when rule-based responses have low confidence.
Integrates with Hugging Face models for advanced NLP capabilities.
"""

import random
import os
from collections import Counter
from typing import Dict, Optional, List, Union

# Import the HFModels class
from chatbot.hf_models import HFModels

class MLEnhancer:
    """Enhances chatbot responses using machine learning techniques."""
    
    def __init__(self, user_profile=None):
        """Initialize the ML enhancer with necessary resources.
        
        Args:
            user_profile (UserProfile, optional): User profile for personalization
        """
        # Store user profile if provided
        self.user_profile = user_profile
        
        # Initialize Hugging Face models
        self.hf_models = HFModels()
        
        # Health and wellness related keywords for intent recognition (copied from NLPProcessor)
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
        
        # Personalization factors for different user profiles
        self.personalization_factors = {
            'beginner': {
                'nutrition': "start with simple dietary changes",
                'fitness': "begin with gentle, low-impact exercises",
                'sleep': "focus on establishing a consistent sleep schedule",
                'stress': "try basic breathing exercises for stress reduction"
            },
            'intermediate': {
                'nutrition': "experiment with meal planning and preparation",
                'fitness': "incorporate varied workout routines for different muscle groups",
                'sleep': "optimize your sleep environment and pre-sleep routine",
                'stress': "practice regular mindfulness meditation sessions"
            },
            'advanced': {
                'nutrition': "fine-tune your macronutrient ratios for optimal performance",
                'fitness': "consider periodization in your training program",
                'sleep': "analyze your sleep cycles and optimize for deep sleep phases",
                'stress': "develop a comprehensive stress management strategy"
            }
        }
        
        # Dietary restriction response modifiers
        self.dietary_modifiers = {
            'vegetarian': "focusing on plant-based protein sources like legumes, tofu, and tempeh",
            'vegan': "incorporating a variety of plant foods to ensure complete nutrition",
            'gluten-free': "choosing naturally gluten-free grains like rice, quinoa, and buckwheat",
            'dairy-free': "using plant-based alternatives for calcium and protein",
            'keto': "prioritizing healthy fats and keeping carbohydrates minimal",
            'paleo': "focusing on whole foods that align with ancestral eating patterns"
        }
        
        # Context-aware response enhancers
        self.context_enhancers = {
            'time_sensitive': [
                "This is especially important in the {time_period} when your body needs {need}.",
                "Many people find this most effective during the {time_period}.",
                "Consider adapting this advice for your {time_period} routine."
            ],
            'condition_specific': [
                "This approach can be particularly helpful for managing {condition}.",
                "People with {condition} often benefit from these adjustments.",
                "When dealing with {condition}, it's important to {adaptation}."
            ],
            'goal_oriented': [
                "This strategy aligns well with your goal to {goal}.",
                "To achieve {goal}, consistency with this approach is key.",
                "Many who successfully {goal} find this technique valuable."
            ]
        }
        
        # Simple user context memory (would be expanded in a real implementation)
        self.user_context = {
            'interaction_count': 0,
            'mentioned_topics': Counter(),
            'inferred_level': 'beginner',  # Default starting point
            'recent_concerns': []
        }
    
    def update_user_context(self, processed_input):
        """Update the user context based on the current interaction.
        
        Args:
            processed_input (dict): Processed user input with intent and entities
        """
        # Increment interaction count
        self.user_context['interaction_count'] += 1
        
        # Track mentioned topics
        intent_type = processed_input['intent']['type']
        if intent_type != 'unknown':
            self.user_context['mentioned_topics'][intent_type] += 1
        
        # Track recent concerns from health conditions
        if processed_input['entities']['health_conditions']:
            self.user_context['recent_concerns'] = processed_input['entities']['health_conditions']
        
        # Infer user level based on interaction patterns (simplified)
        if self.user_context['interaction_count'] > 10:
            self.user_context['inferred_level'] = 'intermediate'
        if self.user_context['interaction_count'] > 25:
            self.user_context['inferred_level'] = 'advanced'
    
    def enhance_response(self, processed_input, rule_response):
        """Enhance a rule-based response using ML techniques.
        
        Args:
            processed_input (dict): Processed user input with intent and entities
            rule_response (dict): Response from the rule engine
            
        Returns:
            str: Enhanced response text
        """
        # Update user context with current interaction
        self.update_user_context(processed_input)
        
        # Get the base response text
        response_text = rule_response['response']
        intent_type = rule_response['intent_type']
        
        # Use Hugging Face models for better intent classification
        candidate_labels = list(self.intent_keywords.keys())
        hf_intent_result = self.hf_models.classify_intent(processed_input['original_text'], candidate_labels)
        
        # If HF model is more confident about a different intent, use that instead
        if hf_intent_result['scores'][0] > rule_response.get('confidence', 0):
            intent_type = hf_intent_result['labels'][0]
            
        # If we have relevant context, use the QA model to enhance the response
        if rule_response.get('context'):
            qa_result = self.hf_models.answer_question(
                question=processed_input['original_text'],
                context=rule_response['context']
            )
            if qa_result['score'] > 0.7:  # Only use if confident
                response_text = qa_result['answer']
        
        # Use semantic search to find best matching responses if confidence is low
        if rule_response.get('confidence', 0) < 0.6:
            candidates = rule_response.get('alternative_responses', [])
            if candidates:
                best_matches = self.hf_models.find_best_matches(
                    query=processed_input['original_text'],
                    candidates=candidates
                )
                if best_matches and best_matches[0][1] > 0.7:  # If good match found
                    response_text = best_matches[0][0]
        
        # Get personalization context from user profile if available
        if self.user_profile:
            personalization_context = self.user_profile.get_personalization_context()
            user_level = personalization_context['fitness_level']
            dietary_restrictions = personalization_context['dietary_restrictions']
            health_goals = personalization_context['current_goals']
            interaction_level = personalization_context['interaction_level']
            frequent_topics = personalization_context['frequent_topics']
        else:
            # Fall back to inferred level if no user profile
            user_level = self.user_context['inferred_level']
            dietary_restrictions = []
            health_goals = []
            interaction_level = 'new'
            frequent_topics = []
        
        # Add personalization based on user level
        if intent_type in self.personalization_factors[user_level]:
            personalization = self.personalization_factors[user_level][intent_type]
            response_text += f" As you continue your wellness journey, {personalization}."
        
        # Add context enhancement if applicable
        entities = processed_input['entities']
        
        # Add dietary restriction personalization if applicable
        if intent_type == 'nutrition' and dietary_restrictions and random.random() < 0.8:  # 80% chance to apply
            restriction = random.choice(dietary_restrictions)
            if restriction in self.dietary_modifiers:
                modifier = self.dietary_modifiers[restriction]
                response_text += f" For your {restriction} diet, consider {modifier}."
        
        # Time-sensitive enhancement
        if entities['time_periods'] and random.random() < 0.7:  # 70% chance to apply
            time_period = entities['time_periods'][0]
            needs_map = {
                'morning': 'energy',
                'afternoon': 'focus',
                'evening': 'relaxation',
                'night': 'recovery'
            }
            need = needs_map.get(time_period, 'support')
            
            enhancer = random.choice(self.context_enhancers['time_sensitive'])
            response_text += " " + enhancer.format(time_period=time_period, need=need)
        
        # Condition-specific enhancement
        if entities['health_conditions'] and random.random() < 0.8:  # 80% chance to apply
            condition = entities['health_conditions'][0]
            adaptations = {
                'stress': 'prioritize self-care',
                'anxiety': 'practice grounding techniques',
                'insomnia': 'maintain a consistent sleep schedule',
                'fatigue': 'balance activity with proper rest',
                'pain': 'consult with a healthcare professional'
            }
            adaptation = adaptations.get(condition, 'listen to your body')
            
            enhancer = random.choice(self.context_enhancers['condition_specific'])
            response_text += " " + enhancer.format(condition=condition, adaptation=adaptation)
        
        # Goal-oriented enhancement
        if health_goals and random.random() < 0.75:  # 75% chance to apply
            goal = random.choice(health_goals)
            enhancer = random.choice(self.context_enhancers['goal_oriented'])
            response_text += " " + enhancer.format(goal=goal)
        
        # Add a disclaimer for low-confidence responses
        if rule_response.get('confidence', 0) < 0.4:
            response_text += "\n\nNote: This is general advice. For personalized guidance, consider consulting with a healthcare professional."
        
        return response_text