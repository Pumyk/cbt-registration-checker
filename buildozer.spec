[app]

# App metadata
title = CBT Registration Checker
package.name = cbtchecker
package.domain = edu.uniuyo

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Version
version = 1.2

# Requirements
requirements = python3,kivy==2.3.1,android

# App icon
icon.filename = icon_512.png

# Android config
orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET

# SDK/NDK
android.api = 33
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Use pre-cloned patched p4a (Python 3.12.10 instead of 3.14.2)
p4a.source_dir = /tmp/p4a-patched

# Logging
log_level = 2
