#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Health Coach Chatbot - Main Application

This is the main entry point for the Health Coach chatbot application.
It initializes all necessary components and provides a simple interface
for interacting with the chatbot.
"""

import os
import sys
from chatbot.nlp_processor import NLPProcessor
from chatbot.rule_engine import RuleEngine
from chatbot.ml_enhancer import MLEnhancer
from chatbot.knowledge_base import KnowledgeBase
from chatbot.user_profile import UserProfile


class HealthCoachChatbot:
    """Main chatbot class that coordinates all components."""
    
    def __init__(self, user_id="default_user"):
        """Initialize the chatbot components.
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self.knowledge_base = KnowledgeBase()
        self.nlp_processor = NLPProcessor()
        self.rule_engine = RuleEngine(self.knowledge_base)
        self.user_profile = UserProfile(user_id)
        self.ml_enhancer = MLEnhancer(user_profile=self.user_profile)
        print("Health Coach initialized and ready to help!")
        
    def process_input(self, user_input, feedback=None):
        """Process user input and generate a response.
        
        Args:
            user_input (str): The user's query or message
            feedback (str, optional): User feedback on previous response
            
        Returns:
            str: The chatbot's response
        """
        # Process the input text with NLP
        processed_input = self.nlp_processor.process(user_input)
        
        # Get rule-based response
        rule_response = self.rule_engine.get_response(processed_input)
        
        # Update user profile with this interaction
        topic = processed_input['intent']['type']
        self.user_profile.update_interaction(topic, feedback)
        
        # If we have a strong rule match, return it
        if rule_response.get('confidence', 0) > 0.8:
            return rule_response['response']
        
        # Otherwise, enhance with ML recommendations
        ml_response = self.ml_enhancer.enhance_response(
            processed_input, 
            rule_response
        )
        
        return ml_response
    
    def run_interactive(self):
        """Run the chatbot in interactive mode on the command line."""
        print("Welcome to Health Coach! Type 'quit' to exit.")
        print("Ask me anything about wellness, nutrition, or fitness.")
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Health Coach: Take care and stay healthy!")
                break
                
            response = self.process_input(user_input)
            print(f"Health Coach: {response}")


def main():
    """Main function to run the chatbot."""
    chatbot = HealthCoachChatbot()
    chatbot.run_interactive()


if __name__ == "__main__":
    main()