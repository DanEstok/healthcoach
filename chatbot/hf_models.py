#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hugging Face Models Module

This module integrates Hugging Face transformer models into the Health Coach chatbot
to enhance natural language understanding and response generation capabilities.
"""

import os
import torch
from typing import Dict, List, Tuple, Union, Optional
from transformers import (
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline
)
from sentence_transformers import SentenceTransformer

class HFModels:
    """Manages Hugging Face models for the Health Coach chatbot."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the Hugging Face models.
        
        Args:
            cache_dir (str, optional): Directory to cache downloaded models
        """
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Model names
        self.qa_model_name = "deepset/roberta-base-squad2"
        self.intent_model_name = "facebook/bart-large-mnli"
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        
        # Initialize models as None (lazy loading)
        self.qa_pipeline = None
        self.intent_classifier = None
        self.sentence_transformer = None
        
        # Device configuration
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
    
    def load_qa_model(self):
        """Load the question-answering model."""
        if self.qa_pipeline is None:
            print(f"Loading QA model: {self.qa_model_name}")
            self.qa_pipeline = pipeline(
                "question-answering",
                model=self.qa_model_name,
                tokenizer=self.qa_model_name,
                device=0 if self.device == "cuda" else -1
            )
    
    def load_intent_model(self):
        """Load the intent classification model."""
        if self.intent_classifier is None:
            print(f"Loading intent classification model: {self.intent_model_name}")
            self.intent_classifier = pipeline(
                "zero-shot-classification",
                model=self.intent_model_name,
                tokenizer=self.intent_model_name,
                device=0 if self.device == "cuda" else -1
            )
    
    def load_embedding_model(self):
        """Load the sentence embedding model."""
        if self.sentence_transformer is None:
            print(f"Loading sentence embedding model: {self.embedding_model_name}")
            self.sentence_transformer = SentenceTransformer(self.embedding_model_name, cache_folder=self.cache_dir)
            if self.device == "cuda":
                self.sentence_transformer = self.sentence_transformer.to(torch.device("cuda"))
    
    def answer_question(self, question: str, context: str) -> Dict:
        """Answer a question based on the provided context.
        
        Args:
            question (str): The question to answer
            context (str): The context to extract the answer from
            
        Returns:
            dict: Answer with score and span information
        """
        self.load_qa_model()
        return self.qa_pipeline(question=question, context=context)
    
    def classify_intent(self, text: str, candidate_labels: List[str]) -> Dict:
        """Classify the intent of the input text.
        
        Args:
            text (str): The input text to classify
            candidate_labels (list): List of possible intent labels
            
        Returns:
            dict: Classification results with labels and scores
        """
        self.load_intent_model()
        return self.intent_classifier(text, candidate_labels)
    
    def get_embeddings(self, texts: Union[str, List[str]]) -> torch.Tensor:
        """Generate embeddings for the input text(s).
        
        Args:
            texts (str or list): Input text or list of texts
            
        Returns:
            torch.Tensor: Embeddings for the input text(s)
        """
        self.load_embedding_model()
        return self.sentence_transformer.encode(texts, convert_to_tensor=True)
    
    def find_best_matches(self, query: str, candidates: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
        """Find the best matching candidates for a query using semantic similarity.
        
        Args:
            query (str): The query text
            candidates (list): List of candidate texts to match against
            top_k (int): Number of top matches to return
            
        Returns:
            list: List of (candidate, score) tuples for the top matches
        """
        self.load_embedding_model()
        
        # Generate embeddings
        query_embedding = self.sentence_transformer.encode(query, convert_to_tensor=True)
        candidate_embeddings = self.sentence_transformer.encode(candidates, convert_to_tensor=True)
        
        # Calculate cosine similarities
        cos_scores = torch.nn.functional.cosine_similarity(query_embedding.unsqueeze(0), candidate_embeddings)
        
        # Get top-k matches
        top_results = []
        top_indices = torch.argsort(cos_scores, descending=True)[:top_k]
        for idx in top_indices:
            top_results.append((candidates[idx], cos_scores[idx].item()))
        
        return top_results