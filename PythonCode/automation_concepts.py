# automation_concepts.py
"""
Comprehensive Selenium WebDriver, Robot Framework, and Test Automation Concepts.
This module contains detailed explanations, code examples, and best practices
for test automation technologies.
"""

# =============================================================================
# SELENIUM WEBDRIVER CONCEPTS
# =============================================================================

SELENIUM_CONCEPTS = {
    # -------------------------------------------------------------------------
    # BASICS & SETUP
    # -------------------------------------------------------------------------
    "selenium": """## 🌐 What is Selenium?

**Selenium** is an open-source automated testing framework for web applications. It provides a way to automate browser actions like clicking, typing, and navigating.

### Key Components:
1. **Selenium WebDriver** - Direct browser automation API
2. **Selenium IDE** - Record/playback browser extension
3. **Selenium Grid** - Distributed test execution

### Installation:
```python
pip install selenium
```

### Browser Drivers:
- **ChromeDriver** for Chrome
- **GeckoDriver** for Firefox
- **EdgeDriver** for Microsoft Edge
- **SafariDriver** for Safari

### First Script:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize browser
driver = webdriver.Chrome()

# Open URL
driver.get("https://www.google.com")

# Find element and interact
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium Python")
search_box.submit()

# Close browser
driver.quit()
```

### Key Benefits:
- Cross-browser testing
- Multiple language support (Python, Java, C#, JavaScript)
- Large community and ecosystem
- Integration with test frameworks""",

    "webdriver": """## 🔧 Selenium WebDriver Architecture

**WebDriver** is the core component of Selenium that provides a programming interface to create and execute test scripts.

### Architecture:
```
Test Script → WebDriver API → Browser Driver → Browser
```

### How it Works:
1. Test script sends commands via WebDriver API
2. Commands are converted to HTTP requests (JSON Wire Protocol)
3. Browser driver receives and executes commands
4. Results are sent back to the script

### WebDriver Instance:
```python
from selenium import webdriver

# Chrome
driver = webdriver.Chrome()

# Firefox
driver = webdriver.Firefox()

# Edge
driver = webdriver.Edge()

# Safari
driver = webdriver.Safari()
```

### Common Methods:
```python
# Navigation
driver.get("https://example.com")    # Open URL
driver.back()                         # Go back
driver.forward()                      # Go forward
driver.refresh()                      # Refresh page

# Browser Info
driver.title                          # Page title
driver.current_url                    # Current URL
driver.page_source                    # Page HTML

# Window Management
driver.maximize_window()              # Maximize
driver.minimize_window()              # Minimize
driver.set_window_size(1920, 1080)   # Set size

# Cleanup
driver.close()                        # Close current tab
driver.quit()                         # Close all and end session
```""",

    "webdriver manager": """## 📦 WebDriver Manager

**WebDriver Manager** automatically downloads and manages browser drivers, eliminating manual driver setup.

### Installation:
```python
pip install webdriver-manager
```

### Usage with Different Browsers:

**Chrome:**
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

**Firefox:**
```python
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
```

**Edge:**
```python
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
```

### Benefits:
- No manual driver downloads
- Automatic version matching
- Cross-platform support
- Caches drivers locally""",

    # -------------------------------------------------------------------------
    # LOCATORS
    # -------------------------------------------------------------------------
    "selenium locators": """## 🎯 Selenium Locators

**Locators** are strategies to find elements on a web page. Selenium supports 8 locator types.

### All Locator Types:
```python
from selenium.webdriver.common.by import By

# 1. ID - Fastest and most reliable
driver.find_element(By.ID, "username")

# 2. NAME - Form elements
driver.find_element(By.NAME, "email")

# 3. CLASS_NAME - Single class
driver.find_element(By.CLASS_NAME, "btn-primary")

# 4. TAG_NAME - HTML tag
driver.find_element(By.TAG_NAME, "input")

# 5. LINK_TEXT - Exact link text
driver.find_element(By.LINK_TEXT, "Click Here")

# 6. PARTIAL_LINK_TEXT - Partial match
driver.find_element(By.PARTIAL_LINK_TEXT, "Click")

# 7. XPATH - Most flexible
driver.find_element(By.XPATH, "//input[@type='email']")

# 8. CSS_SELECTOR - Fast and readable
driver.find_element(By.CSS_SELECTOR, "input.form-control")
```

### Locator Priority (Best to Worst):
1. **ID** - Unique, fastest
2. **Name** - Usually unique for forms
3. **CSS Selector** - Fast, readable
4. **XPath** - Most flexible, slower

### Find Multiple Elements:
```python
# Returns list of elements
elements = driver.find_elements(By.CLASS_NAME, "item")
for element in elements:
    print(element.text)
```""",

    "xpath": """## 🔍 XPath Locators

**XPath** (XML Path Language) is a powerful way to locate elements using path expressions.

### Basic Syntax:
```python
from selenium.webdriver.common.by import By

# Absolute XPath (fragile - avoid)
driver.find_element(By.XPATH, "/html/body/div/form/input")

# Relative XPath (recommended)
driver.find_element(By.XPATH, "//input[@id='username']")
```

### Common XPath Expressions:

**By Attribute:**
```python
# Single attribute
"//input[@type='text']"
"//button[@class='submit']"
"//a[@href='/login']"

# Multiple attributes
"//input[@type='text' and @name='email']"
"//button[@class='btn' or @id='submit']"
```

**By Text:**
```python
# Exact text
"//button[text()='Submit']"

# Contains text
"//button[contains(text(),'Sub')]"

# Starts with
"//input[starts-with(@id,'user')]"
```

**Axes (Navigation):**
```python
# Parent
"//input[@id='email']/parent::div"

# Child
"//form[@id='login']/child::input"

# Following sibling
"//label[@for='email']/following-sibling::input"

# Ancestor
"//input[@id='email']/ancestor::form"

# Descendant
"//div[@class='container']//input"
```

### Best Practices:
- Use relative XPath over absolute
- Combine with unique attributes
- Avoid index-based XPath when possible""",

    "css selectors": """## 🎨 CSS Selectors

**CSS Selectors** provide a fast and readable way to locate elements.

### Basic Selectors:
```python
from selenium.webdriver.common.by import By

# By ID (#)
driver.find_element(By.CSS_SELECTOR, "#username")

# By Class (.)
driver.find_element(By.CSS_SELECTOR, ".btn-primary")

# By Tag
driver.find_element(By.CSS_SELECTOR, "input")

# By Attribute
driver.find_element(By.CSS_SELECTOR, "[name='email']")
driver.find_element(By.CSS_SELECTOR, "input[type='text']")
```

### Advanced Selectors:
```python
# Multiple classes
".btn.btn-primary.active"

# Direct child (>)
"form > input"

# Descendant (space)
"form input"

# Adjacent sibling (+)
"label + input"

# General sibling (~)
"h1 ~ p"

# First child
"li:first-child"

# Last child
"li:last-child"

# Nth child
"li:nth-child(2)"
"li:nth-child(odd)"
"li:nth-child(even)"
```

### Attribute Selectors:
```python
# Contains
"[class*='btn']"

# Starts with
"[id^='user']"

# Ends with
"[id$='name']"

# Exact match
"[type='submit']"
```

### CSS vs XPath:
| CSS Selector | XPath |
|-------------|-------|
| Faster | More flexible |
| More readable | Can traverse up (parent) |
| Can't select by text | Can select by text |""",

    "relative locators": """## 📍 Relative Locators (Selenium 4)

**Relative Locators** find elements based on their position relative to other elements.

### Available Methods:
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

# Above
element = driver.find_element(
    locate_with(By.TAG_NAME, "input").above({By.ID: "password"})
)

# Below
element = driver.find_element(
    locate_with(By.TAG_NAME, "input").below({By.ID: "email"})
)

# To the left of
element = driver.find_element(
    locate_with(By.TAG_NAME, "button").to_left_of({By.ID: "submit"})
)

# To the right of
element = driver.find_element(
    locate_with(By.TAG_NAME, "input").to_right_of({By.ID: "label"})
)

# Near (within 50 pixels by default)
element = driver.find_element(
    locate_with(By.TAG_NAME, "input").near({By.ID: "label"})
)
```

### Chaining Relative Locators:
```python
# Find input that is below email and above submit
element = driver.find_element(
    locate_with(By.TAG_NAME, "input")
    .below({By.ID: "email"})
    .above({By.ID: "submit"})
)
```

### Use Cases:
- Forms with consistent layout
- Tables without unique identifiers
- Dynamic content positioning""",

    # -------------------------------------------------------------------------
    # ELEMENT INTERACTIONS
    # -------------------------------------------------------------------------
    "element interactions": """## 🖱️ Element Interactions

**WebElement** methods allow you to interact with page elements.

### Finding Elements:
```python
from selenium.webdriver.common.by import By

# Single element
element = driver.find_element(By.ID, "username")

# Multiple elements
elements = driver.find_elements(By.CLASS_NAME, "item")
```

### Click Actions:
```python
button = driver.find_element(By.ID, "submit")
button.click()
```

### Typing Text:
```python
input_field = driver.find_element(By.ID, "username")
input_field.send_keys("myusername")

# Clear and type
input_field.clear()
input_field.send_keys("newvalue")
```

### Getting Information:
```python
element = driver.find_element(By.ID, "message")

# Get text content
text = element.text

# Get attribute value
value = element.get_attribute("value")
href = element.get_attribute("href")
class_name = element.get_attribute("class")

# Get CSS property
color = element.value_of_css_property("color")
```

### Element State:
```python
# Check if visible
is_displayed = element.is_displayed()

# Check if enabled
is_enabled = element.is_enabled()

# Check if selected (checkbox/radio)
is_selected = element.is_selected()
```

### Form Submission:
```python
form = driver.find_element(By.TAG_NAME, "form")
form.submit()

# Or submit from any form element
input_field.submit()
```""",

    "dropdowns": """## 📋 Working with Dropdowns

**Select** class provides methods to interact with dropdown elements.

### Using Select Class:
```python
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# Find the dropdown element
dropdown = driver.find_element(By.ID, "country")
select = Select(dropdown)
```

### Selection Methods:
```python
# By visible text
select.select_by_visible_text("United States")

# By value attribute
select.select_by_value("us")

# By index (0-based)
select.select_by_index(2)
```

### Deselection (Multi-select):
```python
# Deselect by text
select.deselect_by_visible_text("Option 1")

# Deselect by value
select.deselect_by_value("opt1")

# Deselect by index
select.deselect_by_index(0)

# Deselect all
select.deselect_all()
```

### Getting Options:
```python
# All options
all_options = select.options
for option in all_options:
    print(option.text)

# Selected option(s)
selected = select.first_selected_option
all_selected = select.all_selected_options

# Check if multi-select
is_multi = select.is_multiple
```

### Non-Standard Dropdowns:
```python
# For custom dropdowns (not <select>)
dropdown_trigger = driver.find_element(By.CLASS_NAME, "dropdown-toggle")
dropdown_trigger.click()

option = driver.find_element(By.XPATH, "//li[text()='Option 1']")
option.click()
```""",

    "checkboxes radio buttons": """## ☑️ Checkboxes and Radio Buttons

### Checkboxes:
```python
from selenium.webdriver.common.by import By

checkbox = driver.find_element(By.ID, "agree")

# Check if selected
if not checkbox.is_selected():
    checkbox.click()

# Uncheck if selected
if checkbox.is_selected():
    checkbox.click()
```

### Radio Buttons:
```python
# Select specific radio button
radio = driver.find_element(By.ID, "gender_male")
radio.click()

# Find all radio buttons in a group
radios = driver.find_elements(By.NAME, "gender")
for radio in radios:
    if radio.get_attribute("value") == "male":
        radio.click()
        break
```

### Multiple Checkboxes:
```python
# Select multiple checkboxes
checkboxes = driver.find_elements(By.NAME, "interests")
for cb in checkboxes:
    if cb.get_attribute("value") in ["sports", "music"]:
        if not cb.is_selected():
            cb.click()
```

### Best Practices:
```python
# Use labels for better reliability
label = driver.find_element(By.XPATH, "//label[@for='agree']")
label.click()

# Verify state after action
checkbox.click()
assert checkbox.is_selected(), "Checkbox was not selected"
```""",

    "file upload": """## 📁 File Upload

### Standard File Input:
```python
from selenium.webdriver.common.by import By
import os

# Find file input element
file_input = driver.find_element(By.ID, "file-upload")

# Send file path directly
file_path = os.path.abspath("test_file.pdf")
file_input.send_keys(file_path)

# Submit the form
driver.find_element(By.ID, "upload-btn").click()
```

### Multiple Files:
```python
file_input = driver.find_element(By.ID, "files")
files = [
    os.path.abspath("file1.pdf"),
    os.path.abspath("file2.pdf")
]
file_input.send_keys("\\n".join(files))
```

### Hidden File Inputs:
```python
# Make hidden input visible with JavaScript
driver.execute_script(
    "arguments[0].style.display = 'block';",
    file_input
)
file_input.send_keys(file_path)
```

### Drag and Drop Upload:
```python
from selenium.webdriver.common.action_chains import ActionChains

# For drag-and-drop zones, use JavaScript
js_script = '''
    var input = document.createElement('input');
    input.type = 'file';
    input.style.display = 'none';
    document.body.appendChild(input);
    return input;
'''
file_input = driver.execute_script(js_script)
file_input.send_keys(file_path)
```""",

    # -------------------------------------------------------------------------
    # WAITS
    # -------------------------------------------------------------------------
    "selenium waits": """## ⏳ Selenium Waits

**Waits** are essential for handling dynamic web pages and timing issues.

### Types of Waits:

**1. Implicit Wait (Global):**
```python
driver.implicitly_wait(10)  # Wait up to 10 seconds
# Applies to all find_element calls
```

**2. Explicit Wait (Targeted):**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.ID, "result"))
)
```

**3. Fluent Wait (Customizable):**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

wait = WebDriverWait(
    driver,
    timeout=30,
    poll_frequency=0.5,
    ignored_exceptions=[NoSuchElementException]
)
element = wait.until(EC.element_to_be_clickable((By.ID, "btn")))
```

### Comparison:
| Wait Type | Scope | Use Case |
|-----------|-------|----------|
| Implicit | Global | Simple apps, consistent load times |
| Explicit | Single element | Dynamic content, specific conditions |
| Fluent | Single element | Custom polling, ignore exceptions |

### Best Practice:
- Use explicit waits for reliability
- Avoid mixing implicit and explicit waits
- Set reasonable timeouts""",

    "expected conditions": """## ✅ Expected Conditions

**Expected Conditions** (EC) provide pre-built conditions for explicit waits.

### Common Conditions:
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait = WebDriverWait(driver, 10)

# Element presence (in DOM)
element = wait.until(
    EC.presence_of_element_located((By.ID, "element"))
)

# Element visible
element = wait.until(
    EC.visibility_of_element_located((By.ID, "element"))
)

# Element clickable
element = wait.until(
    EC.element_to_be_clickable((By.ID, "button"))
)

# Element invisible
wait.until(
    EC.invisibility_of_element_located((By.ID, "loader"))
)

# Text present
wait.until(
    EC.text_to_be_present_in_element((By.ID, "status"), "Complete")
)
```

### More Conditions:
```python
# Title conditions
wait.until(EC.title_is("Expected Title"))
wait.until(EC.title_contains("Partial"))

# URL conditions
wait.until(EC.url_to_be("https://example.com"))
wait.until(EC.url_contains("/dashboard"))

# Alert present
alert = wait.until(EC.alert_is_present())

# Frame available
wait.until(EC.frame_to_be_available_and_switch_to_it("frameName"))

# Element staleness (removed from DOM)
wait.until(EC.staleness_of(old_element))

# Number of windows
wait.until(EC.number_of_windows_to_be(2))

# All elements present
elements = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "item"))
)
```

### Custom Wait Condition:
```python
def element_has_class(locator, class_name):
    def _predicate(driver):
        element = driver.find_element(*locator)
        if class_name in element.get_attribute("class"):
            return element
        return False
    return _predicate

element = wait.until(element_has_class((By.ID, "btn"), "active"))
```""",

    # -------------------------------------------------------------------------
    # ACTIONS CLASS
    # -------------------------------------------------------------------------
    "actions class": """## 🎮 Actions Class

**ActionChains** enables complex user interactions like drag-drop, hover, and keyboard actions.

### Basic Setup:
```python
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

actions = ActionChains(driver)
```

### Mouse Actions:
```python
element = driver.find_element(By.ID, "button")

# Click
actions.click(element).perform()

# Double click
actions.double_click(element).perform()

# Right click (context click)
actions.context_click(element).perform()

# Hover (move to element)
actions.move_to_element(element).perform()

# Click and hold
actions.click_and_hold(element).perform()

# Release
actions.release(element).perform()
```

### Drag and Drop:
```python
source = driver.find_element(By.ID, "draggable")
target = driver.find_element(By.ID, "droppable")

# Method 1: drag_and_drop
actions.drag_and_drop(source, target).perform()

# Method 2: drag_and_drop_by_offset
actions.drag_and_drop_by_offset(source, 100, 50).perform()

# Method 3: Manual steps
actions.click_and_hold(source)\\
       .move_to_element(target)\\
       .release()\\
       .perform()
```

### Move Actions:
```python
# Move by offset
actions.move_by_offset(100, 200).perform()

# Move to element with offset
actions.move_to_element_with_offset(element, 10, 10).perform()
```

### Chaining Actions:
```python
actions.move_to_element(menu)\\
       .pause(1)\\
       .click(submenu)\\
       .perform()
```""",

    "keyboard actions": """## ⌨️ Keyboard Actions

### Using send_keys:
```python
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

element = driver.find_element(By.ID, "input")

# Type text
element.send_keys("Hello World")

# Special keys
element.send_keys(Keys.ENTER)
element.send_keys(Keys.TAB)
element.send_keys(Keys.ESCAPE)

# Key combinations
element.send_keys(Keys.CONTROL, "a")  # Select all
element.send_keys(Keys.CONTROL, "c")  # Copy
element.send_keys(Keys.CONTROL, "v")  # Paste

# Clear and type
element.send_keys(Keys.CONTROL, "a", Keys.DELETE)
element.send_keys("New text")
```

### Using ActionChains:
```python
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

actions = ActionChains(driver)

# Key down/up
actions.key_down(Keys.SHIFT)\\
       .send_keys("hello")\\
       .key_up(Keys.SHIFT)\\
       .perform()  # Types "HELLO"

# Send keys to specific element
actions.send_keys_to_element(element, "text").perform()

# Global keyboard actions (no element focus)
actions.send_keys(Keys.ESCAPE).perform()
```

### Common Key Codes:
```python
Keys.ENTER      # Enter/Return
Keys.TAB        # Tab
Keys.ESCAPE     # Escape
Keys.BACKSPACE  # Backspace
Keys.DELETE     # Delete
Keys.SPACE      # Space
Keys.CONTROL    # Ctrl
Keys.ALT        # Alt
Keys.SHIFT      # Shift
Keys.ARROW_UP   # Up arrow
Keys.ARROW_DOWN # Down arrow
Keys.PAGE_UP    # Page up
Keys.PAGE_DOWN  # Page down
Keys.HOME       # Home
Keys.END        # End
Keys.F1 - F12   # Function keys
```""",

    # -------------------------------------------------------------------------
    # JAVASCRIPT EXECUTOR
    # -------------------------------------------------------------------------
    "javascript executor": """## 📜 JavaScript Executor

**execute_script** allows running JavaScript directly in the browser.

### Basic Usage:
```python
# Execute JavaScript
driver.execute_script("alert('Hello World')")

# Return value
title = driver.execute_script("return document.title")
```

### Scrolling:
```python
# Scroll to bottom
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

# Scroll to top
driver.execute_script("window.scrollTo(0, 0)")

# Scroll by pixels
driver.execute_script("window.scrollBy(0, 500)")

# Scroll element into view
element = driver.find_element(By.ID, "target")
driver.execute_script("arguments[0].scrollIntoView(true);", element)

# Scroll with smooth behavior
driver.execute_script(
    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
    element
)
```

### Element Manipulation:
```python
element = driver.find_element(By.ID, "myElement")

# Click via JavaScript (bypasses overlay issues)
driver.execute_script("arguments[0].click();", element)

# Set value
driver.execute_script("arguments[0].value = 'new value';", element)

# Change style
driver.execute_script("arguments[0].style.border = '2px solid red';", element)

# Remove element
driver.execute_script("arguments[0].remove();", element)

# Highlight element (debugging)
driver.execute_script(
    "arguments[0].style.backgroundColor = 'yellow';",
    element
)
```

### Get Information:
```python
# Get computed style
color = driver.execute_script(
    "return window.getComputedStyle(arguments[0]).color;",
    element
)

# Check if element in viewport
in_viewport = driver.execute_script('''
    var rect = arguments[0].getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= window.innerHeight &&
        rect.right <= window.innerWidth
    );
''', element)

# Get page ready state
ready_state = driver.execute_script("return document.readyState")
```

### Async JavaScript:
```python
# execute_async_script waits for callback
result = driver.execute_async_script('''
    var callback = arguments[arguments.length - 1];
    setTimeout(function() {
        callback('done');
    }, 2000);
''')
```""",

    # -------------------------------------------------------------------------
    # WINDOW & FRAME HANDLING
    # -------------------------------------------------------------------------
    "window handling": """## 🪟 Window and Tab Handling

### Get Window Handles:
```python
# Current window handle
main_window = driver.current_window_handle

# All window handles
all_windows = driver.window_handles
```

### Switch Between Windows:
```python
# Open new tab
driver.execute_script("window.open('https://example.com', '_blank');")

# Get all handles
windows = driver.window_handles

# Switch to new window
for window in windows:
    if window != main_window:
        driver.switch_to.window(window)
        break

# Switch back to main
driver.switch_to.window(main_window)
```

### New Window/Tab (Selenium 4):
```python
# Open new tab
driver.switch_to.new_window('tab')

# Open new window
driver.switch_to.new_window('window')
```

### Close Windows:
```python
# Close current window/tab
driver.close()

# Switch and close
driver.switch_to.window(new_window)
driver.close()
driver.switch_to.window(main_window)

# Quit (close all)
driver.quit()
```

### Window Size and Position:
```python
# Get size
size = driver.get_window_size()
print(f"Width: {size['width']}, Height: {size['height']}")

# Set size
driver.set_window_size(1920, 1080)

# Get position
position = driver.get_window_position()

# Set position
driver.set_window_position(0, 0)

# Maximize/minimize
driver.maximize_window()
driver.minimize_window()
driver.fullscreen_window()
```""",

    "frames iframes": """## 🖼️ Frames and iFrames

### Switching to Frame:
```python
from selenium.webdriver.common.by import By

# By index (0-based)
driver.switch_to.frame(0)

# By name or ID
driver.switch_to.frame("frameName")
driver.switch_to.frame("frameId")

# By WebElement
frame_element = driver.find_element(By.TAG_NAME, "iframe")
driver.switch_to.frame(frame_element)
```

### Switching Back:
```python
# Switch to parent frame
driver.switch_to.parent_frame()

# Switch to main content
driver.switch_to.default_content()
```

### Nested Frames:
```python
# Switch to outer frame
driver.switch_to.frame("outerFrame")

# Switch to nested frame
driver.switch_to.frame("innerFrame")

# Work with elements in inner frame
element = driver.find_element(By.ID, "element_in_inner")

# Go back to outer frame
driver.switch_to.parent_frame()

# Go back to main
driver.switch_to.default_content()
```

### Wait for Frame:
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
wait.until(EC.frame_to_be_available_and_switch_to_it("frameName"))
```

### Common Pattern:
```python
def interact_with_frame(driver, frame_locator, element_locator, action):
    \"\"\"Interact with element inside frame.\"\"\"
    try:
        driver.switch_to.frame(frame_locator)
        element = driver.find_element(*element_locator)
        action(element)
    finally:
        driver.switch_to.default_content()
```""",

    "alerts": """## ⚠️ Handling Alerts

### Types of Alerts:
1. **Simple Alert** - OK button only
2. **Confirm Alert** - OK and Cancel
3. **Prompt Alert** - Text input with OK/Cancel

### Basic Alert Handling:
```python
from selenium.webdriver.common.alert import Alert

# Switch to alert
alert = driver.switch_to.alert

# Get alert text
print(alert.text)

# Accept (OK)
alert.accept()

# Dismiss (Cancel)
alert.dismiss()

# Send text (prompt)
alert.send_keys("My input")
alert.accept()
```

### Wait for Alert:
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
alert = wait.until(EC.alert_is_present())
alert.accept()
```

### Handle Unexpected Alerts:
```python
from selenium.common.exceptions import NoAlertPresentException

def handle_alert_if_present(driver, accept=True):
    try:
        alert = driver.switch_to.alert
        if accept:
            alert.accept()
        else:
            alert.dismiss()
        return True
    except NoAlertPresentException:
        return False
```

### Authentication Alert:
```python
# For HTTP Basic Auth alerts
# Include credentials in URL
driver.get("https://username:password@example.com")

# Or use Selenium 4 DevTools
# (for Chrome-based browsers)
```""",

    # -------------------------------------------------------------------------
    # SCREENSHOTS
    # -------------------------------------------------------------------------
    "screenshots": """## 📸 Taking Screenshots

### Full Page Screenshot:
```python
# Save to file
driver.save_screenshot("screenshot.png")

# Get as base64
screenshot_base64 = driver.get_screenshot_as_base64()

# Get as PNG bytes
screenshot_png = driver.get_screenshot_as_png()
```

### Element Screenshot:
```python
element = driver.find_element(By.ID, "myElement")

# Save element screenshot
element.screenshot("element.png")
```

### Full Page (Selenium 4 - Firefox):
```python
# Firefox supports full page screenshot
driver.save_full_page_screenshot("fullpage.png")
```

### Screenshot with Timestamp:
```python
from datetime import datetime

def take_screenshot(driver, name="screenshot"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename
```

### Screenshot on Failure:
```python
import pytest

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_example(driver):
    try:
        # Test steps
        assert False, "Test failed"
    except AssertionError:
        driver.save_screenshot("failure.png")
        raise
```

### Screenshot Directory:
```python
import os

def save_screenshot(driver, name, directory="screenshots"):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{name}.png")
    driver.save_screenshot(path)
    return path
```""",

    # -------------------------------------------------------------------------
    # COOKIES
    # -------------------------------------------------------------------------
    "cookies": """## 🍪 Cookie Management

### Get Cookies:
```python
# Get all cookies
all_cookies = driver.get_cookies()
for cookie in all_cookies:
    print(f"{cookie['name']}: {cookie['value']}")

# Get specific cookie
cookie = driver.get_cookie("session_id")
print(cookie['value'])
```

### Add Cookie:
```python
# Add simple cookie
driver.add_cookie({
    "name": "test_cookie",
    "value": "test_value"
})

# Add cookie with options
driver.add_cookie({
    "name": "session",
    "value": "abc123",
    "domain": ".example.com",
    "path": "/",
    "secure": True,
    "httpOnly": True,
    "expiry": 1735689600  # Unix timestamp
})
```

### Delete Cookies:
```python
# Delete specific cookie
driver.delete_cookie("test_cookie")

# Delete all cookies
driver.delete_all_cookies()
```

### Save and Load Cookies:
```python
import json

# Save cookies to file
def save_cookies(driver, filepath):
    with open(filepath, 'w') as f:
        json.dump(driver.get_cookies(), f)

# Load cookies from file
def load_cookies(driver, filepath):
    with open(filepath, 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        # Handle expiry format
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        driver.add_cookie(cookie)

# Usage
driver.get("https://example.com")  # Must be on domain first
save_cookies(driver, "cookies.json")

# Later session
driver.get("https://example.com")
load_cookies(driver, "cookies.json")
driver.refresh()  # Apply cookies
```""",

    # -------------------------------------------------------------------------
    # PAGE OBJECT MODEL
    # -------------------------------------------------------------------------
    "page object model": """## 🏗️ Page Object Model (POM)

**Page Object Model** is a design pattern that creates an object repository for web elements.

### Benefits:
- Code reusability
- Better maintainability
- Reduced code duplication
- Cleaner test code

### Basic Structure:
```
project/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/
│   ├── __init__.py
│   └── test_login.py
└── conftest.py
```

### Base Page:
```python
# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def type_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        return self.find_element(locator).text
```

### Page Class:
```python
# pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login")
    ERROR_MSG = (By.CLASS_NAME, "error")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://example.com/login"
    
    def open(self):
        self.driver.get(self.url)
        return self
    
    def login(self, username, password):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
        return DashboardPage(self.driver)
    
    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)
```

### Test Using POM:
```python
# tests/test_login.py
import pytest
from pages.login_page import LoginPage

def test_valid_login(driver):
    login_page = LoginPage(driver)
    dashboard = login_page.open().login("user", "pass")
    assert dashboard.is_loaded()

def test_invalid_login(driver):
    login_page = LoginPage(driver)
    login_page.open().login("invalid", "invalid")
    assert "Invalid credentials" in login_page.get_error_message()
```""",

    # -------------------------------------------------------------------------
    # HEADLESS & CROSS-BROWSER
    # -------------------------------------------------------------------------
    "headless browser": """## 👻 Headless Browser Testing

**Headless mode** runs browsers without a visible UI - faster and ideal for CI/CD.

### Chrome Headless:
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")  # New headless mode
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
```

### Firefox Headless:
```python
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("-headless")

driver = webdriver.Firefox(options=options)
```

### Edge Headless:
```python
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument("--headless=new")

driver = webdriver.Edge(options=options)
```

### Common Options:
```python
options = Options()

# Headless
options.add_argument("--headless=new")

# Window size (important in headless)
options.add_argument("--window-size=1920,1080")

# Disable images (faster)
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

# Disable extensions
options.add_argument("--disable-extensions")

# Incognito
options.add_argument("--incognito")

# Custom user agent
options.add_argument("--user-agent=Mozilla/5.0 ...")
```

### Screenshot in Headless:
```python
# Screenshots work normally in headless
driver.save_screenshot("headless_screenshot.png")
```""",

    "cross browser testing": """## 🌐 Cross-Browser Testing

### Browser Setup Functions:
```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def get_chrome_driver():
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)

def get_firefox_driver():
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service)

def get_edge_driver():
    service = EdgeService(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service)

def get_driver(browser="chrome"):
    browsers = {
        "chrome": get_chrome_driver,
        "firefox": get_firefox_driver,
        "edge": get_edge_driver
    }
    return browsers.get(browser.lower(), get_chrome_driver)()
```

### Pytest Parameterization:
```python
import pytest

@pytest.fixture(params=["chrome", "firefox", "edge"])
def driver(request):
    driver = get_driver(request.param)
    yield driver
    driver.quit()

def test_cross_browser(driver):
    driver.get("https://example.com")
    assert "Example" in driver.title
```

### Configuration File:
```python
# config.py
import os

BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
BASE_URL = os.getenv("BASE_URL", "https://example.com")
```

### Browser Capabilities:
```python
# Chrome capabilities
chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability("browserVersion", "latest")
chrome_options.set_capability("platformName", "Windows 10")
```""",

    # -------------------------------------------------------------------------
    # SELENIUM GRID
    # -------------------------------------------------------------------------
    "selenium grid": """## 🔲 Selenium Grid

**Selenium Grid** enables parallel test execution across multiple machines and browsers.

### Grid Architecture:
```
Hub (central server)
├── Node 1 (Chrome)
├── Node 2 (Firefox)
└── Node 3 (Edge)
```

### Start Grid (Selenium 4):
```bash
# Download selenium-server
# Start in standalone mode
java -jar selenium-server-4.x.jar standalone

# Or start hub and nodes separately
java -jar selenium-server-4.x.jar hub
java -jar selenium-server-4.x.jar node --hub http://localhost:4444
```

### Connect to Grid:
```python
from selenium import webdriver

# Remote WebDriver
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=webdriver.ChromeOptions()
)
```

### Docker Compose Grid:
```yaml
# docker-compose.yml
version: "3"
services:
  hub:
    image: selenium/hub:latest
    ports:
      - "4444:4444"
  
  chrome:
    image: selenium/node-chrome:latest
    depends_on:
      - hub
    environment:
      - SE_EVENT_BUS_HOST=hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    shm_size: 2gb
  
  firefox:
    image: selenium/node-firefox:latest
    depends_on:
      - hub
    environment:
      - SE_EVENT_BUS_HOST=hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    shm_size: 2gb
```

### Parallel Execution with pytest-xdist:
```bash
pip install pytest-xdist
pytest -n 4  # Run on 4 parallel workers
```

```python
# conftest.py
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=webdriver.ChromeOptions()
    )
    yield driver
    driver.quit()
```""",

    # -------------------------------------------------------------------------
    # BEST PRACTICES
    # -------------------------------------------------------------------------
    "selenium best practices": """## ✨ Selenium Best Practices

### 1. Use Explicit Waits:
```python
# ❌ Bad - Hard sleep
import time
time.sleep(5)

# ✅ Good - Explicit wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable(locator))
```

### 2. Use Page Object Model:
```python
# ❌ Bad - Locators in test
def test_login():
    driver.find_element(By.ID, "username").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("pass")

# ✅ Good - Page Object
def test_login():
    login_page.enter_credentials("user", "pass")
```

### 3. Prefer Reliable Locators:
```python
# ❌ Bad - Fragile XPath
"//div/div[2]/form/input[1]"

# ✅ Good - Stable locators
By.ID, "username"
By.CSS_SELECTOR, "[data-testid='username']"
```

### 4. Handle Exceptions:
```python
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException
)

def safe_click(driver, locator, retries=3):
    for i in range(retries):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except StaleElementReferenceException:
            if i == retries - 1:
                raise
    return False
```

### 5. Clean Test Data:
```python
@pytest.fixture
def setup_teardown(driver):
    # Setup
    create_test_user()
    yield
    # Teardown
    delete_test_user()
    driver.delete_all_cookies()
```

### 6. Meaningful Assertions:
```python
# ❌ Bad
assert driver.find_element(By.ID, "msg")

# ✅ Good
assert "Success" in driver.find_element(By.ID, "msg").text, \\
    "Expected success message not displayed"
```

### 7. Configure Timeouts Appropriately:
```python
# Set reasonable defaults
driver.set_page_load_timeout(30)
driver.set_script_timeout(30)
driver.implicitly_wait(0)  # Use explicit waits instead
```""",
}


