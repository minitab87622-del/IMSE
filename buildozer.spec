[app]

# (str) Title of your application
title = Industrial GPA Calculator

# (str) Package name
package.name = gpacalculator

# (str) Package domain
package.domain = org.industrial.app

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (شملنا ملفات الخطوط ttf)
source.include_exts = py,png,jpg,kv,atlas,json,ttf

# (str) Application versioning
version = 1.0

# (list) Application requirements (تمت إضافة مكتبات اللغة العربية)
requirements = python3,kivy,arabic_reshaper,python-bidi

# (str) Custom source code for requirements
icon.filename = %(source.dir)s/icon.png

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (list) List of Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
