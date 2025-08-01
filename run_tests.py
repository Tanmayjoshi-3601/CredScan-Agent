#!/usr/bin/env python3
"""
Simple test runner that suppresses Streamlit warnings for cleaner output.
"""

import sys
import warnings
import logging

# Suppress Streamlit warnings when running tests
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")
logging.getLogger("streamlit").setLevel(logging.ERROR)

# Import and run the test suite
from test_agent_system import main

if __name__ == "__main__":
    main()