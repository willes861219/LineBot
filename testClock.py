import winsound
import time

my_hour = input('請輸入時：')
my_minute = input('請輸入分：')
print('您的鬧鈴已設定成功！等待它叫醒你吧~~~~')

while True:
    current_time = time.strftime('%H:%M', time.localtime())
    now = current_time.split(':')

    if my_hour == now[0] and my_minute == now[1]:
        winsound.Beep(600, 1000)
        break
    