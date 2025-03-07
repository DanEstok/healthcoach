#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced Knowledge Base Module

This module provides an enhanced knowledge base of wellness information for the Health Coach chatbot.
It contains structured information about nutrition, fitness, sleep, and stress management.
This version includes more specific subcategories for better response targeting.
"""

import random

class KnowledgeBase:
    """Stores and provides access to wellness information."""
    
    def __init__(self):
        """Initialize the knowledge base with wellness information."""
        # Nutrition advice by category
        self.nutrition_advice = {
            'general': [
                "aim for a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains",
                "stay hydrated by drinking at least 8 glasses of water daily",
                "limit processed foods, added sugars, and excessive salt intake",
                "practice portion control and mindful eating",
                "include a variety of colorful foods in your meals for diverse nutrients"
            ],
            'energy': [
                "eat regular meals with a balance of complex carbohydrates and proteins",
                "include iron-rich foods like leafy greens, beans, and lean meats to combat fatigue",
                "choose whole grains over refined carbohydrates for sustained energy",
                "incorporate healthy fats from nuts, seeds, and avocados",
                "have small, frequent meals to maintain steady blood sugar levels"
            ],
            'protein': [
                "include lean meats, poultry, fish, beans, eggs, and nuts in your diet",
                "for plant-based options, try tofu, tempeh, lentils, and quinoa",
                "Greek yogurt and cottage cheese are excellent high-protein dairy options",
                "aim for 0.8-1 gram of protein per kilogram of body weight daily",
                "distribute protein intake throughout the day for optimal muscle maintenance"
            ],
            'meat': [
                "choose lean cuts of beef like sirloin, tenderloin, and 93% lean ground beef for high protein with less fat",
                "opt for skinless chicken breast and turkey breast which provide excellent protein-to-fat ratios",
                "include fish like salmon, tuna, and cod which offer high-quality protein plus beneficial omega-3 fatty acids",
                "consider lean pork options such as tenderloin and center-cut chops for variety in your protein sources",
                "game meats like bison and venison typically offer more protein and less fat than conventional beef"
            ],
            'weight_management': [
                "focus on nutrient-dense foods rather than calorie restriction",
                "increase fiber intake through fruits, vegetables, and whole grains",
                "be mindful of portion sizes and eat slowly to recognize fullness cues",
                "prepare meals at home to control ingredients and cooking methods",
                "choose lean proteins and healthy fats that promote satiety"
            ]
        }
        
        # Fitness advice by category
        self.fitness_advice = {
            'general': [
                "aim for at least 150 minutes of moderate aerobic activity weekly",
                "include strength training exercises at least twice per week",
                "incorporate flexibility and balance exercises into your routine",
                "find activities you enjoy to make exercise sustainable",
                "start gradually and progressively increase intensity over time"
            ],
            'cardio': [
                "try activities like walking, jogging, cycling, or swimming",
                "aim for 20-30 minutes of elevated heart rate activity most days",
                "mix high-intensity intervals with moderate activity for efficiency",
                "monitor your heart rate to ensure you're working at an appropriate intensity",
                "include a proper warm-up and cool-down with each session"
            ],
            'strength': [
                "focus on major muscle groups: legs, hips, back, chest, abdomen, shoulders, and arms",
                "start with bodyweight exercises before adding external resistance",
                "aim for 8-12 repetitions per set for general strength building",
                "allow 48 hours of recovery between working the same muscle groups",
                "maintain proper form to prevent injury and maximize benefits"
            ],
            'quick_workouts': [
                "try a 10-minute circuit of bodyweight exercises like push-ups, squats, and lunges",
                "take a brisk 15-minute walk during your break",
                "do 5 minutes of stair climbing for an efficient cardio burst",
                "practice desk exercises like seated leg raises and chair dips",
                "use resistance bands for a quick full-body workout anywhere"
            ]
        }
        
        # Sleep advice by category
        self.sleep_advice = {
            'general': [
                "aim for 7-9 hours of quality sleep per night",
                "maintain a consistent sleep schedule, even on weekends",
                "create a restful environment that's dark, quiet, and cool",
                "limit exposure to screens at least an hour before bedtime",
                "establish a relaxing bedtime routine to signal your body it's time to sleep"
            ],
            'insomnia': [
                "avoid caffeine, alcohol, and large meals close to bedtime",
                "try relaxation techniques like deep breathing or progressive muscle relaxation",
                "if you can't fall asleep within 20 minutes, get up and do something calming",
                "limit daytime naps to 30 minutes or less",
                "consider cognitive behavioral therapy specifically designed for insomnia"
            ],
            'environment': [
                "invest in a comfortable mattress and pillows that support your sleep position",
                "use blackout curtains or an eye mask to block unwanted light",
                "consider white noise or earplugs to mask disruptive sounds",
                "keep your bedroom at a comfortable temperature between 60-67°F (15-19°C)",
                "remove electronic devices and work materials from your sleep space"
            ]
        }
        
        # Stress management advice by category
        self.stress_advice = {
            'general': [
                "practice mindfulness meditation for at least 10 minutes daily",
                "engage in regular physical activity to reduce stress hormones",
                "maintain social connections and talk about your feelings",
                "set realistic goals and priorities to avoid feeling overwhelmed",
                "make time for hobbies and activities you enjoy"
            ],
            'techniques': [
                "try deep breathing exercises: inhale for 4 counts, hold for 7, exhale for 8",
                "practice progressive muscle relaxation by tensing and releasing muscle groups",
                "use guided imagery to mentally transport yourself to a peaceful place",
                "take short breaks throughout the day to reset your mind",
                "keep a journal to express thoughts and identify stress triggers"
            ],
            'lifestyle': [
                "limit caffeine and alcohol which can exacerbate anxiety",
                "ensure you're getting adequate sleep to improve stress resilience",
                "practice saying no to additional responsibilities when feeling overwhelmed",
                "spend time in nature, which has been shown to reduce stress levels",
                "consider limiting news and social media consumption if it increases anxiety"
            ]
        }
    
    def get_advice(self, intent_type, entities):
        """Get relevant advice based on intent and entities.
        
        Args:
            intent_type (str): The type of intent (nutrition, fitness, etc.)
            entities (dict): Extracted entities from user input
            
        Returns:
            str: Relevant advice based on the intent and entities
        """
        # Select the appropriate advice category based on intent
        if intent_type == 'nutrition':
            advice_category = self.nutrition_advice
        elif intent_type == 'fitness':
            advice_category = self.fitness_advice
        elif intent_type == 'sleep':
            advice_category = self.sleep_advice
        elif intent_type == 'stress':
            advice_category = self.stress_advice
        else:
            # For general or unknown intents, provide general wellness advice
            general_advice = [
                *self.nutrition_advice['general'],
                *self.fitness_advice['general'],
                *self.sleep_advice['general'],
                *self.stress_advice['general']
            ]
            return random.choice(general_advice)
        
        # Try to match specific subcategories based on entities
        subcategory = 'general'  # Default to general advice
        
        # Check for food items that might indicate specific nutrition needs
        if intent_type == 'nutrition' and entities['food_items']:
            if 'protein' in entities['food_items']:
                subcategory = 'protein'
            elif 'meat' in entities['food_items'] or any(item in ['beef', 'chicken', 'pork', 'fish'] for item in entities['food_items']):
                subcategory = 'meat'
        
        # Check for activities that might indicate specific fitness needs
        if intent_type == 'fitness' and entities['activities']:
            if any(item in ['run', 'jog', 'swim', 'bike'] for item in entities['activities']):
                subcategory = 'cardio'
            elif any(item in ['lift', 'muscle', 'strength'] for item in entities['activities']):
                subcategory = 'strength'
        
        # Check for time periods that might indicate quick workout needs
        if intent_type == 'fitness' and entities['time_periods']:
            if any(item in ['lunch', 'break', 'quick', 'short'] for item in entities['time_periods']):
                subcategory = 'quick_workouts'
        
        # Check for health conditions that might indicate specific needs
        if intent_type == 'sleep' and entities['health_conditions']:
            if 'insomnia' in entities['health_conditions']:
                subcategory = 'insomnia'
        
        # Check for specific stress management needs
        if intent_type == 'stress' and entities['health_conditions']:
            if any(item in ['anxiety', 'overwhelm', 'tension'] for item in entities['health_conditions']):
                subcategory = 'techniques'
        
        # Get advice from the appropriate subcategory if it exists, otherwise use general
        if subcategory in advice_category:
            return random.choice(advice_category[subcategory])
        else:
            return random.choice(advice_category['general'])