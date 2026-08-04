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

# Pin python-for-android to a release that uses Python 3.11.5
p4a.branch = v2024.01.21

# App icon
icon.filename = icon_512.png

# Android config
orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET

# Build settings
bootstrap = sdl2
build_arch = arm64-v8a,armeabi-v7a

# SDK/NDK
android.api = 33
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True

# Logging
log_level = 2
