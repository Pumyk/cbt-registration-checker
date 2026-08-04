[app]

# App metadata
title = CBT Registration Checker
package.name = cbtchecker
package.domain = edu.uniuyo

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Version
version = 1.0

# Requirements
requirements = python3,kivy==2.3.1,android

# Android config
orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET

# Build settings
bootstrap = sdl2
build_arch = arm64-v8a,armeabi-v7a

# Landscape
android.api = 34
android.minapi = 24
android.ndk = 26b
android.accept_sdk_license = True

# Logging
log_level = 2

# Copy libs
android.add_src = 
