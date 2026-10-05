[app]
title = MyLockApp
package.name = mylockapp
package.domain = org.test
source.dir = .
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 1

# 权限配置（悬浮窗、读存储、震动）
android.permissions = SYSTEM_ALERT_WINDOW, READ_EXTERNAL_STORAGE, VIBRATE

# 编译架构与 NDK（只编译现代手机的64位架构，强制使用稳定的25b版本）
android.archs = arm64-v8a
android.ndk = 25b
android.api = 33
android.minapi = 21

# 确保图片资源被打包进去
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = shizuku.jpg

# 附加优化配置
android.allow_backup = True
android.wakelock = True
android.python_version = 3.11