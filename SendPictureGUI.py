from tkinter import *
import os
import calendar
from datetime import datetime
from tkinter import messagebox
from tkinter import scrolledtext
import itchat
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import threading

window=Tk()
window.title('发送微信定时器')
is_login=False
is_started=False
path='./pics/'

today=datetime.today()
month=calendar.monthrange(today.year,today.month)[1]
cornType='1-'
cornType+=str(month)

scheduler = BlockingScheduler()

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_logs(log):
    t_logs.insert('end',get_time()+' || '+log+'\n')
    t_logs.see(END)

def clear_logs():
    t_logs.delete(1.0,END)

def loginCallback():
    print("***登录成功***")
    add_logs("***登录成功***")

def exitCallback():
    print("***已退出***")
    add_logs("***已退出***")

def login():
    itchat.auto_login(hotReload=True,enableCmdQR=2, loginCallback=loginCallback, exitCallback=exitCallback)

def logout():
    itchat.logout()

def wechat_login():
    global is_login
    if is_login==False:
        add_logs('开始登录微信')
        print('登陆微信')
        login()
        is_login=True
        log_btn.configure(state='disabled')
        logout_btn.configure(state='normal')
    else:
        add_logs('注销微信')
        logout()
        is_login=False
        log_btn.configure(state='normal')
        logout_btn.configure(state='disabled')

def find_chatroom(room_name):
    for room in itchat.get_chatrooms(update=True):
        if room['NickName']==room_name:
            return room

def sendMsg():
    month = datetime.now().month
    day = datetime.now().day
    filename = str(month) + "." + str(day) + ".jpg"
    file_path = path + filename;
    chatroom = find_chatroom(e_nickname.get())
    print(e_nickname.get())
    room_name = chatroom['UserName']
    #itchat.send(msg=u'发送图片测试:' + get_time(), toUserName=room_name)
    itchat.send(msg='@img@' + file_path, toUserName=room_name)
    print("***消息发送完成" + get_time() + "***")
    add_logs("***消息发送完成" + get_time() + "***")

def job_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')


def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()

def start_scheduler(scheduler):
    global is_started
    global is_login
    if is_login==False:
        messagebox.showinfo('提示','需先登录微信')
    else:
        hour=e_hour.get()
        minute=e_minute.get()
        if is_started==False:
            add_logs('计时器开始工作')
            is_started=True
            start_btn.configure(state='disabled')
            end_btn.configure(state='normal')
            trigger = CronTrigger(day=cornType, hour=int(hour), minute=int(minute))
            scheduler.add_job(sendMsg, trigger)
            scheduler.start()
        else:
            add_logs('计时器停止工作')
            is_started=False
            start_btn.configure(state='normal')
            end_btn.configure(state='disabled')
            scheduler.shutdown()

def stop():
    print('计时器结束工作')

l1=Label(window,text="登录状态：")
l1.grid(row=0,column=0,sticky=W)


log_btn=Button(window,text='登录',command=wechat_login)
log_btn.grid(row=0,column=1,sticky=W)

logout_btn=Button(window,text='注销登录',state='disabled',command=wechat_login)
logout_btn.grid(row=0,column=2,sticky=W)

l_pics=Label(window,text='文件夹图片：')
l_pics.grid(row=1,column=0,sticky=W)

pics=os.listdir(path)
t_pics=Text(window,height=3)
t_pics.insert('insert',pics)
t_pics.grid(row=1,column=1,columnspan=5)



Label(window,text='定时器：').grid(row=2,column=0,sticky=W)
Label(window,text=cornType).grid(row=2,column=1,sticky=W)
Label(window,text='hour:').grid(row=2,column=2,sticky=W)
e_hour=Entry(window)
e_hour.grid(row=2,column=3,sticky=W)
Label(window,text='minute:').grid(row=2,column=4,sticky=W)
e_minute=Entry(window)
e_minute.grid(row=2,column=5,sticky=W)

Label(window,text='群名称:').grid(row=3,column=0,sticky=W)
e_nickname=Entry(window)
e_nickname.grid(row=3,column=1,sticky=W)

start_btn=Button(window,text='开始',command=lambda :thread_it(start_scheduler,scheduler))
start_btn.grid(row=4,column=0)

end_btn=Button(window,text='停止',command=lambda :thread_it(start_scheduler,scheduler))
end_btn.grid(row=4,column=1)

Button(window,text='清空',command=clear_logs).grid(row=5)
t_logs=scrolledtext.ScrolledText(window,height=8)
t_logs.grid(row=6,columnspan=6)


mainloop()