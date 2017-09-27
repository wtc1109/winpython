# -*- mode: python -*-

block_cipher = None


a = Analysis(['file.py'],
             pathex=['C:\\Python27', 'C:\\Python27\\Lib', 'C:\\Python27\\Lib\\site-packages\\pycrypto-2.6.1\\lib\\Crypto\\Random\\OSRNG', 'C:\\Python27\\Lib\\site-packages\\M2CryptoWin64-0.21.1-3\\build\\lib\\M2Crypto', 'C:\\Python27\\Lib\\site-packages\\M2CryptoWin64-0.21.1-3\\build\\lib\\M2Crypto\\SSL', 'C:\\Python27\\Lib\\site-packages\\M2CryptoWin64-0.21.1-3\\build\\lib\\M2Crypto\\PGP', 'C:\\Python27\\Lib\\site-packages\\M2CryptoWin64-0.21.1-3\\M2Crypto', 'C:\\Python27\\Lib\\site-packages\\M2Crypto', 'C:\\Python27\\Lib\\site-packages\\M2Crypto\\SSL', 'C:\\Python27\\Lib\\site-packages\\M2Crypto\\PGP', 'C:\\Python27\\Lib\\site-packages\\pycrypto-2.6.1\\lib\\Crypto\\', 'C:\\Users\\BlueCard\\PycharmProjects\\winpython'],
             binaries=[],
             datas=[],
             hiddenimports=['queue'],
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
          name='file',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
