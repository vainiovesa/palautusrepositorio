*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Input Text  username  aku
    Input Password  password  ankka123
    Input Password  password_confirmation  ankka123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Input Text  username  a
    Input Password  password  salasana1
    Input Password  password_confirmation  salasana1
    Click Button  Register
    Register Should Fail With Message  Username too short

Register With Valid Username And Too Short Password
    Input Text  username  käyttäjänimi
    Input Password  password  1yhyt
    Input Password  password_confirmation  1yhyt
    Click Button  Register
    Register Should Fail With Message  Password too short

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Input Text  username  käyttäjänimi
    Input Password  password  salasana
    Input Password  password_confirmation  salasana
    Click Button  Register
    Register Should Fail With Message  Password can't consist solely of letters

Register With Nonmatching Password And Password Confirmation
    Input Text  username  käyttäjänimi
    Input Password  password  salasana_123
    Input Password  password_confirmation  salasana_321
    Click Button  Register
    Register Should Fail With Message  Password and confirmation don't match

Register With Username That Is Already In Use
    Input Text  username  roope
    Input Password  password  ankka123
    Input Password  password_confirmation  ankka123
    Click Button  Register
    Register Should Succeed
    Go To Register Page
    Input Text  username  roope
    Input Password  password  rahasäiliö1
    Input Password  password_confirmation  rahasäiliö1
    Click Button  Register
    Register Should Fail With Message  A user with this username already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page