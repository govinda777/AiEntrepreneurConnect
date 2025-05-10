import os
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context arguments"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the application"""
    port = os.getenv("STREAMLIT_PORT", "8501")
    return f"http://localhost:{port}"

@pytest.fixture(autouse=True)
def setup_page(page, base_url):
    """Setup page with base URL and common configurations"""
    page.set_default_timeout(30000)  # 30 seconds timeout
    page.set_default_navigation_timeout(30000)
    return page 