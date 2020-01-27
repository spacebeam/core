#!/usr/bin/env bash

function install_java() {
    cd ~ 
    wget https://repo.huaweicloud.com/java/jdk/8u192-b12/jdk-8u192-windows-i586.exe 
    sudo -u wine wine jdk-8u192-windows-i586.exe /s
    REG_KEY="HKEY_CURRENT_USER\Environment"
    sudo -u wine wine REG ADD "${REG_KEY}" /v PATH /t REG_EXPAND_SZ /d "C:\Program Files (x86)\Java\jre1.8.0_192\bin" /f
}

install_java
