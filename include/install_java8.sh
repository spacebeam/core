#!/usr/bin/env bash

function install_java() {
    cd /usr/src
    wget https://github.com/frekele/oracle-java/releases/download/8u212-b10/jdk-8u212-windows-i586.exe
    wine jdk-8u212-windows-i586.exe /s
    REG_KEY="HKEY_CURRENT_USER\Environment"
    wine REG ADD "${REG_KEY}" /v PATH /t REG_EXPAND_SZ /d "C:\Program Files (x86)\Java\jre1.8.0_212\bin" /f
}

install_java