# =============================================================================
# ROBOT FRAMEWORK CONCEPTS
# =============================================================================

ROBOT_FRAMEWORK_CONCEPTS = {
    # -------------------------------------------------------------------------
    # BASICS
    # -------------------------------------------------------------------------
    "robot framework": """## 🤖 What is Robot Framework?

**Robot Framework** is an open-source automation framework for acceptance testing, ATDD, and RPA.

### Key Features:
- Keyword-driven testing approach
- Easy-to-read tabular syntax
- Rich ecosystem of libraries
- Excellent reporting
- Platform independent

### Installation:
```bash
pip install robotframework
pip install robotframework-seleniumlibrary  # For web testing
```

### First Test:
```robot
*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}     https://www.google.com
${BROWSER}    chrome

*** Test Cases ***
Open Google And Search
    Open Browser    ${URL}    ${BROWSER}
    Input Text    name=q    Robot Framework
    Press Keys    name=q    ENTER
    Wait Until Page Contains    Robot Framework
    Close Browser
```

### Running Tests:
```bash
robot test_file.robot                    # Single file
robot tests/                             # Directory
robot --include smoke tests/             # By tag
robot --outputdir results tests/         # Custom output
```

### Report Files:
- **log.html** - Detailed execution log
- **report.html** - High-level summary
- **output.xml** - Machine-readable results""",

    "robot test structure": """## 📋 Robot Framework Test Structure

### File Sections:
```robot
*** Settings ***
# Libraries, resources, variables, setup/teardown

*** Variables ***
# Test data and configuration

*** Test Cases ***
# Individual test cases

*** Keywords ***
# Custom/user keywords

*** Comments ***
# Optional comments section
```

### Complete Example:
```robot
*** Settings ***
Documentation    Login functionality tests
Library          SeleniumLibrary
Resource         common.robot
Suite Setup      Open Browser To Login Page
Suite Teardown   Close All Browsers
Test Setup       Go To Login Page
Test Teardown    Capture Screenshot On Failure

*** Variables ***
${LOGIN_URL}     https://example.com/login
${VALID_USER}    testuser
${VALID_PASS}    testpass123

*** Test Cases ***
Valid Login
    [Documentation]    Test successful login with valid credentials
    [Tags]    smoke    login    critical
    Enter Username    ${VALID_USER}
    Enter Password    ${VALID_PASS}
    Click Login Button
    Verify Dashboard Is Displayed

Invalid Login
    [Documentation]    Test login with invalid credentials
    [Tags]    login    negative
    Enter Username    invalid
    Enter Password    invalid
    Click Login Button
    Verify Error Message Is Displayed

*** Keywords ***
Enter Username
    [Arguments]    ${username}
    Input Text    id=username    ${username}

Enter Password
    [Arguments]    ${password}
    Input Password    id=password    ${password}

Click Login Button
    Click Button    id=login-btn

Verify Dashboard Is Displayed
    Wait Until Page Contains Element    id=dashboard
    Title Should Be    Dashboard

Verify Error Message Is Displayed
    Wait Until Element Is Visible    class=error-message
```""",

    "robot variables": """## 📦 Robot Framework Variables

### Scalar Variables:
```robot
*** Variables ***
${NAME}         John Doe
${AGE}          25
${PRICE}        19.99
${IS_ACTIVE}    ${TRUE}
${EMPTY_VAR}    ${EMPTY}
${NONE_VAR}     ${NONE}

*** Test Cases ***
Using Scalar Variables
    Log    Name is ${NAME}
    Should Be Equal As Numbers    ${AGE}    25
```

### List Variables:
```robot
*** Variables ***
@{COLORS}       red    green    blue
@{NUMBERS}      1    2    3    4    5
@{EMPTY_LIST}

*** Test Cases ***
Using List Variables
    Log    First color: ${COLORS}[0]
    Length Should Be    ${COLORS}    3
    FOR    ${color}    IN    @{COLORS}
        Log    Color: ${color}
    END
```

### Dictionary Variables:
```robot
*** Variables ***
&{USER}         name=John    age=30    city=NYC
&{CONFIG}       timeout=30    browser=chrome

*** Test Cases ***
Using Dictionary Variables
    Log    Name: ${USER}[name]
    Log    Age: ${USER.age}
    Should Be Equal    ${USER}[city]    NYC
```

### Variable Scopes:
```robot
*** Test Cases ***
Variable Scope Example
    # Local variable (test case only)
    ${local}=    Set Variable    local value
    
    # Suite variable (all tests in suite)
    Set Suite Variable    ${SUITE_VAR}    suite value
    
    # Global variable (all suites)
    Set Global Variable    ${GLOBAL_VAR}    global value
    
    # Test variable
    Set Test Variable    ${TEST_VAR}    test value
```

### Environment Variables:
```robot
*** Test Cases ***
Using Environment Variables
    ${home}=    Get Environment Variable    HOME
    ${path}=    Get Environment Variable    PATH    default=/usr/bin
    Log    Home directory: ${home}
```""",

    "robot keywords": """## 🔑 Robot Framework Keywords

### Built-in Keywords:
```robot
*** Test Cases ***
Built-in Keyword Examples
    # Logging
    Log    This is a message
    Log Many    First    Second    Third
    Log To Console    Console message
    
    # Variables
    ${var}=    Set Variable    Hello
    ${result}=    Set Variable If    ${condition}    Yes    No
    
    # Conditions
    Should Be Equal    ${actual}    ${expected}
    Should Contain    ${text}    substring
    Should Be True    ${value} > 10
    
    # Control flow
    Run Keyword If    ${status}    Keyword To Run
    Run Keyword Unless    ${status}    Alternative Keyword
    
    # Collections
    ${length}=    Get Length    ${list}
    Append To List    ${list}    new item
    
    # Strings
    ${upper}=    Convert To Upper Case    hello
    ${replaced}=    Replace String    ${text}    old    new
    
    # Time
    Sleep    2s
    ${time}=    Get Time
```

### User Keywords:
```robot
*** Keywords ***
Login With Credentials
    [Documentation]    Logs in with given credentials
    [Arguments]    ${username}    ${password}
    Input Text    id=username    ${username}
    Input Password    id=password    ${password}
    Click Button    Login
    [Return]    ${TRUE}

Keyword With Default Arguments
    [Arguments]    ${name}    ${greeting}=Hello
    Log    ${greeting}, ${name}!

Keyword With Multiple Return Values
    [Arguments]    ${a}    ${b}
    ${sum}=    Evaluate    ${a} + ${b}
    ${diff}=    Evaluate    ${a} - ${b}
    [Return]    ${sum}    ${diff}
```

### Embedded Arguments:
```robot
*** Keywords ***
User "${username}" logs in with password "${password}"
    Input Text    id=username    ${username}
    Input Password    id=password    ${password}
    Click Button    Login

*** Test Cases ***
Login Test With Embedded Arguments
    User "john" logs in with password "secret123"
```

### Keyword Teardown:
```robot
*** Keywords ***
Safe Browser Operation
    [Arguments]    ${url}
    Open Browser    ${url}    chrome
    [Teardown]    Close Browser
```""",

    "robot control flow": """## 🔄 Robot Framework Control Flow

### FOR Loops:
```robot
*** Test Cases ***
FOR Loop Examples
    # Basic FOR loop
    FOR    ${item}    IN    apple    banana    cherry
        Log    Item: ${item}
    END
    
    # Loop with range
    FOR    ${i}    IN RANGE    1    6
        Log    Number: ${i}
    END
    
    # Loop with list
    @{fruits}=    Create List    apple    banana    cherry
    FOR    ${fruit}    IN    @{fruits}
        Log    Fruit: ${fruit}
    END
    
    # Loop with enumerate
    FOR    ${index}    ${item}    IN ENUMERATE    @{fruits}
        Log    ${index}: ${item}
    END
    
    # Loop with zip
    @{names}=    Create List    Alice    Bob
    @{ages}=    Create List    25    30
    FOR    ${name}    ${age}    IN ZIP    ${names}    ${ages}
        Log    ${name} is ${age} years old
    END
```

### IF/ELSE:
```robot
*** Test Cases ***
IF ELSE Examples
    ${status}=    Set Variable    active
    
    # Simple IF
    IF    "${status}" == "active"
        Log    User is active
    END
    
    # IF-ELSE
    IF    ${value} > 10
        Log    Value is greater than 10
    ELSE
        Log    Value is 10 or less
    END
    
    # IF-ELSE IF-ELSE
    IF    ${score} >= 90
        Log    Grade: A
    ELSE IF    ${score} >= 80
        Log    Grade: B
    ELSE IF    ${score} >= 70
        Log    Grade: C
    ELSE
        Log    Grade: F
    END
```

### TRY/EXCEPT:
```robot
*** Test Cases ***
TRY EXCEPT Examples
    TRY
        Click Element    id=nonexistent
    EXCEPT    Element not found
        Log    Element was not found
    EXCEPT    AS    ${error}
        Log    Error occurred: ${error}
    FINALLY
        Log    Cleanup actions here
    END
```

### WHILE Loop:
```robot
*** Test Cases ***
WHILE Loop Example
    ${counter}=    Set Variable    0
    WHILE    ${counter} < 5
        Log    Counter: ${counter}
        ${counter}=    Evaluate    ${counter} + 1
    END
```

### BREAK and CONTINUE:
```robot
*** Test Cases ***
Break and Continue Example
    FOR    ${i}    IN RANGE    10
        IF    ${i} == 3
            CONTINUE
        END
        IF    ${i} == 7
            BREAK
        END
        Log    Number: ${i}
    END
```""",

    "robot seleniumlibrary": """## 🌐 SeleniumLibrary for Robot Framework

### Installation:
```bash
pip install robotframework-seleniumlibrary
```

### Basic Usage:
```robot
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
Web Test Example
    Open Browser    https://example.com    chrome
    Title Should Be    Example Domain
    Close Browser
```

### Browser Keywords:
```robot
*** Test Cases ***
Browser Operations
    # Open browser
    Open Browser    ${URL}    chrome
    Open Browser    ${URL}    firefox    headless=true
    
    # Navigate
    Go To    https://another-url.com
    Go Back
    Go Forward
    Reload Page
    
    # Window management
    Maximize Browser Window
    Set Window Size    1920    1080
    
    # Get info
    ${title}=    Get Title
    ${url}=    Get Location
    ${source}=    Get Source
    
    # Close
    Close Browser
    Close All Browsers
```

### Element Interaction:
```robot
*** Test Cases ***
Element Interactions
    # Find and click
    Click Element    id=button
    Click Button    Submit
    Click Link    Click here
    
    # Input
    Input Text    id=username    myuser
    Input Password    id=password    mypass
    Clear Element Text    id=input
    
    # Dropdowns
    Select From List By Value    id=country    us
    Select From List By Label    id=country    United States
    Select From List By Index    id=country    2
    
    # Checkboxes
    Select Checkbox    id=agree
    Unselect Checkbox    id=newsletter
    Checkbox Should Be Selected    id=agree
    
    # Get info
    ${text}=    Get Text    id=message
    ${value}=    Get Value    id=input
    ${attr}=    Get Element Attribute    id=link    href
```

### Waiting:
```robot
*** Test Cases ***
Wait Examples
    Wait Until Page Contains    Welcome
    Wait Until Page Contains Element    id=result    timeout=10s
    Wait Until Element Is Visible    id=modal
    Wait Until Element Is Not Visible    id=loader
    Wait Until Element Is Enabled    id=submit
    Wait Until Element Contains    id=status    Complete
```

### Screenshots:
```robot
*** Test Cases ***
Screenshot Examples
    Capture Page Screenshot
    Capture Page Screenshot    filename=myshot.png
    Capture Element Screenshot    id=chart    chart.png
    
    # Automatic screenshot on failure
    Register Keyword To Run On Failure    Capture Page Screenshot
```""",

    "robot resource files": """## 📁 Robot Framework Resource Files

### Resource File Structure:
```robot
# resources/common.robot
*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${BROWSER}        chrome
${TIMEOUT}        10s
${BASE_URL}       https://example.com

*** Keywords ***
Open Application
    [Arguments]    ${url}=${BASE_URL}
    Open Browser    ${url}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}

Close Application
    Close All Browsers

Wait And Click
    [Arguments]    ${locator}
    Wait Until Element Is Visible    ${locator}
    Click Element    ${locator}
```

### Using Resources:
```robot
*** Settings ***
Resource    resources/common.robot
Resource    resources/login_keywords.robot

*** Test Cases ***
Test Using Resources
    Open Application
    Login With Valid Credentials
    Close Application
```

### Variable Files (Python):
```python
# variables/config.py
BROWSER = "chrome"
TIMEOUT = 10
BASE_URL = "https://example.com"

def get_credentials():
    return {"username": "user", "password": "pass"}
```

```robot
*** Settings ***
Variables    variables/config.py

*** Test Cases ***
Test Using Variable File
    Log    Browser: ${BROWSER}
    Log    Timeout: ${TIMEOUT}
```

### Library Import with Arguments:
```robot
*** Settings ***
Library    SeleniumLibrary    timeout=10    implicit_wait=5
Library    DatabaseLibrary    dbhost=localhost    dbname=test
Library    CustomLibrary    arg1    arg2
```""",

    "robot reporting": """## 📊 Robot Framework Reporting

### Default Output Files:
- **output.xml** - Machine-readable results
- **log.html** - Detailed execution log
- **report.html** - Summary report

### Command Line Options:
```bash
# Custom output directory
robot --outputdir results tests/

# Custom file names
robot --output custom_output.xml --log custom_log.html tests/

# Only report (no log)
robot --log NONE tests/

# Include timestamp
robot --timestampoutputs tests/

# Merge multiple outputs
rebot --merge output1.xml output2.xml
```

### Log Levels:
```robot
*** Test Cases ***
Logging Example
    Log    Debug message    level=DEBUG
    Log    Info message     level=INFO
    Log    Warning          level=WARN
    Log    Error message    level=ERROR
    
    # Set log level
    Set Log Level    DEBUG
```

### Custom Messages in Report:
```robot
*** Test Cases ***
Test With Documentation
    [Documentation]    This test verifies login functionality.
    ...                It tests both valid and invalid credentials.
    [Tags]    smoke    login
    
    # Add message to report
    Set Test Message    Login verified successfully
    
    # Fail with custom message
    Fail    Custom failure message
```

### Screenshots in Reports:
```robot
*** Test Cases ***
Test With Screenshots
    Capture Page Screenshot    embed=True
    
    # Screenshot on failure
    [Teardown]    Run Keyword If Test Failed    Capture Page Screenshot
```

### Generating Reports:
```bash
# Generate report from output
rebot output.xml

# Combine multiple outputs
rebot --name "Combined" output1.xml output2.xml

# Filter by tag
rebot --include smoke output.xml
```""",

    "robot tags": """## 🏷️ Robot Framework Tags

### Defining Tags:
```robot
*** Settings ***
Force Tags       regression    web
Default Tags     smoke

*** Test Cases ***
Test With Tags
    [Tags]    login    critical    JIRA-123
    Log    This test has multiple tags

Test Without Default Tags
    [Tags]    -smoke    api
    Log    Removed default smoke tag
```

### Running by Tags:
```bash
# Include tag
robot --include smoke tests/

# Exclude tag
robot --exclude slow tests/

# Multiple includes (OR)
robot --include smokeORcritical tests/

# Multiple includes (AND)
robot --include smokeANDlogin tests/

# Combine include and exclude
robot --include regression --exclude slow tests/

# Tag patterns
robot --include JIRA-* tests/
```

### Reserved Tags:
```robot
*** Test Cases ***
Special Tags Example
    [Tags]    robot:skip           # Skip this test
    [Tags]    robot:skip-on-failure    # Skip remaining if fails
    [Tags]    robot:recursive-continue  # Continue on failure
    [Tags]    robot:recursive-stop      # Stop on failure
    [Tags]    robot:flatten           # Flatten keyword
```

### Tag Statistics:
```bash
# Custom tag statistics
robot --tagstatinclude smoke* --tagstatexclude slow tests/

# Combine tags in statistics  
robot --tagstatcombine smokeANDlogin:critical_login tests/
```""",

    "robot listeners": """## 👂 Robot Framework Listeners

### What are Listeners?
Listeners are classes that can react to events during test execution.

### Built-in Listener Interface:
```python
# my_listener.py
class MyListener:
    ROBOT_LISTENER_API_VERSION = 3
    
    def start_suite(self, data, result):
        print(f"Starting suite: {data.name}")
    
    def end_suite(self, data, result):
        print(f"Suite {data.name} finished: {result.status}")
    
    def start_test(self, data, result):
        print(f"Starting test: {data.name}")
    
    def end_test(self, data, result):
        print(f"Test {data.name}: {result.status}")
    
    def start_keyword(self, data, result):
        pass
    
    def end_keyword(self, data, result):
        pass
    
    def log_message(self, message):
        if message.level == 'FAIL':
            print(f"FAILURE: {message.message}")
    
    def close(self):
        print("Listener closing")
```

### Using Listeners:
```bash
# Command line
robot --listener my_listener.py tests/
robot --listener my_listener.py:arg1:arg2 tests/

# Multiple listeners
robot --listener listener1.py --listener listener2.py tests/
```

### Listener for Reporting:
```python
# slack_notifier.py
import requests

class SlackNotifier:
    ROBOT_LISTENER_API_VERSION = 3
    
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.results = {"passed": 0, "failed": 0}
    
    def end_test(self, data, result):
        if result.status == "PASS":
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
    
    def close(self):
        message = f"Tests completed: {self.results['passed']} passed, {self.results['failed']} failed"
        requests.post(self.webhook_url, json={"text": message})
```""",

    "robot custom library": """## 📚 Creating Custom Robot Framework Libraries

### Simple Library Class:
```python
# CustomLibrary.py
class CustomLibrary:
    \"\"\"Custom library for Robot Framework.\"\"\"
    
    ROBOT_LIBRARY_SCOPE = 'SUITE'  # or TEST, GLOBAL
    
    def __init__(self, base_url=None):
        self.base_url = base_url
    
    def say_hello(self, name):
        \"\"\"Says hello to the given name.
        
        Example:
        | Say Hello | World |
        \"\"\"
        return f"Hello, {name}!"
    
    def add_numbers(self, a, b):
        \"\"\"Adds two numbers and returns the result.\"\"\"
        return int(a) + int(b)
    
    def should_be_positive(self, number):
        \"\"\"Verifies that number is positive.\"\"\"
        if int(number) <= 0:
            raise AssertionError(f"{number} is not positive")
```

### Using Custom Library:
```robot
*** Settings ***
Library    CustomLibrary.py    base_url=https://api.example.com

*** Test Cases ***
Test Custom Library
    ${greeting}=    Say Hello    World
    Should Be Equal    ${greeting}    Hello, World!
    
    ${sum}=    Add Numbers    5    3
    Should Be Equal As Numbers    ${sum}    8
    
    Should Be Positive    10
```

### Library with State:
```python
# SessionLibrary.py
class SessionLibrary:
    ROBOT_LIBRARY_SCOPE = 'TEST'
    
    def __init__(self):
        self._session = None
    
    def create_session(self, username):
        self._session = {"user": username, "active": True}
        return self._session
    
    def get_current_user(self):
        if not self._session:
            raise RuntimeError("No active session")
        return self._session["user"]
    
    def close_session(self):
        self._session = None
```

### Dynamic Library:
```python
class DynamicLibrary:
    def get_keyword_names(self):
        return ['dynamic_keyword', 'another_keyword']
    
    def run_keyword(self, name, args, kwargs):
        if name == 'dynamic_keyword':
            return self._dynamic_keyword(*args, **kwargs)
    
    def get_keyword_documentation(self, name):
        return f"Documentation for {name}"
```""",

    "robot pabot": """## 🔀 Parallel Execution with Pabot

### Installation:
```bash
pip install robotframework-pabot
```

### Basic Usage:
```bash
# Run tests in parallel
pabot tests/

# Specify number of processes
pabot --processes 4 tests/

# Parallel by test
pabot --testlevelsplit tests/

# Parallel by suite
pabot tests/
```

### Pabot Options:
```bash
# Resource file for shared resources
pabot --resourcefile resources.dat tests/

# Ordering file
pabot --ordering orderfile.txt tests/

# Output directory
pabot --outputdir results tests/

# Verbose mode
pabot --verbose tests/
```

### Resource File (Shared State):
```
# resources.dat
# Define shared resources that shouldn't run in parallel

[browser1]
BROWSER_TYPE=chrome
PORT=4444

[browser2]
BROWSER_TYPE=firefox
PORT=4445
```

### Using Shared Resources:
```robot
*** Settings ***
Library    pabot.PabotLib

*** Test Cases ***
Test With Shared Resource
    Acquire Value Set    browser1
    ${browser}=    Get Value From Set    BROWSER_TYPE
    Log    Using browser: ${browser}
    Release Value Set
```

### Best Practices:
- Ensure tests are independent
- Use unique test data per test
- Avoid shared state between tests
- Use resource files for limited resources""",
}


