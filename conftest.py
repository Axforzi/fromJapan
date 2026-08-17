"""Asegura que la raíz del proyecto esté en sys.path para importar `app`, `schema`, etc."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))