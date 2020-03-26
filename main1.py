import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
import random
import time
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
start = 0
def usr_login(): 
    global usr_name
    global start
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
            start = 1
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
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y= 90)
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

if start == 0:
    time.sleep(10000000)
pygame.init()
bg_size = width, height = 400, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

background = pygame.image.load("images/background.png").convert()

BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)

#载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.MidEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.BigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc

def main():
    pygame.mixer.music.play(-1)
    
    clock = pygame.time.Clock()

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    me = myplane.MyPlane(bg_size)
    
    enemies = pygame.sprite.Group()

    # 生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 5)

    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 1)

    running = True
    switch_image = True
    delay = 100
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)
    
    bullets = []

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 生命数量
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.ttf", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    DOUBLE_BULLET_TIME = USEREVENT + 1

    # 解除我方飞机无敌状态
    INVINCEBLE_TIME = USEREVENT + 2


    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    # 标记是否使用超级子弹
    is_double_bullet = False

    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    # 每30秒发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 *1000)

    # 阻止重复读取成绩记录文件
    recorded = False

    # 标志是否暂停游戏
    paused = False
    paused_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/resume_pressed.png").convert_alpha()
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width -10, 10
    paused_image = paused_nor_image

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                        paused_image = resume_pressed_image
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        paused_image = pause_pressed_image
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = paused_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if random.choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)
            elif event.type == INVINCEBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCEBLE_TIME, 0)


        # 根据用户的得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 300000:
            level = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        screen.blit(background, (0,0))

        if life_num and not paused:
            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            #发射子弹
            if not(delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 33, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            #检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            
            # 绘制全屏炸弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # 绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, \
                            (each.rect.left, each.rect.top - 5),\
                            (each.rect.right, each.rect.top - 5), \
                            2)
                    
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                            (each.rect.left, each.rect.top -5), \
                            (each.rect.left + each.rect.width * energy_remain, \
                            each.rect.top - 5), \
                            2)

                else:
                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index+1)%6
                        if e3_destroy_index == 0:
                            me_down_sound.stop()
                            score += 10000
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()

                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image1, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, \
                            (each.rect.left, each.rect.top - 5),\
                            (each.rect.right, each.rect.top - 5), \
                            2)
                    
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, \
                            (each.rect.left, each.rect.top -5), \
                            (each.rect.left + each.rect.width * energy_remain, \
                            each.rect.top - 5), \
                            2)
                else:
                    if not(delay % 3):
                        if e2_destroy_index ==0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index+1)%4
                        if e2_destroy_index == 0:
                            score += 5000
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image1, each.rect)
                else:
                    if not(delay % 3):
                        if e1_destroy_index ==0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index+1)%4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()    

            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False

            # 绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                me_down_sound.play()
                if not(delay % 3):
                    screen.blit(each.destroy_images[me_destroy_index], each.rect)
                    me_destroy_index = (me_destroy_index+1)%4
                    # 剩余生命数量
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCEBLE_TIME, 3 * 1000)

             # 绘制剩余炸弹数量
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height-10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))


            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,\
                        (width - 10 - (i+1)*life_rect.width, \
                        height - 10 - life_rect.height))
            
            score_text = score_font.render(str("Score: %s" % score), True, WHITE)
            screen.blit(score_text, (10,5))
        elif life_num == 0:
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)
            
            if not recorded:
                recorded = True
                # 读取历史最高分
                with open("record.txt", "r") as f:
                    record_score = int(f.read())
            
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))
                with open("user.txt", "a") as fe:
                    fe.write(usr_name + ' ' + str(score) + '\n' )

            # 绘制结束画面
            record_score_text = score_font.render("Best: %d" % record_score,True,WHITE)
            screen.blit(record_score_text, (50,50))
            
            gameover_text1 = gameover_font.render("Your Score: ", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                (width - gameover_text1_rect.width) // 2, height // 2
            screen.blit(gameover_text1, gameover_text1_rect)

            
            gameover_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                (width - gameover_text2_rect.width) // 2, \
                                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                        (width - again_rect.width) // 2,\
                        gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                        (width - again_rect.width) // 2, \
                        again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                     pygame.quit()
                     sys.exit()

        screen.blit(paused_image, paused_rect)

        # 切换图片
        if not(delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
    