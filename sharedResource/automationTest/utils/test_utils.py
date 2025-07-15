#!/usr/bin/env python3
"""
Test Utilities for Automation Tests
Provides common testing functions and utilities for Selenium-based automation tests.
"""

import os
import sys
import time
import logging
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException


class TestUtils:
    """Utility class for common testing operations."""
    
    @staticmethod
    def setup_chrome_driver(headless: bool = True, window_size: str = "1920,1080") -> webdriver.Chrome:
        """
        Set up Chrome WebDriver with common options.
        
        Args:
            headless: Whether to run in headless mode
            window_size: Browser window size
            
        Returns:
            Configured Chrome WebDriver instance
        """
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=" + window_size)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except WebDriverException as e:
            logging.error(f"Failed to create Chrome WebDriver: {e}")
            raise
    
    @staticmethod
    def wait_for_element(driver: webdriver.Chrome, by: By, value: str, timeout: int = 10) -> Optional[Any]:
        """
        Wait for an element to be present and visible.
        
        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement if found, None otherwise
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logging.warning(f"Element not found: {by}={value}")
            return None
    
    @staticmethod
    def wait_for_element_clickable(driver: webdriver.Chrome, by: By, value: str, timeout: int = 10) -> Optional[Any]:
        """
        Wait for an element to be clickable.
        
        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement if clickable, None otherwise
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logging.warning(f"Element not clickable: {by}={value}")
            return None
    
    @staticmethod
    def wait_for_text_present(driver: webdriver.Chrome, by: By, value: str, text: str, timeout: int = 10) -> bool:
        """
        Wait for specific text to be present in an element.
        
        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            text: Text to wait for
            timeout: Maximum wait time in seconds
            
        Returns:
            True if text is found, False otherwise
        """
        try:
            WebDriverWait(driver, timeout).until(
                EC.text_to_be_present_in_element((by, value), text)
            )
            return True
        except TimeoutException:
            logging.warning(f"Text '{text}' not found in element: {by}={value}")
            return False
    
    @staticmethod
    def safe_click(driver: webdriver.Chrome, by: By, value: str, timeout: int = 10) -> bool:
        """
        Safely click an element with wait and error handling.
        
        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            True if click successful, False otherwise
        """
        element = TestUtils.wait_for_element_clickable(driver, by, value, timeout)
        if element:
            try:
                element.click()
                return True
            except Exception as e:
                logging.error(f"Failed to click element {by}={value}: {e}")
                return False
        return False
    
    @staticmethod
    def safe_input(driver: webdriver.Chrome, by: By, value: str, text: str, timeout: int = 10) -> bool:
        """
        Safely input text into an element with wait and error handling.
        
        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            text: Text to input
            timeout: Maximum wait time in seconds
            
        Returns:
            True if input successful, False otherwise
        """
        element = TestUtils.wait_for_element(driver, by, value, timeout)
        if element:
            try:
                element.clear()
                element.send_keys(text)
                return True
            except Exception as e:
                logging.error(f"Failed to input text into element {by}={value}: {e}")
                return False
        return False
    
    @staticmethod
    def get_element_text(driver: webdriver.Chrome, by: By, value: str, timeout: int = 10) -> Optional[str]:
        """
        Get text from an element with wait.
        
        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            Element text if found, None otherwise
        """
        element = TestUtils.wait_for_element(driver, by, value, timeout)
        if element:
            try:
                return element.text
            except Exception as e:
                logging.error(f"Failed to get text from element {by}={value}: {e}")
                return None
        return None
    
    @staticmethod
    def is_element_present(driver: webdriver.Chrome, by: By, value: str, timeout: int = 5) -> bool:
        """
        Check if an element is present on the page.
        
        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            True if element is present, False otherwise
        """
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def is_element_visible(driver: webdriver.Chrome, by: By, value: str, timeout: int = 5) -> bool:
        """
        Check if an element is visible on the page.
        
        Args:
            driver: WebDriver instance
            by: Locator strategy
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_for_url_change(driver: webdriver.Chrome, current_url: str, timeout: int = 10) -> bool:
        """
        Wait for URL to change from current URL.
        
        Args:
            driver: WebDriver instance
            current_url: Current URL to wait for change from
            timeout: Maximum wait time in seconds
            
        Returns:
            True if URL changed, False otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if driver.current_url != current_url:
                return True
            time.sleep(0.5)
        return False
    
    @staticmethod
    def wait_for_page_load(driver: webdriver.Chrome, timeout: int = 10) -> bool:
        """
        Wait for page to fully load.
        
        Args:
            driver: WebDriver instance
            timeout: Maximum wait time in seconds
            
        Returns:
            True if page loaded, False otherwise
        """
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def take_screenshot(driver: webdriver.Chrome, filename: str) -> bool:
        """
        Take a screenshot and save it.
        
        Args:
            driver: WebDriver instance
            filename: Screenshot filename
            
        Returns:
            True if screenshot saved successfully, False otherwise
        """
        try:
            # Create screenshots directory if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = os.path.join("screenshots", filename)
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot saved: {screenshot_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to take screenshot: {e}")
            return False
    
    @staticmethod
    def setup_logging(log_file: str = "test.log", level: int = logging.INFO) -> None:
        """
        Set up logging configuration.
        
        Args:
            log_file: Log file path
            level: Logging level
        """
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    @staticmethod
    def generate_test_report(test_results: Dict[str, Any], report_file: str) -> bool:
        """
        Generate HTML test report.
        
        Args:
            test_results: Dictionary containing test results
            report_file: Output HTML file path
            
        Returns:
            True if report generated successfully, False otherwise
        """
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Test Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
                    .summary {{ margin: 20px 0; }}
                    .test-case {{ margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
                    .pass {{ background-color: #d4edda; border-color: #c3e6cb; }}
                    .fail {{ background-color: #f8d7da; border-color: #f5c6cb; }}
                    .error {{ background-color: #fff3cd; border-color: #ffeaa7; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Automation Test Report</h1>
                    <p>Generated: {test_results.get('timestamp', 'Unknown')}</p>
                </div>
                
                <div class="summary">
                    <h2>Test Summary</h2>
                    <p>Total Tests: {test_results.get('total', 0)}</p>
                    <p>Passed: {test_results.get('passed', 0)}</p>
                    <p>Failed: {test_results.get('failed', 0)}</p>
                    <p>Errors: {test_results.get('errors', 0)}</p>
                </div>
                
                <div class="test-cases">
                    <h2>Test Cases</h2>
            """
            
            for test_case in test_results.get('test_cases', []):
                status_class = test_case.get('status', 'unknown').lower()
                html_content += f"""
                    <div class="test-case {status_class}">
                        <h3>{test_case.get('name', 'Unknown Test')}</h3>
                        <p><strong>Status:</strong> {test_case.get('status', 'Unknown')}</p>
                        <p><strong>Duration:</strong> {test_case.get('duration', 'Unknown')}s</p>
                        <p><strong>Message:</strong> {test_case.get('message', 'No message')}</p>
                    </div>
                """
            
            html_content += """
                </div>
            </body>
            </html>
            """
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logging.info(f"Test report generated: {report_file}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to generate test report: {e}")
            return False 