# =============================================================================
# RELATED TOOLS CONCEPTS
# =============================================================================

RELATED_TOOLS_CONCEPTS = {
    "pytest": """## 🧪 pytest Framework

**pytest** is a powerful Python testing framework that makes writing tests simple.

### Installation:
```bash
pip install pytest pytest-html pytest-xdist
```

### Basic Test:
```python
# test_example.py
def test_addition():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"

class TestMath:
    def test_multiply(self):
        assert 3 * 4 == 12
```

### Running Tests:
```bash
pytest                      # Run all tests
pytest test_file.py         # Specific file
pytest -v                   # Verbose
pytest -k "test_add"        # By name pattern
pytest -m smoke             # By marker
pytest --html=report.html   # Generate HTML report
```

### Assertions:
```python
def test_assertions():
    # Basic
    assert value == expected
    assert value != other
    assert value is True
    assert value is not None
    
    # Collections
    assert item in collection
    assert len(items) == 5
    
    # Exceptions
    with pytest.raises(ValueError):
        int("not a number")
    
    # Approximate
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

### Markers:
```python
import pytest

@pytest.mark.smoke
def test_quick():
    pass

@pytest.mark.slow
def test_long_running():
    pass

@pytest.mark.skip(reason="Not implemented")
def test_future():
    pass

@pytest.mark.xfail
def test_expected_failure():
    assert False

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (2, 3, 5),
    (10, 20, 30)
])
def test_add(a, b, expected):
    assert a + b == expected
```""",

    "pytest fixtures": """## 🔧 pytest Fixtures

### Basic Fixture:
```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Test", "value": 42}

def test_using_fixture(sample_data):
    assert sample_data["name"] == "Test"
```

### Fixture Scopes:
```python
@pytest.fixture(scope="function")  # Default - each test
def func_fixture():
    return "function scope"

@pytest.fixture(scope="class")  # Each test class
def class_fixture():
    return "class scope"

@pytest.fixture(scope="module")  # Each module
def module_fixture():
    return "module scope"

@pytest.fixture(scope="session")  # Entire test session
def session_fixture():
    return "session scope"
```

### Setup and Teardown:
```python
@pytest.fixture
def browser():
    # Setup
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    yield driver  # Test runs here
    
    # Teardown
    driver.quit()

def test_google(browser):
    browser.get("https://google.com")
    assert "Google" in browser.title
```

### Fixture with Parameters:
```python
@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()
    yield driver
    driver.quit()

def test_cross_browser(browser):
    browser.get("https://example.com")
```

### conftest.py (Shared Fixtures):
```python
# conftest.py - fixtures available to all tests
import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def base_url():
    return "https://example.com"

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def logged_in_driver(driver, base_url):
    driver.get(f"{base_url}/login")
    # Perform login
    return driver
```""",

    "pytest selenium": """## 🌐 pytest with Selenium

### Project Structure:
```
project/
├── conftest.py
├── pytest.ini
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── login_page.py
└── tests/
    ├── __init__.py
    └── test_login.py
```

### conftest.py:
```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--headless", action="store_true")

@pytest.fixture(scope="session")
def browser_type(request):
    return request.config.getoption("--browser")

@pytest.fixture
def driver(request, browser_type):
    if browser_type == "chrome":
        options = Options()
        if request.config.getoption("--headless"):
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    elif browser_type == "firefox":
        driver = webdriver.Firefox()
    
    driver.implicitly_wait(10)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.failed:
        driver = item.funcargs.get('driver')
        if driver:
            driver.save_screenshot(f"screenshots/{item.name}.png")
```

### pytest.ini:
```ini
[pytest]
markers =
    smoke: Quick smoke tests
    regression: Full regression tests
    login: Login functionality tests

testpaths = tests
python_files = test_*.py
python_functions = test_*

addopts = -v --html=reports/report.html
```

### Test File:
```python
# tests/test_login.py
import pytest
from pages.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.login
def test_valid_login(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("user", "pass")
    assert login_page.is_logged_in()

@pytest.mark.login
@pytest.mark.parametrize("username,password", [
    ("invalid", "invalid"),
    ("", "password"),
    ("user", ""),
])
def test_invalid_login(driver, username, password):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)
    assert login_page.is_error_displayed()
```""",

    "unittest": """## 🧪 unittest Framework

**unittest** is Python's built-in testing framework.

### Basic Test:
```python
import unittest

class TestMath(unittest.TestCase):
    
    def test_addition(self):
        self.assertEqual(1 + 1, 2)
    
    def test_subtraction(self):
        self.assertEqual(5 - 3, 2)
    
    def test_string_upper(self):
        self.assertEqual("hello".upper(), "HELLO")

if __name__ == "__main__":
    unittest.main()
```

### Setup and Teardown:
```python
class TestWithSetup(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        \"\"\"Run once before all tests in class.\"\"\"
        cls.shared_resource = "setup"
    
    @classmethod
    def tearDownClass(cls):
        \"\"\"Run once after all tests in class.\"\"\"
        cls.shared_resource = None
    
    def setUp(self):
        \"\"\"Run before each test.\"\"\"
        self.test_data = [1, 2, 3]
    
    def tearDown(self):
        \"\"\"Run after each test.\"\"\"
        self.test_data = None
    
    def test_example(self):
        self.assertEqual(len(self.test_data), 3)
```

### Assertions:
```python
class TestAssertions(unittest.TestCase):
    
    def test_assertions(self):
        # Equality
        self.assertEqual(a, b)
        self.assertNotEqual(a, b)
        
        # Boolean
        self.assertTrue(condition)
        self.assertFalse(condition)
        
        # None
        self.assertIsNone(value)
        self.assertIsNotNone(value)
        
        # Type
        self.assertIsInstance(obj, cls)
        
        # Membership
        self.assertIn(item, container)
        self.assertNotIn(item, container)
        
        # Exceptions
        with self.assertRaises(ValueError):
            int("not a number")
        
        # Numeric
        self.assertAlmostEqual(0.1 + 0.2, 0.3, places=5)
        self.assertGreater(5, 3)
        self.assertLess(3, 5)
```

### Test Discovery:
```bash
python -m unittest discover
python -m unittest discover -s tests -p "test_*.py"
```""",

    "allure reporting": """## 📊 Allure Reporting

### Installation:
```bash
pip install allure-pytest
# Also need Allure command line tool
brew install allure  # macOS
```

### Basic Usage:
```python
import allure

@allure.feature("Login")
@allure.story("Valid Login")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_login(driver):
    with allure.step("Open login page"):
        driver.get("https://example.com/login")
    
    with allure.step("Enter credentials"):
        driver.find_element(By.ID, "username").send_keys("user")
        driver.find_element(By.ID, "password").send_keys("pass")
    
    with allure.step("Click login button"):
        driver.find_element(By.ID, "login").click()
    
    with allure.step("Verify login success"):
        assert "Dashboard" in driver.title
```

### Allure Decorators:
```python
import allure

@allure.epic("E-Commerce")
@allure.feature("Shopping Cart")
@allure.story("Add Item to Cart")
@allure.title("Test adding product to cart")
@allure.description("Verifies that user can add product to cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("cart", "smoke")
@allure.link("https://jira.com/ISSUE-123", name="JIRA")
@allure.issue("BUG-456")
@allure.testcase("TC-789")
def test_add_to_cart():
    pass
```

### Attachments:
```python
@allure.step("Take screenshot")
def take_screenshot(driver, name):
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG
    )

@allure.step("Attach log")
def attach_log(log_content):
    allure.attach(
        log_content,
        name="log",
        attachment_type=allure.attachment_type.TEXT
    )
```

### Generate Report:
```bash
# Run tests and generate results
pytest --alluredir=allure-results

# Generate and open report
allure serve allure-results

# Generate static report
allure generate allure-results -o allure-report
```""",

    "jenkins integration": """## 🔧 Jenkins CI/CD Integration

### Jenkinsfile (Pipeline):
```groovy
pipeline {
    agent any
    
    environment {
        BROWSER = 'chrome'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    pytest tests/ \\
                        --junitxml=reports/junit.xml \\
                        --html=reports/report.html \\
                        --alluredir=allure-results
                '''
            }
        }
        
        stage('Robot Tests') {
            steps {
                sh 'robot --outputdir results tests/'
            }
        }
    }
    
    post {
        always {
            // Archive test results
            junit 'reports/junit.xml'
            
            // Publish HTML report
            publishHTML([
                allowMissing: false,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Test Report'
            ])
            
            // Allure report
            allure includeProperties: false,
                   results: [[path: 'allure-results']]
            
            // Robot Framework results
            robot outputPath: 'results',
                  passThreshold: 90.0,
                  unstableThreshold: 80.0
        }
        
        failure {
            mail to: 'team@example.com',
                 subject: "Test Failed: ${env.JOB_NAME}",
                 body: "Check console output at ${env.BUILD_URL}"
        }
    }
}
```

### Docker Integration:
```groovy
pipeline {
    agent {
        docker {
            image 'python:3.9'
            args '-v /dev/shm:/dev/shm'
        }
    }
    
    stages {
        stage('Test') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pytest --headless
                '''
            }
        }
    }
}
```

### Selenium Grid in Jenkins:
```groovy
stage('Parallel Browser Tests') {
    parallel {
        stage('Chrome') {
            steps {
                sh 'pytest --browser=chrome'
            }
        }
        stage('Firefox') {
            steps {
                sh 'pytest --browser=firefox'
            }
        }
    }
}
```""",

    "github actions": """## 🔄 GitHub Actions for Testing

### Basic Workflow:
```yaml
# .github/workflows/tests.yml
name: Run Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run pytest
        run: |
          pytest --junitxml=results.xml
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: results.xml
```

### Selenium Tests:
```yaml
jobs:
  selenium-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install Chrome
        run: |
          wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
          sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
          sudo apt-get update
          sudo apt-get install -y google-chrome-stable
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run Selenium tests
        run: pytest tests/selenium/ --headless
      
      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: screenshots
          path: screenshots/
```

### Matrix Testing:
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10']
        browser: ['chrome', 'firefox']
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Run tests on ${{ matrix.browser }}
        run: pytest --browser=${{ matrix.browser }}
```""",

    "docker selenium": """## 🐳 Docker for Selenium Testing

### Docker Compose for Selenium Grid:
```yaml
# docker-compose.yml
version: "3"
services:
  selenium-hub:
    image: selenium/hub:latest
    container_name: selenium-hub
    ports:
      - "4444:4444"
  
  chrome:
    image: selenium/node-chrome:latest
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    shm_size: 2gb
  
  firefox:
    image: selenium/node-firefox:latest
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443
    shm_size: 2gb
  
  tests:
    build: .
    depends_on:
      - chrome
      - firefox
    environment:
      - SELENIUM_HUB=http://selenium-hub:4444/wd/hub
    command: pytest tests/
```

### Dockerfile for Tests:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "tests/", "-v"]
```

### Connect to Dockerized Grid:
```python
from selenium import webdriver

def get_remote_driver(browser="chrome"):
    options = webdriver.ChromeOptions() if browser == "chrome" else webdriver.FirefoxOptions()
    
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )
    return driver
```

### Standalone Chrome:
```bash
# Run Chrome standalone
docker run -d -p 4444:4444 -p 7900:7900 --shm-size 2g selenium/standalone-chrome

# Connect in Python
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=webdriver.ChromeOptions()
)

# Watch in browser at http://localhost:7900 (VNC)
```""",
}


# =============================================================================
# COMBINED CONCEPTS DICTIONARY
# =============================================================================

ALL_AUTOMATION_CONCEPTS = {
    **SELENIUM_CONCEPTS,
    **ROBOT_FRAMEWORK_CONCEPTS,
    **RELATED_TOOLS_CONCEPTS,
}


# Automation-related tags for filtering
AUTOMATION_TAGS = [
    "Selenium", "WebDriver", "Locators", "XPath", "CSS Selectors",
    "Waits", "Actions", "Page Object Model", "Headless", "Grid",
    "Robot Framework", "Keywords", "Variables", "SeleniumLibrary",
    "pytest", "unittest", "Fixtures", "CI/CD", "Jenkins", "Docker"
]


