[app]

title = CBT Registration Checker
package.name = cbtchecker
package.domain = edu.uniuyo

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.3

requirements = python3,kivy==2.3.1,android

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 26
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
