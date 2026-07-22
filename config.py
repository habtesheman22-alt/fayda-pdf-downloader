#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot configuration"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # PDF URLs
    PDF_URLS = {
        'form': os.getenv('FAYDA_FORM_URL', 'https://example.com/fayda-form.pdf'),
        'instructions': os.getenv('INSTRUCTIONS_URL', 'https://example.com/instructions.pdf'),
        'requirements': os.getenv('REQUIREMENTS_URL', 'https://example.com/requirements.pdf'),
        'fees': os.getenv('FEE_INFO_URL', 'https://example.com/fee-info.pdf')
    }
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def validate():
        """Validate configuration"""
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN not set in environment")
