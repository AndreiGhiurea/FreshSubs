# -*- mode: python -*-

block_cipher = None


a = Analysis(['GUI.py'],
             pathex=['C:\\Users\\Andrei\\Desktop\\Developer\\Python\\FreshSubs', 'C:\\Users\\Andrei\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\PyQt5\\Qt\\bin'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='FreshSubs',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='fresh.ico')
