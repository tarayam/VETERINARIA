#!/usr/bin/env python
"""
Script para compilar traducciones sin gettext en Windows
"""
import polib
import os

def compile_po_to_mo():
    """Compila archivos .po a .mo"""
    locale_dir = 'locale/es/LC_MESSAGES'
    po_file = os.path.join(locale_dir, 'django.po')
    mo_file = os.path.join(locale_dir, 'django.mo')
    
    if os.path.exists(po_file):
        # Cargar el archivo .po
        po = polib.pofile(po_file)
        
        # Compilar a .mo
        po.save_as_mofile(mo_file)
        print(f"Archivo compilado: {mo_file}")
    else:
        print(f"Archivo no encontrado: {po_file}")

if __name__ == "__main__":
    compile_po_to_mo()
