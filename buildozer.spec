[app]

# (str) Title of your application
title = Hisab AlHimayat

# (str) Package name
package.name = hisabalhimayat

# (str) Package domain (needed for android/ios packaging)
package.domain = org.app

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (تمت إضافة ttf لحزم ملف الخط font.ttf والصور)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application versioning
version = 0.1

# (list) Application requirements
# تشمل كيفي ومكتبات معالجة النص العربي إن وجدت
requirements = python3,kivy,arabic_reshaper,python-bidi

# (str) Icon of the application (ملف الأيقونة)
icon.filename = %(source.dir)s/icon.png

# (str) Presplash of the application (ملف الخلفية عند فتح التطبيق)
presplash.filename = %(source.dir)s/background.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1

[app:android]

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (bool) Accept SDK license automatically (ضروري جداً لبيئة كولاب لتجنب التوقف)
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a
