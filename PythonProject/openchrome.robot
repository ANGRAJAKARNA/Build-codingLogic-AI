*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${u}    https://www.amazon.in/
${b}    chrome

*** Test Cases ***
Run Page
    Open Browser    ${u}    ${b}
    Maximize Browser Window
    Sleep    3s
    Click Element    //span[@class="nav-line-2 "]
    Sleep    3
    Close Browser
