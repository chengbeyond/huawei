#! /usr/bin/env python
#  -*- coding: utf-8 -*-


import sys
import requests
import winreg
import re
import threading
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

import ip_proxy_support


def vp_start_gui():
    global val, w, root
    root = tk.Tk()
    root.resizable(False, False)
    root.update()
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    width = 402
    height = 128
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)

    top = Toplevel1(root)
    ip_proxy_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    ip_proxy_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font9 = "-family {Microsoft YaHei UI} -size 10 -weight normal " \
                "-slant roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        top.title("设置本机代理IP小工具")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.TEntry1 = ttk.Entry(top)
        self.TEntry1.place(relx=0.124, rely=0.098, relheight=0.209
                           , relwidth=0.438)
        self.TEntry1.configure(takefocus="")
        self.TEntry1.configure(cursor="ibeam")

        self.TEntry2 = ttk.Entry(top)
        self.TEntry2.place(relx=0.697, rely=0.098, relheight=0.209
                           , relwidth=0.189)
        self.TEntry2.configure(takefocus="")
        self.TEntry2.configure(cursor="ibeam")

        self.TLabel1 = ttk.Label(top)
        self.TLabel1.place(relx=0.05, rely=0.131, height=23, width=16)
        self.TLabel1.configure(background="#d9d9d9")
        self.TLabel1.configure(foreground="#000000")
        self.TLabel1.configure(font=font9)
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(text='''IP''')

        self.TLabel2 = ttk.Label(top)
        self.TLabel2.place(relx=0.585, rely=0.121, height=21, width=29)
        self.TLabel2.configure(background="#d9d9d9")
        self.TLabel2.configure(foreground="#000000")
        self.TLabel2.configure(font=font9)
        self.TLabel2.configure(relief='flat')
        self.TLabel2.configure(text='''port''')

        self.TLabel3 = ttk.Label(top)
        self.TLabel3.place(relx=0.124, rely=0.719, height=21, width=500)
        self.TLabel3.configure(background="#d9d9d9")
        self.TLabel3.configure(foreground="#000000")
        self.TLabel3.configure(font="TkDefaultFont")
        self.TLabel3.configure(relief='flat')
        self.TLabel3.configure(text='''准备就绪''')

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.124, rely=0.392, height=28, width=95)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=self.set_ips)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''设置为本机代理''')

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.398, rely=0.392, height=28, width=62)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(command=self.restores)
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''还原设置''')

        self.Button3 = tk.Button(top)
        self.Button3.place(relx=0.597, rely=0.392, height=28, width=83)
        self.Button3.configure(activebackground="#ececec")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(command=self.check_ips)
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''测试是否有效''')

    def set_ips(self):
        t1 = threading.Thread(target=self.set_ip)
        t1.start()

    def restores(self):
        t2 = threading.Thread(target=self.restore)
        t2.start()

    def check_ips(self):
        t3 = threading.Thread(target=self.check_ip)
        t3.start()

    def set_ip(self):
        ip = self.TEntry1.get()
        port = self.TEntry2.get()
        rule_ip = r"^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$"
        rule_port = r"\d+?"
        ret = re.match(rule_ip, ip)
        ret2 = re.match(rule_port, port)

        if ret is None or ret2 is None:
            self.TLabel3.configure(text='''请输入有效IP或者port''')
            return

        proxy = ip + ":" + str(port)
        xpath = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, xpath, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy)
        except Exception as e:
            print("ERROR: " + str(e.args))
        finally:
            None
        self.TLabel3.configure(text='''设置成功''')

    def restore(self):
        proxy = ""
        xpath = "Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, xpath, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy)
            self.TLabel3.configure(text='''设置已经还原，请重新打开浏览器''')
        except Exception as e:
            print("ERROR: " + str(e.args))
        finally:
            None

    def check_ip(self):
        try:
            url = "https://api.ipify.org/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                              "537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
            }
            res = requests.get(url, headers=headers, verify=False)
            ret = res.content.decode()
            print('''当前IP代理地址：%s''' % ret)
            self.TLabel3.configure(text='''当前IP地址：%s''' % ret)
        except Exception as e:
            self.TLabel3.configure(text='''当前IP代理无效''')
            print(e)

if __name__ == '__main__':
    vp_start_gui()
