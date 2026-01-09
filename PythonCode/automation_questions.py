# automation_questions.py
"""
Practice questions for Selenium WebDriver, Robot Framework, and Test Automation.
Questions are structured similarly to the main Python questions for consistency.
"""

# =============================================================================
# SELENIUM QUESTIONS
# =============================================================================

SELENIUM_QUESTIONS = {
    "Basic": [
        {
            "question": "Write a function to open a browser and navigate to a URL",
            "function": "open_browser",
            "test_cases": [
                (("https://example.com",), True),
                (("https://google.com",), True),
            ],
            "hints": [
                "Use webdriver.Chrome() to create a driver instance",
                "Use driver.get(url) to navigate",
                "Return the driver object"
            ],
            "solution": '''from selenium import webdriver

def open_browser(url):
    """Opens Chrome browser and navigates to URL."""
    driver = webdriver.Chrome()
    driver.get(url)
    return driver''',
            "tags": ["Selenium", "WebDriver", "Basics"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to find an element by ID and return its text",
            "function": "get_element_text_by_id",
            "test_cases": [
                (("driver", "header"), "Welcome"),
                (("driver", "message"), "Hello World"),
            ],
            "hints": [
                "Use driver.find_element(By.ID, element_id)",
                "Use .text property to get the text content",
                "Import By from selenium.webdriver.common.by"
            ],
            "solution": '''from selenium.webdriver.common.by import By

def get_element_text_by_id(driver, element_id):
    """Finds element by ID and returns its text."""
    element = driver.find_element(By.ID, element_id)
    return element.text''',
            "tags": ["Selenium", "Locators", "Elements"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to input text into a field and click a button",
            "function": "fill_and_submit",
            "test_cases": [
                (("driver", "username", "testuser", "submit"), True),
            ],
            "hints": [
                "Find the input field using find_element",
                "Use send_keys() to enter text",
                "Use click() on the button element"
            ],
            "solution": '''from selenium.webdriver.common.by import By

def fill_and_submit(driver, input_id, text, button_id):
    """Fills input field and clicks submit button."""
    input_field = driver.find_element(By.ID, input_id)
    input_field.clear()
    input_field.send_keys(text)
    
    button = driver.find_element(By.ID, button_id)
    button.click()
    return True''',
            "tags": ["Selenium", "Elements", "Forms"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to get the current page title",
            "function": "get_page_title",
            "test_cases": [
                (("driver",), "Example Domain"),
            ],
            "hints": [
                "Use driver.title property",
                "No need to find any element"
            ],
            "solution": '''def get_page_title(driver):
    """Returns the current page title."""
    return driver.title''',
            "tags": ["Selenium", "WebDriver", "Basics"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to check if an element is displayed",
            "function": "is_element_visible",
            "test_cases": [
                (("driver", "header"), True),
                (("driver", "hidden-element"), False),
            ],
            "hints": [
                "Find the element first",
                "Use is_displayed() method",
                "Handle NoSuchElementException"
            ],
            "solution": '''from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def is_element_visible(driver, element_id):
    """Checks if element is visible on page."""
    try:
        element = driver.find_element(By.ID, element_id)
        return element.is_displayed()
    except NoSuchElementException:
        return False''',
            "tags": ["Selenium", "Elements", "Assertions"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to get all links on a page",
            "function": "get_all_links",
            "test_cases": [
                (("driver",), ["https://example.com", "https://google.com"]),
            ],
            "hints": [
                "Find all <a> elements using TAG_NAME",
                "Use find_elements (plural)",
                "Get href attribute from each element"
            ],
            "solution": '''from selenium.webdriver.common.by import By

def get_all_links(driver):
    """Returns list of all href values on page."""
    links = driver.find_elements(By.TAG_NAME, "a")
    return [link.get_attribute("href") for link in links if link.get_attribute("href")]''',
            "tags": ["Selenium", "Locators", "Collections"],
            "time_complexity": "O(n)",
            "space_complexity": "O(n)"
        },
        {
            "question": "Write a function to take a screenshot",
            "function": "take_screenshot",
            "test_cases": [
                (("driver", "screenshot.png"), True),
            ],
            "hints": [
                "Use driver.save_screenshot(filename)",
                "Return True if successful"
            ],
            "solution": '''def take_screenshot(driver, filename):
    """Takes screenshot and saves to file."""
    return driver.save_screenshot(filename)''',
            "tags": ["Selenium", "Screenshots", "Basics"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to clear and type text in an input field",
            "function": "clear_and_type",
            "test_cases": [
                (("driver", "search", "hello"), True),
            ],
            "hints": [
                "Find the element by ID",
                "Use clear() before send_keys()",
                "Return True when done"
            ],
            "solution": '''from selenium.webdriver.common.by import By

def clear_and_type(driver, element_id, text):
    """Clears input field and types new text."""
    element = driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text)
    return True''',
            "tags": ["Selenium", "Elements", "Forms"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
    ],
    
    "Intermediate": [
        {
            "question": "Write a function to wait for an element to be clickable",
            "function": "wait_for_clickable",
            "test_cases": [
                (("driver", "submit-btn", 10), "element"),
            ],
            "hints": [
                "Use WebDriverWait",
                "Use expected_conditions.element_to_be_clickable",
                "Return the element when ready"
            ],
            "solution": '''from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_clickable(driver, element_id, timeout=10):
    """Waits for element to be clickable and returns it."""
    wait = WebDriverWait(driver, timeout)
    element = wait.until(
        EC.element_to_be_clickable((By.ID, element_id))
    )
    return element''',
            "tags": ["Selenium", "Waits", "Expected Conditions"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to select an option from a dropdown by visible text",
            "function": "select_dropdown_option",
            "test_cases": [
                (("driver", "country", "United States"), True),
            ],
            "hints": [
                "Use Select class from selenium.webdriver.support.ui",
                "Use select_by_visible_text() method"
            ],
            "solution": '''from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def select_dropdown_option(driver, dropdown_id, option_text):
    """Selects option from dropdown by visible text."""
    dropdown = driver.find_element(By.ID, dropdown_id)
    select = Select(dropdown)
    select.select_by_visible_text(option_text)
    return True''',
            "tags": ["Selenium", "Dropdowns", "Forms"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to handle a JavaScript alert",
            "function": "handle_alert",
            "test_cases": [
                (("driver", True), "Alert text"),
                (("driver", False), "Alert text"),
            ],
            "hints": [
                "Use driver.switch_to.alert",
                "Use accept() to confirm, dismiss() to cancel",
                "Get alert text before accepting/dismissing"
            ],
            "solution": '''def handle_alert(driver, accept=True):
    """Handles JavaScript alert and returns its text."""
    alert = driver.switch_to.alert
    alert_text = alert.text
    
    if accept:
        alert.accept()
    else:
        alert.dismiss()
    
    return alert_text''',
            "tags": ["Selenium", "Alerts", "Window Handling"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to switch to an iframe by name and find an element",
            "function": "find_element_in_iframe",
            "test_cases": [
                (("driver", "content-frame", "element-id"), "element"),
            ],
            "hints": [
                "Use driver.switch_to.frame()",
                "Find the element inside the frame",
                "Don't forget to switch back with default_content()"
            ],
            "solution": '''from selenium.webdriver.common.by import By

def find_element_in_iframe(driver, iframe_name, element_id):
    """Switches to iframe and finds element."""
    driver.switch_to.frame(iframe_name)
    element = driver.find_element(By.ID, element_id)
    driver.switch_to.default_content()
    return element''',
            "tags": ["Selenium", "Frames", "iFrames"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to perform hover action on an element",
            "function": "hover_element",
            "test_cases": [
                (("driver", "menu-item"), True),
            ],
            "hints": [
                "Use ActionChains class",
                "Use move_to_element() method",
                "Don't forget to call perform()"
            ],
            "solution": '''from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def hover_element(driver, element_id):
    """Hovers mouse over element."""
    element = driver.find_element(By.ID, element_id)
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    return True''',
            "tags": ["Selenium", "Actions", "Mouse"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to scroll to an element using JavaScript",
            "function": "scroll_to_element",
            "test_cases": [
                (("driver", "footer"), True),
            ],
            "hints": [
                "Use execute_script()",
                "Use scrollIntoView() JavaScript method",
                "Pass element as argument to script"
            ],
            "solution": '''from selenium.webdriver.common.by import By

def scroll_to_element(driver, element_id):
    """Scrolls page to bring element into view."""
    element = driver.find_element(By.ID, element_id)
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    return True''',
            "tags": ["Selenium", "JavaScript", "Scrolling"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to switch between browser windows",
            "function": "switch_to_new_window",
            "test_cases": [
                (("driver",), True),
            ],
            "hints": [
                "Store original window handle",
                "Get all window handles",
                "Switch to the new window"
            ],
            "solution": '''def switch_to_new_window(driver):
    """Switches to newly opened window."""
    original_window = driver.current_window_handle
    all_windows = driver.window_handles
    
    for window in all_windows:
        if window != original_window:
            driver.switch_to.window(window)
            return True
    
    return False''',
            "tags": ["Selenium", "Windows", "Tabs"],
            "time_complexity": "O(n)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to wait until page contains specific text",
            "function": "wait_for_text",
            "test_cases": [
                (("driver", "Success", 10), True),
            ],
            "hints": [
                "Use WebDriverWait",
                "Use text_to_be_present_in_element or custom condition",
                "Search in body tag for general text"
            ],
            "solution": '''from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_text(driver, text, timeout=10):
    """Waits for text to appear on page."""
    wait = WebDriverWait(driver, timeout)
    wait.until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), text)
    )
    return True''',
            "tags": ["Selenium", "Waits", "Assertions"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to get and set cookies",
            "function": "manage_cookies",
            "test_cases": [
                (("driver", "session", "abc123", True), {"name": "session", "value": "abc123"}),
                (("driver", "session", None, False), None),
            ],
            "hints": [
                "Use driver.add_cookie() to add",
                "Use driver.get_cookie() to retrieve",
                "Cookie must be a dictionary with name and value"
            ],
            "solution": '''def manage_cookies(driver, name, value=None, add=True):
    """Adds or gets a cookie."""
    if add and value:
        driver.add_cookie({"name": name, "value": value})
        return driver.get_cookie(name)
    else:
        return driver.get_cookie(name)''',
            "tags": ["Selenium", "Cookies", "Session"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to perform drag and drop",
            "function": "drag_and_drop",
            "test_cases": [
                (("driver", "source", "target"), True),
            ],
            "hints": [
                "Use ActionChains class",
                "Use drag_and_drop(source, target) method",
                "Don't forget to call perform()"
            ],
            "solution": '''from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def drag_and_drop(driver, source_id, target_id):
    """Performs drag and drop from source to target."""
    source = driver.find_element(By.ID, source_id)
    target = driver.find_element(By.ID, target_id)
    
    actions = ActionChains(driver)
    actions.drag_and_drop(source, target).perform()
    return True''',
            "tags": ["Selenium", "Actions", "Drag and Drop"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
    ],
    
    "Advanced": [
        {
            "question": "Write a BasePage class for Page Object Model",
            "function": "BasePage",
            "test_cases": [],
            "hints": [
                "Include WebDriverWait in __init__",
                "Add common methods: find_element, click, type_text",
                "Handle exceptions gracefully"
            ],
            "solution": '''from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def find_element(self, locator):
        """Finds element with explicit wait."""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def click(self, locator):
        """Clicks on element after waiting for it to be clickable."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def type_text(self, locator, text):
        """Types text into element after clearing it."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Returns text content of element."""
        return self.find_element(locator).text
    
    def is_visible(self, locator, timeout=5):
        """Checks if element is visible."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False''',
            "tags": ["Selenium", "Page Object Model", "Design Pattern"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to create a Remote WebDriver for Selenium Grid",
            "function": "create_remote_driver",
            "test_cases": [],
            "hints": [
                "Use webdriver.Remote",
                "Pass command_executor URL",
                "Set browser options"
            ],
            "solution": '''from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def create_remote_driver(hub_url, browser="chrome", headless=False):
    """Creates Remote WebDriver for Selenium Grid."""
    if browser.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
    elif browser.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
    else:
        raise ValueError(f"Unsupported browser: {browser}")
    
    driver = webdriver.Remote(
        command_executor=hub_url,
        options=options
    )
    return driver''',
            "tags": ["Selenium", "Grid", "Remote"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a retry decorator for flaky Selenium tests",
            "function": "retry",
            "test_cases": [],
            "hints": [
                "Use functools.wraps for proper decoration",
                "Catch exceptions and retry specified times",
                "Add delay between retries"
            ],
            "solution": '''import functools
import time

def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    """Decorator to retry function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# Usage:
# @retry(max_attempts=3, delay=2)
# def flaky_click(driver, element_id):
#     driver.find_element(By.ID, element_id).click()''',
            "tags": ["Selenium", "Best Practices", "Decorators"],
            "time_complexity": "O(n)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a function to execute custom expected condition",
            "function": "wait_for_condition",
            "test_cases": [],
            "hints": [
                "Create a callable that takes driver as argument",
                "Return element when condition is met",
                "Return False otherwise"
            ],
            "solution": '''from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def wait_for_condition(driver, condition_func, timeout=10):
    """Waits for custom condition to be true."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(condition_func)

def element_has_class(locator, class_name):
    """Custom condition: element has specific class."""
    def _predicate(driver):
        try:
            element = driver.find_element(*locator)
            if class_name in element.get_attribute("class"):
                return element
            return False
        except:
            return False
    return _predicate

# Usage:
# element = wait_for_condition(
#     driver, 
#     element_has_class((By.ID, "btn"), "active")
# )''',
            "tags": ["Selenium", "Waits", "Custom Conditions"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a context manager for browser sessions",
            "function": "BrowserSession",
            "test_cases": [],
            "hints": [
                "Implement __enter__ and __exit__ methods",
                "Initialize driver in __enter__",
                "Quit driver in __exit__"
            ],
            "solution": '''from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BrowserSession:
    """Context manager for browser sessions."""
    
    def __init__(self, browser="chrome", headless=False):
        self.browser = browser
        self.headless = headless
        self.driver = None
    
    def __enter__(self):
        if self.browser == "chrome":
            options = Options()
            if self.headless:
                options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)
        elif self.browser == "firefox":
            self.driver = webdriver.Firefox()
        
        self.driver.maximize_window()
        return self.driver
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
        return False  # Don't suppress exceptions

# Usage:
# with BrowserSession(headless=True) as driver:
#     driver.get("https://example.com")''',
            "tags": ["Selenium", "Context Manager", "Best Practices"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
    ]
}


# =============================================================================
# ROBOT FRAMEWORK QUESTIONS
# =============================================================================

ROBOT_FRAMEWORK_QUESTIONS = {
    "Basic": [
        {
            "question": "Write a Robot Framework test to open browser and verify title",
            "function": "verify_page_title",
            "test_cases": [],
            "hints": [
                "Use Open Browser keyword",
                "Use Title Should Be for verification",
                "Close Browser at the end"
            ],
            "solution": '''*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Verify Page Title
    Open Browser    https://example.com    chrome
    Title Should Be    Example Domain
    Close Browser''',
            "tags": ["Robot Framework", "SeleniumLibrary", "Basics"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a Robot Framework keyword to login with credentials",
            "function": "login_keyword",
            "test_cases": [],
            "hints": [
                "Use [Arguments] for parameters",
                "Use Input Text for username",
                "Use Input Password for password"
            ],
            "solution": '''*** Keywords ***
Login With Credentials
    [Arguments]    ${username}    ${password}
    Input Text    id=username    ${username}
    Input Password    id=password    ${password}
    Click Button    id=login-btn''',
            "tags": ["Robot Framework", "Keywords", "Forms"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write Robot Framework variables for test configuration",
            "function": "define_variables",
            "test_cases": [],
            "hints": [
                "Use *** Variables *** section",
                "Use ${} for scalar variables",
                "Use @{} for list variables"
            ],
            "solution": '''*** Variables ***
${BROWSER}        chrome
${BASE_URL}       https://example.com
${TIMEOUT}        10s
@{VALID_USERS}    admin    user1    user2
&{CREDENTIALS}    username=admin    password=admin123''',
            "tags": ["Robot Framework", "Variables", "Configuration"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a Robot Framework FOR loop to click multiple elements",
            "function": "click_multiple_elements",
            "test_cases": [],
            "hints": [
                "Use FOR...IN loop syntax",
                "Use @{} for list iteration",
                "End with END keyword"
            ],
            "solution": '''*** Test Cases ***
Click Multiple Items
    @{items}=    Create List    item1    item2    item3
    FOR    ${item}    IN    @{items}
        Click Element    id=${item}
        Log    Clicked ${item}
    END''',
            "tags": ["Robot Framework", "Control Flow", "Loops"],
            "time_complexity": "O(n)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write Robot Framework test with setup and teardown",
            "function": "test_with_setup_teardown",
            "test_cases": [],
            "hints": [
                "Use [Setup] and [Teardown] in test case",
                "Or use Test Setup/Teardown in Settings",
                "Common for browser open/close"
            ],
            "solution": '''*** Settings ***
Library    SeleniumLibrary
Test Setup    Open Browser    ${URL}    ${BROWSER}
Test Teardown    Close Browser

*** Variables ***
${URL}        https://example.com
${BROWSER}    chrome

*** Test Cases ***
Test With Setup Teardown
    [Documentation]    Test using suite setup/teardown
    Page Should Contain    Example
    
Test With Local Setup
    [Setup]    Log    Custom setup for this test
    [Teardown]    Log    Custom teardown for this test
    Log    Test body''',
            "tags": ["Robot Framework", "Setup", "Teardown"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
    ],
    
    "Intermediate": [
        {
            "question": "Write Robot Framework IF/ELSE condition",
            "function": "conditional_logic",
            "test_cases": [],
            "hints": [
                "Use IF...ELSE IF...ELSE...END syntax",
                "Conditions use Python expressions",
                "String comparison uses quotes"
            ],
            "solution": '''*** Test Cases ***
Conditional Login Response
    ${status}=    Get Element Attribute    id=status    innerText
    
    IF    "${status}" == "success"
        Log    Login successful
        Click Element    id=dashboard
    ELSE IF    "${status}" == "error"
        Log    Login failed
        Capture Page Screenshot
    ELSE
        Log    Unknown status: ${status}
        Fail    Unexpected login status
    END''',
            "tags": ["Robot Framework", "Control Flow", "Conditions"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write a Robot Framework keyword with embedded arguments",
            "function": "embedded_arguments",
            "test_cases": [],
            "hints": [
                "Use quotes in keyword name for embedded arguments",
                "Arguments are captured from keyword name",
                "Makes tests more readable"
            ],
            "solution": '''*** Keywords ***
User "${username}" logs in with password "${password}"
    Input Text    id=username    ${username}
    Input Password    id=password    ${password}
    Click Button    Login
    
User should see "${message}" message
    Wait Until Page Contains    ${message}
    
*** Test Cases ***
Login Test With Embedded Arguments
    User "admin" logs in with password "secret123"
    User should see "Welcome" message''',
            "tags": ["Robot Framework", "Keywords", "BDD"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write Robot Framework TRY/EXCEPT error handling",
            "function": "error_handling",
            "test_cases": [],
            "hints": [
                "Use TRY...EXCEPT...FINALLY...END syntax",
                "Can catch specific error types",
                "FINALLY always executes"
            ],
            "solution": '''*** Test Cases ***
Safe Element Click
    TRY
        Wait Until Element Is Visible    id=dynamic-element    timeout=5s
        Click Element    id=dynamic-element
    EXCEPT    Element*not*visible    type=GLOB
        Log    Element was not visible, trying alternative
        Click Element    id=fallback-element
    EXCEPT    AS    ${error}
        Log    Unexpected error: ${error}
        Capture Page Screenshot    error.png
    FINALLY
        Log    Click attempt completed
    END''',
            "tags": ["Robot Framework", "Error Handling", "Exceptions"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write Robot Framework test using resource file",
            "function": "use_resource_file",
            "test_cases": [],
            "hints": [
                "Create separate .robot file for keywords",
                "Import using Resource keyword in Settings",
                "Can also import variable files"
            ],
            "solution": '''# File: resources/common.robot
*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${BROWSER}    chrome
${TIMEOUT}    10s

*** Keywords ***
Open Application
    [Arguments]    ${url}
    Open Browser    ${url}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}

# File: tests/login_test.robot
*** Settings ***
Resource    ../resources/common.robot

*** Test Cases ***
Test Using Resource
    Open Application    https://example.com
    Title Should Be    Example Domain
    [Teardown]    Close Browser''',
            "tags": ["Robot Framework", "Resources", "Organization"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write Robot Framework data-driven test",
            "function": "data_driven_test",
            "test_cases": [],
            "hints": [
                "Use Test Template in Settings",
                "Each test case provides different data",
                "Template keyword handles the logic"
            ],
            "solution": '''*** Settings ***
Library    SeleniumLibrary
Test Template    Login Should Fail With Invalid Credentials

*** Test Cases ***                USERNAME    PASSWORD    ERROR_MSG
Empty Username                    ${EMPTY}    validpass   Username required
Empty Password                    validuser   ${EMPTY}    Password required
Invalid Credentials               invalid     invalid     Invalid credentials
Special Characters                user@#$     pass@#$     Invalid credentials

*** Keywords ***
Login Should Fail With Invalid Credentials
    [Arguments]    ${username}    ${password}    ${expected_error}
    Open Browser    https://example.com/login    chrome
    Input Text    id=username    ${username}
    Input Password    id=password    ${password}
    Click Button    Login
    Page Should Contain    ${expected_error}
    [Teardown]    Close Browser''',
            "tags": ["Robot Framework", "Data-Driven", "Testing"],
            "time_complexity": "O(n)",
            "space_complexity": "O(1)"
        },
    ],
    
    "Advanced": [
        {
            "question": "Write a custom Robot Framework library in Python",
            "function": "CustomLibrary",
            "test_cases": [],
            "hints": [
                "Create Python class with methods as keywords",
                "Use docstrings for documentation",
                "Set ROBOT_LIBRARY_SCOPE for scope"
            ],
            "solution": '''# custom_library.py
class CustomLibrary:
    """Custom keywords for Robot Framework."""
    
    ROBOT_LIBRARY_SCOPE = 'SUITE'
    
    def __init__(self, base_url=None):
        self.base_url = base_url
    
    def generate_random_email(self, domain="example.com"):
        """Generates random email address.
        
        Example:
        | ${email}= | Generate Random Email | gmail.com |
        """
        import random
        import string
        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{name}@{domain}"
    
    def verify_json_response(self, response, expected_key, expected_value):
        """Verifies JSON response contains expected key-value pair."""
        import json
        data = json.loads(response)
        if data.get(expected_key) != expected_value:
            raise AssertionError(
                f"Expected {expected_key}={expected_value}, "
                f"got {data.get(expected_key)}"
            )
        return True

# In Robot Framework:
# *** Settings ***
# Library    custom_library.py    base_url=https://api.example.com''',
            "tags": ["Robot Framework", "Custom Library", "Python"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write Robot Framework listener for custom reporting",
            "function": "CustomListener",
            "test_cases": [],
            "hints": [
                "Implement ROBOT_LISTENER_API_VERSION = 3",
                "Use start_test, end_test methods",
                "Can send notifications or generate reports"
            ],
            "solution": '''# custom_listener.py
import json
from datetime import datetime

class CustomListener:
    """Listener for custom test reporting."""
    
    ROBOT_LISTENER_API_VERSION = 3
    
    def __init__(self, output_file='results.json'):
        self.output_file = output_file
        self.results = {
            'start_time': None,
            'end_time': None,
            'tests': []
        }
    
    def start_suite(self, data, result):
        self.results['start_time'] = datetime.now().isoformat()
        self.results['suite_name'] = data.name
    
    def end_test(self, data, result):
        self.results['tests'].append({
            'name': data.name,
            'status': result.status,
            'message': result.message,
            'duration': result.elapsed_time.total_seconds()
        })
    
    def end_suite(self, data, result):
        self.results['end_time'] = datetime.now().isoformat()
        self.results['total_passed'] = result.statistics.passed
        self.results['total_failed'] = result.statistics.failed
    
    def close(self):
        with open(self.output_file, 'w') as f:
            json.dump(self.results, f, indent=2)

# Usage: robot --listener custom_listener.py tests/''',
            "tags": ["Robot Framework", "Listeners", "Reporting"],
            "time_complexity": "O(n)",
            "space_complexity": "O(n)"
        },
    ]
}


# =============================================================================
# PYTEST QUESTIONS
# =============================================================================

PYTEST_QUESTIONS = {
    "Basic": [
        {
            "question": "Write a pytest fixture for WebDriver setup and teardown",
            "function": "driver_fixture",
            "test_cases": [],
            "hints": [
                "Use @pytest.fixture decorator",
                "yield for setup/teardown pattern",
                "driver.quit() in teardown"
            ],
            "solution": '''import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    """Fixture to initialize and cleanup WebDriver."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    yield driver  # Test runs here
    
    driver.quit()

def test_page_title(driver):
    driver.get("https://example.com")
    assert "Example" in driver.title''',
            "tags": ["pytest", "Fixtures", "Selenium"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
        {
            "question": "Write parameterized pytest test for multiple inputs",
            "function": "parameterized_test",
            "test_cases": [],
            "hints": [
                "Use @pytest.mark.parametrize decorator",
                "First arg is parameter names as string",
                "Second arg is list of tuples with values"
            ],
            "solution": '''import pytest

@pytest.mark.parametrize("input_value,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("PyTest", "PYTEST"),
])
def test_uppercase(input_value, expected):
    assert input_value.upper() == expected

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_addition(a, b, expected):
    assert a + b == expected''',
            "tags": ["pytest", "Parameterization", "Testing"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
    ],
    
    "Intermediate": [
        {
            "question": "Write pytest conftest.py with shared fixtures",
            "function": "conftest_example",
            "test_cases": [],
            "hints": [
                "conftest.py is auto-discovered by pytest",
                "Use scope parameter for fixture lifetime",
                "Can add command line options"
            ],
            "solution": '''# conftest.py
import pytest
from selenium import webdriver

def pytest_addoption(parser):
    """Add command line options."""
    parser.addoption("--browser", default="chrome", help="Browser to use")
    parser.addoption("--headless", action="store_true", help="Run headless")

@pytest.fixture(scope="session")
def base_url():
    """Base URL for all tests."""
    return "https://example.com"

@pytest.fixture(scope="function")
def driver(request):
    """WebDriver fixture with CLI options."""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        driver = webdriver.Firefox()
    
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_user(driver, base_url):
    """Fixture that provides logged-in session."""
    driver.get(f"{base_url}/login")
    driver.find_element("id", "username").send_keys("user")
    driver.find_element("id", "password").send_keys("pass")
    driver.find_element("id", "login").click()
    return driver''',
            "tags": ["pytest", "Fixtures", "Configuration"],
            "time_complexity": "O(1)",
            "space_complexity": "O(1)"
        },
    ]
}


# =============================================================================
# ALL AUTOMATION QUESTIONS
# =============================================================================

AUTOMATION_QUESTIONS = {
    "Selenium-Basic": SELENIUM_QUESTIONS["Basic"],
    "Selenium-Intermediate": SELENIUM_QUESTIONS["Intermediate"],
    "Selenium-Advanced": SELENIUM_QUESTIONS["Advanced"],
    "RobotFramework-Basic": ROBOT_FRAMEWORK_QUESTIONS["Basic"],
    "RobotFramework-Intermediate": ROBOT_FRAMEWORK_QUESTIONS["Intermediate"],
    "RobotFramework-Advanced": ROBOT_FRAMEWORK_QUESTIONS["Advanced"],
    "pytest-Basic": PYTEST_QUESTIONS["Basic"],
    "pytest-Intermediate": PYTEST_QUESTIONS["Intermediate"],
}


# Automation question tags
AUTOMATION_QUESTION_TAGS = [
    "Selenium", "WebDriver", "Locators", "XPath", "CSS Selectors",
    "Waits", "Expected Conditions", "Actions", "Alerts", "Frames",
    "Page Object Model", "Grid", "Headless",
    "Robot Framework", "Keywords", "Variables", "SeleniumLibrary",
    "pytest", "Fixtures", "Parameterization", "Markers"
]

