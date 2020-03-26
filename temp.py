import tkinter as tk
import tkinter.messagebox 
import pickle
import pandas as pd

window = tk.Tk()
window.title('Plane Wars')
window.geometry('400x700')

canvas = tk.Canvas(window, height=700, width=400)#创建画布
image_file = tk.PhotoImage(file='images/background.png')#加载图片文件
print(1)
image = canvas.create_image(0,0, anchor='nw', image=image_file)#将图片置于画布上
canvas.pack(side='top')#放置画布（为上端）

tk.Label(window, text='User name: ').place(x=50, y= 150)#创建一个`label`名为`User name: `置于坐标（50,150）
tk.Label(window, text='Password: ').place(x=50, y= 190)
var_usr_name = tk.StringVar()#定义变量
var_usr_name.set('example@python.com')#变量赋值'example@python.com'
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)#创建一个`entry`，显示为变量`var_usr_name`即图中的`example@python.com`
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')#`show`这个参数将输入的密码变为`***`的形式
entry_usr_pwd.place(x=160, y=190)

def usr_login(): 
    global usr_name
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
            
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
            
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='Welcome', message='即将开始游戏 ' + usr_name)
            window.destroy()
            
        else:
            tk.messagebox.showerror(message='Error, 您的密码错误，请重试。')
    else:
        is_sign_up = tk.messagebox.askyesno('Welcome','您没有注册. 现在注册吗?')
        if is_sign_up:
            usr_sign_up()
    
def usr_sign_up():
    def sign_to_Python():
          ##以下三行就是获取我们注册时所输入的信息
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            nn = new_name.get()
            with open('usrs_info.pickle', 'rb') as usr_file:
                exist_usr_info = pickle.load(usr_file)
         
         ##这里就是判断，如果两次密码输入不一致，则提示`'Error', 'Password and confirm password must be the same!'`
            if np != npf:
                tk.messagebox.showerror('Error', '两次输入密码不一致!')
          
         ##如果用户名已经在我们的数据文件中，则提示`'Error', 'The user has already signed up!'`
            elif nn in exist_usr_info:
                tk.messagebox.showerror('Error', '此用户已经被注册了!')
    
    
        ##最后如果输入无以上错误，则将注册输入的信息记录到文件当中，并提示注册成功`'Welcome', 'You have successfully signed up!'`
        ##然后销毁窗口。
            else:
                exist_usr_info[nn] = np
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(exist_usr_info, usr_file)
                tk.messagebox.showinfo('Welcome', '你已经成功注册!')
         ##然后销毁窗口。
                window_sign_up.destroy()
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('350x200')
    window_sign_up.title('注册窗口')
    
    new_name = tk.StringVar()#将输入的注册名赋值给变量
    new_name.set('example@python.com')#将最初显示定为'example@python.com'
    tk.Label(window_sign_up, text='User name: ').place(x=10, y= 10)#将`User name:`放置在坐标（10,10）。
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)#创建一个注册名的`entry`，变量为`new_name`
    entry_new_name.place(x=150, y=10)#`entry`放置在坐标（150,10）.


    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)


    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='confirm: ').place(x=10, y= 90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)


    btn_comfirm_sign_up = tk.Button(window_sign_up, text='注册', command=sign_to_Python)
    btn_comfirm_sign_up.place(x=150, y=130)
def record():
    df = pd.read_table('user.txt',names = ['score'],sep=' ')
    DF = df.sort_values(by=['score'],ascending=False)
    print(DF)    
    record_sign_up = tk.Toplevel(window)
    record_sign_up.geometry('200x300')
    record_sign_up.title('查询')
    
    new_pwd_confirm = tk.StringVar()
    tk.Label(record_sign_up, text=str(DF)).place(x=10, y= 10)
# login and sign up button
btn_login = tk.Button(window, text='登录', command=usr_login)#定义一个`button`按钮，名为`Login`,触发命令为`usr_login`
btn_login.place(x=170, y=230)
btn_sign_up = tk.Button(window, text='注册', command=usr_sign_up)
btn_sign_up.place(x=270, y=230)
btn_sign_up = tk.Button(window, text='查询', command=record)
btn_sign_up.place(x=70, y=230)

window.mainloop()
