#!/usr/bin/python3.5
# coding=utf-8
# Myimport.py

# import sys

def my_import(modulename, alias):
    if modulename not in sys.modules:
        import modulname as alias
