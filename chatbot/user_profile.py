#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
User Profile Module

This module manages user profiles and session data for the Health Coach chatbot.
It enables personalization of responses and tracks user progress over time.
"""

from datetime import datetime
from typing import Dict, List, Optional

class UserProfile:
    """Manages individual user profile data and preferences."""
    
    def __init__(self, user_id: str):
        """Initialize a new user profile.
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self.user_id = user_id
        self.created_at = datetime.now()
        self.last_interaction = datetime.now()
        
        # User preferences and settings
        self.preferences = {
            'fitness_level': 'beginner',  # beginner, intermediate, advanced
            'dietary_restrictions': [],    # vegetarian, vegan, gluten-free, etc.
            'health_goals': [],            # weight_loss, muscle_gain, better_sleep, etc.
            'notification_preferences': {'daily_tips': True, 'weekly_summary': True}
        }
        
        # Interaction history
        self.interaction_history = {
            'total_interactions': 0,
            'topic_frequency': {},         # Track most discussed topics
            'last_topics': [],             # Recent conversation topics
            'feedback_history': []         # User feedback on responses
        }
        
        # Progress tracking
        self.progress_metrics = {
            'goals_achieved': [],
            'consistency_score': 0.0,
            'engagement_level': 'new',     # new, regular, active, highly_active
            'streak_days': 0
        }
    
    def update_engagement_metrics(self) -> None:
        """Update user engagement metrics based on interaction patterns."""
        # Update engagement level based on interaction frequency
        interactions_per_week = self.interaction_history['total_interactions'] / max(1, (datetime.now() - self.created_at).days / 7)
        
        if interactions_per_week >= 10:
            self.progress_metrics['engagement_level'] = 'highly_active'
        elif interactions_per_week >= 5:
            self.progress_metrics['engagement_level'] = 'active'
        elif interactions_per_week >= 2:
            self.progress_metrics['engagement_level'] = 'regular'
        else:
            self.progress_metrics['engagement_level'] = 'new'

    def update_consistency_score(self) -> None:
        """Update user consistency score based on regular usage and goal progress."""
        # Calculate base score from streak
        streak_factor = min(1.0, self.progress_metrics['streak_days'] / 30)
        
        # Factor in goal achievement rate
        total_goals = len(self.progress_metrics['goals_achieved']) + len(self.preferences['health_goals'])
        achievement_rate = len(self.progress_metrics['goals_achieved']) / max(1, total_goals)
        
        # Combine factors for final score (0.0 to 1.0)
        self.progress_metrics['consistency_score'] = (streak_factor * 0.6) + (achievement_rate * 0.4)

    def update_streak(self) -> None:
        """Update user's streak based on daily interactions."""
        today = datetime.now().date()
        last_interaction_date = self.last_interaction.date()
        
        if last_interaction_date == today:
            return  # Already interacted today
        elif (today - last_interaction_date).days == 1:
            self.progress_metrics['streak_days'] += 1
        else:
            self.progress_metrics['streak_days'] = 0

    def update_interaction(self, topic: str, feedback: Optional[str] = None) -> None:
        """Update user interaction history and progress metrics.
        
        Args:
            topic (str): The main topic of the interaction
            feedback (str, optional): User feedback on the interaction
        """
        previous_date = self.last_interaction.date()
        self.last_interaction = datetime.now()
        self.interaction_history['total_interactions'] += 1
        
        # Update topic frequency
        self.interaction_history['topic_frequency'][topic] = \
            self.interaction_history['topic_frequency'].get(topic, 0) + 1
        
        # Update recent topics
        self.interaction_history['last_topics'].append(topic)
        if len(self.interaction_history['last_topics']) > 5:
            self.interaction_history['last_topics'].pop(0)
        
        # Store feedback if provided
        if feedback:
            self.interaction_history['feedback_history'].append({
                'timestamp': datetime.now(),
                'topic': topic,
                'feedback': feedback
            })
        
        # Update progress tracking metrics
        if self.last_interaction.date() != previous_date:
            self.update_streak()
        self.update_engagement_metrics()
        self.update_consistency_score()
    
    def update_preferences(self, preferences: Dict) -> None:
        """Update user preferences.
        
        Args:
            preferences (dict): Dictionary of preference updates
        """
        self.preferences.update(preferences)
    
    def add_health_goal(self, goal: str) -> None:
        """Add a new health goal for the user.
        
        Args:
            goal (str): The health goal to add
        """
        if goal not in self.preferences['health_goals']:
            self.preferences['health_goals'].append(goal)
    
    def mark_goal_achieved(self, goal: str) -> None:
        """Mark a health goal as achieved.
        
        Args:
            goal (str): The achieved goal
        """
        if goal in self.preferences['health_goals']:
            self.preferences['health_goals'].remove(goal)
            self.progress_metrics['goals_achieved'].append({
                'goal': goal,
                'achieved_at': datetime.now()
            })
    
    def get_personalization_context(self) -> Dict:
        """Get context for response personalization.
        
        Returns:
            dict: Personalization context based on user profile
        """
        return {
            'fitness_level': self.preferences['fitness_level'],
            'dietary_restrictions': self.preferences['dietary_restrictions'],
            'current_goals': self.preferences['health_goals'],
            'interaction_level': self.progress_metrics['engagement_level'],
            'frequent_topics': sorted(
                self.interaction_history['topic_frequency'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }