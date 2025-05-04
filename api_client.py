import streamlit as st
import requests
import json
import os
from datetime import datetime
import openai_client

class AIClient:
    """Client for AI services"""
    
    def __init__(self):
        # In a real application, get this from environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def analyze_business(self, data):
        """
        Analyze business data using AI
        
        This uses OpenAI's GPT models to generate insights and recommendations
        """
        with st.spinner("Analisando dados do negócio..."):
            return openai_client.analyze_business(data)
    
    def generate_blue_ocean_strategy(self, data):
        """
        Generate a Blue Ocean strategy using AI
        
        This uses OpenAI's GPT models to create a Blue Ocean strategy
        """
        with st.spinner("Gerando estratégia Blue Ocean..."):
            return openai_client.generate_blue_ocean_strategy(data)
    
    def analyze_seo(self, data):
        """
        Analyze SEO data using AI
        
        This uses OpenAI's GPT models to analyze SEO data and make recommendations
        """
        with st.spinner("Analisando dados de SEO..."):
            return openai_client.analyze_seo(data)
