"""Shared pytest setup: put scripts/ on sys.path so tests import the scripts as modules."""
import os
import sys

sys.dont_write_bytecode = True
SCRIPTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
