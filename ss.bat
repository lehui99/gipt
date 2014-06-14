@echo off
cd thirdparty
start node node_modules\shadowsocks\bin\sslocal -c ..\ss1config.json
start node node_modules\shadowsocks\bin\sslocal -c ..\ss2config.json
