#!/bin/bash

if [ $# -gt 0 ]; then
  case "$1" in
    --cinder)
      exec pytest test-cinder/* --alluredir=allure-results
      ;;
    --nova)
      exec pytest test-nova/* --alluredir=allure-results
      ;;
    --neutron)
      exec pytest test-neutron/* --alluredir=allure-results
      ;;
    --glance)
      exec pytest test-glance/* --alluredir=allure-results
      ;;
    --all)
      exec pytest test* --alluredir=allure-results
      ;;
    *)
      echo "Invalid command: $1"
      exit 1
      ;;
  esac
else
  exec pytest test* --alluredir=allure-results
fi