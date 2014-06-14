#!/bin/sh
cd thirdparty
node node_modules/shadowsocks/bin/sslocal -c ../ss1config.json &
node node_modules/shadowsocks/bin/sslocal -c ../ss2config.json &
