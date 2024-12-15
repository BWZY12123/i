import pygame
import time
import random

_display = pygame.display
COLOR_BLACK = pygame.Color(0, 0, 0)  # 黑色
COLOR_RED = pygame.Color(255, 0, 0)  # 红色
version = 'v1.25'  # 版本号
IMAGE_SCALE = 0.5  # 图片缩放比例

class MainGame():
    window = None  # 游戏窗口
    SCREEN_HEIGHT = 500  # 窗口高度
    SCREEN_WIDTH = 800  # 窗口宽度
    TANK_P1 = None  # 玩家坦克
    EnemyTank_list = []  # 敌方坦克列表
    EnemTank_count = 5  # 敌方坦克数量
    Bullet_list = []  # 玩家子弹列表
    Enemy_bullet_list = []  # 敌方子弹列表
    Explode_list = []  # 爆炸效果列表
    Wall_list = []  # 墙壁列表
    
    

    def startGame(self):
        pygame.init()  # 初始化 Pygame
        _display.init()
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])  # 设置窗口大小
        print("窗口已打开")  # 调试信息：窗口已打开
        self.creatMyTank()  # 创建玩家坦克
        self.creatEnemyTank()  # 创建敌方坦克
        self.creatWalls()  # 创建墙壁
        _display.set_caption("坦克大战" + version)  # 设置窗口标题

        while True:
            MainGame.window.fill(COLOR_BLACK)  # 填充黑色背景
            self.getEvent()  # 获取事件
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆" % len(MainGame.EnemyTank_list)), (5, 5))  # 显示剩余敌方坦克数量
            self.blitWalls()  # 绘制墙壁
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                MainGame.TANK_P1.displayTank()  # 绘制玩家坦克
            else:
                del MainGame.TANK_P1  # 如果玩家坦克不存在，则删除
                MainGame.TANK_P1 = None
            self.blitEnemyTank()  # 绘制敌方坦克
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()  # 移动玩家坦克
                MainGame.TANK_P1.hitWalls()  # 检测与墙壁的碰撞
                MainGame.TANK_P1.hitEnemyTank()  # 检测与敌方坦克的碰撞
            self.blitBullet()  # 绘制玩家子弹
            self.blitEnemyBullet()  # 绘制敌方子弹
            self.displayExplodes()  # 显示爆炸效果

                    # 检查游戏结束条件
            if len(MainGame.EnemyTank_list) == 0:
                print("所有敌方坦克已被消灭，游戏胜利！")
                self.endGame()  # 结束游戏
            if MainGame.TANK_P1 is None or not MainGame.TANK_P1.live:
                print("玩家坦克被击败，游戏结束！")
                self.endGame()  # 结束游戏

            time.sleep(0.02)  # 控制游戏帧率
            _display.update()  # 更新显示

    def creatMyTank(self):
        MainGame.TANK_P1 = MyTank(400, 300)  # 创建玩家坦克
        music = Music('逆战.mp3')  # 加载音乐
        music.play()  # 播放音乐

    def creatEnemyTank(self):
        top = 100  # 敌方坦克的初始纵坐标
        for i in range(MainGame.EnemTank_count):
            speed = random.randint(3, 6)  # 随机速度
            left = random.randint(1, 7)  # 随机横坐标
            eTank = EnemyTank(left * 100, top, speed)  # 创建敌方坦克
            MainGame.EnemyTank_list.append(eTank)  # 添加到敌方坦克列表

    def creatWalls(self):
        for i in range(6):
            wall = Wall(130 * i, 240)  # 创建墙壁
            MainGame.Wall_list.append(wall)  # 添加到墙壁列表

    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall ()  # 绘制墙壁
            else:
                MainGame.Wall_list.remove(wall)  # 如果墙壁不再存在，则从列表中移除

    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()  # 绘制敌方坦克
                eTank.randMove()  # 随机移动敌方坦克
                eTank.hitWalls()  # 检测与墙壁的碰撞
                eTank.hitMyTank()  # 检测与玩家坦克的碰撞
                eBullet = eTank.shot()  # 敌方坦克发射子弹
                if eBullet:
                    MainGame.Enemy_bullet_list.append(eBullet)  # 添加子弹到敌方子弹列表
            else:
                MainGame.EnemyTank_list.remove(eTank)  # 如果敌方坦克不再存在，则从列表中移除

    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            if bullet.live:
                bullet.displayBullet()  # 绘制玩家子弹
                bullet.bulletMove()  # 移动子弹
                bullet.hitEnemyTank()  # 检测与敌方坦克的碰撞
                bullet.hitWalls()  # 检测与墙壁的碰撞
            else:
                MainGame.Bullet_list.remove(bullet)  # 如果子弹不再存在，则从列表中移除

    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            if eBullet.live:
                eBullet.displayBullet()  # 绘制敌方子弹
                eBullet.bulletMove()  # 移动敌方子弹
                eBullet.hitWalls()  # 检测与墙壁的碰撞
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    eBullet.hitMyTank()  # 检测与玩家坦克的碰撞
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)  # 如果敌方子弹不再存在，则从列表中移除

    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()  # 显示爆炸效果
            else:
                MainGame.Explode_list.remove(explode)  # 如果爆炸效果不再存在，则从列表中移除

    def getEvent(self):
        eventList = pygame.event.get()  # 获取事件列表
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()  # 结束游戏
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not MainGame.TANK_P1:
                    self.creatMyTank()  # 创建玩家坦克
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    if event.key == pygame.K_LEFT:
                        print("坦克向左调头，移动")  # 调试信息：坦克向左移动
                        MainGame.TANK_P1.direction = 'L'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_RIGHT:
                        print("坦克向右调头，移动")  # 调试信息：坦克向右移动
                        MainGame.TANK_P1.direction = 'R'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_UP:
                        print("坦克向上调头，移动")  # 调试信息：坦克向上移动
                        MainGame.TANK_P1.direction = 'U'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_DOWN:
                        print("坦克向下掉头，移动")  # 调试信息：坦克向下移动
                        MainGame.TANK_P1.direction = 'D'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        print("发射子弹")  # 调试信息：发射子弹
                        if len(MainGame.Bullet_list) < 3:
                            m = Bullet(MainGame.TANK_P1)  # 创建子弹
                            MainGame.Bullet_list.append(m)  # 添加子弹到列表
                        else:
                            print("子弹数量不足")  # 调试信息：子弹数量不足
                        print("当前屏幕中的子弹数量为:%d" % len(MainGame.Bullet_list))  # 显示当前子弹数量
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                        MainGame.TANK_P1.stop = True  # 停止坦克移动

    def getTextSurface(self, text):
        pygame.font.init()  # 初始化字体
        font = pygame.font.SysFont('kaiti', 18)  # 设置字体和大小
        textSurface = font.render(text, True, COLOR_RED)  # 渲染文本
        return textSurface

    def endGame(self):
        print("谢谢使用")  # 调试信息：游戏结束
        pygame.quit()  # 确保 Pygame 正常退出
        exit()  # 退出程序

class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # 初始化基类

class Tank(BaseItem):
    def __init__(self, left, top):
        self.images = {
            'U': pygame.transform.scale(pygame.image.load('上.png'), (50, 50)),  # 向上图片
            'D': pygame.transform.scale(pygame.image.load('下.png'), (50, 50)),  # 向下图片
            'L': pygame.transform.scale(pygame.image.load('左.png'), (50, 50)),  # 向左图片
            'R': pygame.transform.scale(pygame.image.load('右.png'), (50, 50))   # 向右图片
        }
        self.direction = 'U'  # 初始方向为上
        self.image = self.images[self.direction]  # 设置初始图片
        self.rect = self.image.get_rect()  # 获取图片矩形区域
        self.rect.left = left  # 设置横坐标
        self.rect.top = top  # 设置纵坐标
        self.speed = 5  # 移动速度
        self.stop = True  # 停止状态
        self.live = True  # 存活状态
        self.oldLeft = self.rect.left  # 记录旧的横坐标
        self.oldTop = self.rect.top  # 记录旧的纵坐标

    def move(self):
        self.oldLeft = self.rect.left  # 记录当前横坐标
        self.oldTop = self.rect.top  # 记录当前纵坐标
        if self.direction == 'L' and self.rect.left > 0:
            self.rect.left -= self.speed  # 向左移动
        elif self.direction == 'R' and self.rect.left + self.rect.width < MainGame.SCREEN_WIDTH:
            self.rect.left += self.speed  # 向右移动
        elif self.direction == 'U' and self.rect.top > 0:
            self.rect.top -= self.speed  # 向上移动
        elif self.direction == 'D' and self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
            self.rect.top += self.speed  # 向下移动

    def stay(self):
        self.rect.left = self.oldLeft  # 恢复到旧的横坐标
        self.rect.top = self.oldTop  # 恢复到旧的纵坐标

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):  # 检测与墙壁的碰撞
                self.stay()  # 碰撞时恢复位置

    def shot(self):
        return Bullet(self)  # 发射子弹

    def displayTank(self):
        self.image = self.images[self.direction]  # 根据方向更新坦克图片
        MainGame.window.blit(self.image, self.rect)  # 绘制坦克

class MyTank(Tank):
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)  # 调用父类构造函数

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):  # 检测与敌方坦克的碰撞
                self.stay()  # 碰撞时恢复位置

class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)  # 调用父类构造函数
        self.images = {
            'U': pygame.transform.scale(pygame.image.load('上.png'), (50, 50)), 'D': pygame.transform.scale(pygame.image.load('下.png'), (50, 50)),  # 向下图片
            'L': pygame.transform.scale(pygame.image.load('左.png'), (50, 50)),  # 向左图片
            'R': pygame.transform.scale(pygame.image.load('右.png'), (50, 50))   # 向右图片
        }
        self.direction = self.randDirection()  # 随机方向
        self.image = self.images[self.direction]  # 设置初始图片
        self.rect = self.image.get_rect()  # 获取图片矩形区域
        self.rect.left = left  # 设置横坐标
        self.rect.top = top  # 设置纵坐标
        self.speed = speed  # 设置速度
        self.stop = True  # 停止状态
        self.step = 30  # 移动步数

    def randDirection(self):
        num = random.randint(1, 4)  # 随机生成方向
        if num == 1:
            return 'U'  # 向上
        elif num == 2:
            return 'D'  # 向下
        elif num == 3:
            return 'L'  # 向左
        elif num == 4:
            return 'R'  # 向右

    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()  # 随机改变方向
            self.step = 50  # 重置步数
        else:
            self.move()  # 移动
            self.step -= 1  # 减少步数

    def shot(self):
        num = random.randint(1, 1000)  # 随机决定是否发射子弹
        if num <= 20:
            return Bullet(self)  # 发射子弹

    def hitMyTank(self):
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
            if pygame.sprite.collide_rect(self, MainGame.TANK_P1):  # 检测与玩家坦克的碰撞
                self.stay()  # 碰撞时恢复位置

class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.transform.scale(pygame.image.load('zd.png'), (10, 10))  # 加载并缩放子弹图片
        self.direction = tank.direction  # 设置子弹方向
        self.rect = self.image.get_rect()  # 获取子弹矩形区域
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2  # 设置子弹初始位置
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        self.speed = 7  # 设置子弹速度
        self.live = True  # 存活状态

    def bulletMove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed  # 向上移动
            else:
                self.live = False  # 超出边界，子弹消失
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed  # 向下移动
            else:
                self.live = False  # 超出边界，子弹消失
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed  # 向左移动
            else:
                self.live = False  # 超出边界，子弹消失
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed  # 向右移动
            else:
                self.live = False  # 超出边界，子弹消失
                

    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)  # 绘制子弹

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):  # 检测与敌方坦克的碰撞
                explode = Explode(eTank)  # 创建爆炸效果
                MainGame.Explode_list.append(explode)  # 添加到爆炸效果列表
                self.live = False  # 子弹消失
                eTank.live = False  # 敌方坦克消失

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):  # 检测与玩家坦克的碰撞
            explode = Explode(MainGame.TANK_P1)  # 创建爆炸效果
            MainGame.Explode_list.append(explode)  # 添加到爆炸效果列表
            self.live = False  # 子弹消失
            MainGame.TANK_P1.live = False  # 玩家坦克消失

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):  # 检测与墙壁的碰撞
                self.live = False  # 子弹消失
                wall.hp -= 1  # 墙壁生命值减少
                if wall.hp <= 0:
                    wall.live = False  # 墙壁消失

class Explode():
    def __init__(self, tank):
        self.rect = tank.rect  # 设置爆炸位置
        self.step = 0  # 当前帧数
        self.images = [
            pygame.image.load('1.png'),  # 爆炸帧0
            pygame.image.load('2.png'),  # 爆炸帧1
            pygame.image.load('3.png'),  # 爆炸帧2
            pygame.image.load('4.png'),  # 爆炸帧3
            pygame.image.load('5.png')   # 爆炸帧4
        ]
        self.image = self.images[self.step]  # 设置初始爆炸图片
        self.live = True  # 存活状态

    def displayExplode(self):
        if self.step < len(self.images):  # 如果还有帧未显示
            MainGame.window.blit(self.image, self.rect)  # 绘制爆炸效果
            self.image = self.images[self.step]  # 更新爆炸图片
            self.step += 1  # 增加帧数
        else:
            self.live = False  # 爆炸效果结束
            self.step = 0  # 重置帧数

class Wall():
    def __init__(self, left, top):
        self.image = pygame.transform.scale(pygame.image.load('q.png'), (50, 50))  # 加载并缩放墙壁图片
        self.rect = self.image.get_rect()  # 获取墙壁矩形区域
        self.rect.left = left  # 设置横坐标
        self.rect.top = top  # 设置纵坐标
        self.live = True  # 存活状态
        self.hp = 3  # 生命值

    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)  # 绘制墙壁

class Music():
    def __init__(self, fileName):
        self.fileName = fileName  # 音乐文件名
        pygame.mixer.init()  # 初始化音频
        pygame.mixer.music.load(self.fileName)  # 加载音乐文件

    def play(self):
        pygame.mixer.music.play()  # 播放音乐

MainGame().startGame()  # 启动游戏
import pygame
import time
import random

_display = pygame.display
COLOR_BLACK = pygame.Color(0, 0, 0)  # 黑色
COLOR_RED = pygame.Color(255, 0, 0)  # 红色
version = 'v1.25'  # 版本号
IMAGE_SCALE = 0.5  # 图片缩放比例

class MainGame():
    window = None  # 游戏窗口
    SCREEN_HEIGHT = 500  # 窗口高度
    SCREEN_WIDTH = 800  # 窗口宽度
    TANK_P1 = None  # 玩家坦克
    EnemyTank_list = []  # 敌方坦克列表
    EnemTank_count = 5  # 敌方坦克数量
    Bullet_list = []  # 玩家子弹列表
    Enemy_bullet_list = []  # 敌方子弹列表
    Explode_list = []  # 爆炸效果列表
    Wall_list = []  # 墙壁列表
    

    def startGame(self):
        pygame.init()  # 初始化 Pygame
        _display.init()
        MainGame.window = _display.set_mode([MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT])  # 设置窗口大小
        print("窗口已打开")  # 调试信息：窗口已打开
        self.creatMyTank()  # 创建玩家坦克
        self.creatEnemyTank()  # 创建敌方坦克
        self.creatWalls()  # 创建墙壁
        _display.set_caption("坦克大战" + version)  # 设置窗口标题

        while True:
            MainGame.window.fill(COLOR_BLACK)  # 填充黑色背景
            self.getEvent()  # 获取事件
            MainGame.window.blit(self.getTextSurface("剩余敌方坦克%d辆" % len(MainGame.EnemyTank_list)), (5, 5))  # 显示剩余敌方坦克数量
            self.blitWalls()  # 绘制墙壁
            if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                MainGame.TANK_P1.displayTank()  # 绘制玩家坦克
            else:
                del MainGame.TANK_P1  # 如果玩家坦克不存在，则删除
                MainGame.TANK_P1 = None
            self.blitEnemyTank()  # 绘制敌方坦克
            if MainGame.TANK_P1 and not MainGame.TANK_P1.stop:
                MainGame.TANK_P1.move()  # 移动玩家坦克
                MainGame.TANK_P1.hitWalls()  # 检测与墙壁的碰撞
                MainGame.TANK_P1.hitEnemyTank()  # 检测与敌方坦克的碰撞
            self.blitBullet()  # 绘制玩家子弹
            self.blitEnemyBullet()  # 绘制敌方子弹
            self.displayExplodes()  # 显示爆炸效果
            time.sleep(0.02)  # 控制游戏帧率
            _display.update()  # 更新显示

    def creatMyTank(self):
        MainGame.TANK_P1 = MyTank(400, 300)  # 创建玩家坦克
        music = Music('逆战.mp3')  # 加载音乐
        music.play()  # 播放音乐

    def creatEnemyTank(self):
        top = 100  # 敌方坦克的初始纵坐标
        for i in range(MainGame.EnemTank_count):
            speed = random.randint(3, 6)  # 随机速度
            left = random.randint(1, 7)  # 随机横坐标
            eTank = EnemyTank(left * 100, top, speed)  # 创建敌方坦克
            MainGame.EnemyTank_list.append(eTank)  # 添加到敌方坦克列表

    def creatWalls(self):
        for i in range(6):
            wall = Wall(130 * i, 240)  # 创建墙壁
            MainGame.Wall_list.append(wall)  # 添加到墙壁列表

    def blitWalls(self):
        for wall in MainGame.Wall_list:
            if wall.live:
                wall.displayWall()  # 绘制墙壁
            else:
                MainGame .Wall_list.remove(wall)  # 如果墙壁不再存在，则从列表中移除

    def blitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if eTank.live:
                eTank.displayTank()  # 绘制敌方坦克
                eTank.randMove()  # 随机移动敌方坦克
                eTank.hitWalls()  # 检测与墙壁的碰撞
                eTank.hitMyTank()  # 检测与玩家坦克的碰撞
                eBullet = eTank.shot()  # 敌方坦克发射子弹
                if eBullet:
                    MainGame.Enemy_bullet_list.append(eBullet)  # 添加子弹到敌方子弹列表
            else:
                MainGame.EnemyTank_list.remove(eTank)  # 如果敌方坦克不再存在，则从列表中移除

    def blitBullet(self):
        for bullet in MainGame.Bullet_list:
            if bullet.live:
                bullet.displayBullet()  # 绘制玩家子弹
                bullet.bulletMove()  # 移动子弹
                bullet.hitEnemyTank()  # 检测与敌方坦克的碰撞
                bullet.hitWalls()  # 检测与墙壁的碰撞
            else:
                MainGame.Bullet_list.remove(bullet)  # 如果子弹不再存在，则从列表中移除

    def blitEnemyBullet(self):
        for eBullet in MainGame.Enemy_bullet_list:
            if eBullet.live:
                eBullet.displayBullet()  # 绘制敌方子弹
                eBullet.bulletMove()  # 移动敌方子弹
                eBullet.hitWalls()  # 检测与墙壁的碰撞
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    eBullet.hitMyTank()  # 检测与玩家坦克的碰撞
            else:
                MainGame.Enemy_bullet_list.remove(eBullet)  # 如果敌方子弹不再存在，则从列表中移除

    def displayExplodes(self):
        for explode in MainGame.Explode_list:
            if explode.live:
                explode.displayExplode()  # 显示爆炸效果
            else:
                MainGame.Explode_list.remove(explode)  # 如果爆炸效果不再存在，则从列表中移除

    def getEvent(self):
        eventList = pygame.event.get()  # 获取事件列表
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()  # 结束游戏
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not MainGame.TANK_P1:
                    self.creatMyTank()  # 创建玩家坦克
                if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                    if event.key == pygame.K_LEFT:
                        print("坦克向左调头，移动")  # 调试信息：坦克向左移动
                        MainGame.TANK_P1.direction = 'L'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_RIGHT:
                        print("坦克向右调头，移动")  # 调试信息：坦克向右移动
                        MainGame.TANK_P1.direction = 'R'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_UP:
                        print("坦克向上调头，移动")  # 调试信息：坦克向上移动
                        MainGame.TANK_P1.direction = 'U'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_DOWN:
                        print("坦克向下掉头，移动")  # 调试信息：坦克向下移动
                        MainGame.TANK_P1.direction = 'D'
                        MainGame.TANK_P1.stop = False
                    elif event.key == pygame.K_SPACE:
                        print("发射子弹")  # 调试信息：发射子弹
                        if len(MainGame.Bullet_list) < 3:
                            m = Bullet(MainGame.TANK_P1)  # 创建子弹
                            MainGame.Bullet_list.append(m)  # 添加子弹到列表
                        else:
                            print("子弹数量不足")  # 调试信息：子弹数量不足
                        print("当前屏幕中的子弹数量为:%d" % len(MainGame.Bullet_list))  # 显示当前子弹数量
            if event.type == pygame.KEYUP:
                if event.key in [ pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    if MainGame.TANK_P1 and MainGame.TANK_P1.live:
                        MainGame.TANK_P1.stop = True  # 停止坦克移动

    def getTextSurface(self, text):
        pygame.font.init()  # 初始化字体
        font = pygame.font.SysFont('kaiti', 18)  # 设置字体和大小
        textSurface = font.render(text, True, COLOR_RED)  # 渲染文本
        return textSurface

    def endGame(self):
        print("谢谢使用")  # 调试信息：游戏结束
        pygame.quit()  # 确保 Pygame 正常退出
        exit()  # 退出程序

class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # 初始化基类

class Tank(BaseItem):
    def __init__(self, left, top):
        self.images = {
            'U': pygame.transform.scale(pygame.image.load('上.png'), (50, 50)),  # 向上图片
            'D': pygame.transform.scale(pygame.image.load('下.png'), (50, 50)),  # 向下图片
            'L': pygame.transform.scale(pygame.image.load('左.png'), (50, 50)),  # 向左图片
            'R': pygame.transform.scale(pygame.image.load('右.png'), (50, 50))   # 向右图片
        }
        self.direction = 'U'  # 初始方向为上
        self.image = self.images[self.direction]  # 设置初始图片
        self.rect = self.image.get_rect()  # 获取图片矩形区域
        self.rect.left = left  # 设置横坐标
        self.rect.top = top  # 设置纵坐标
        self.speed = 5  # 移动速度
        self.stop = True  # 停止状态
        self.live = True  # 存活状态
        self.oldLeft = self.rect.left  # 记录旧的横坐标
        self.oldTop = self.rect.top  # 记录旧的纵坐标

    def move(self):
        self.oldLeft = self.rect.left  # 记录当前横坐标
        self.oldTop = self.rect.top  # 记录当前纵坐标
        if self.direction == 'L' and self.rect.left > 0:
            self.rect.left -= self.speed  # 向左移动
        elif self.direction == 'R' and self.rect.left + self.rect.width < MainGame.SCREEN_WIDTH:
            self.rect.left += self.speed  # 向右移动
        elif self.direction == 'U' and self.rect.top > 0:
            self.rect.top -= self.speed  # 向上移动
        elif self.direction == 'D' and self.rect.top + self.rect.height < MainGame.SCREEN_HEIGHT:
            self.rect.top += self.speed  # 向下移动

    def stay(self):
        self.rect.left = self.oldLeft  # 恢复到旧的横坐标
        self.rect.top = self.oldTop  # 恢复到旧的纵坐标

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):  # 检测与墙壁的碰撞
                self.stay()  # 碰撞时恢复位置

    def shot(self):
        return Bullet(self)
  # 发射子弹

    def displayTank(self):
        self.image = self.images[self.direction]  # 根据方向更新坦克图片
        MainGame.window.blit(self.image, self.rect)  # 绘制坦克

class MyTank(Tank):
    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)  # 调用父类构造函数

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):  # 检测与敌方坦克的碰撞
                self.stay()  # 碰撞时恢复位置

class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        super(EnemyTank, self).__init__(left, top)  # 调用父类构造函数
        self.images = {
            'U': pygame.transform.scale(pygame.image.load('上.png'), (50, 50)),  # 向上图片
            'D': pygame.transform.scale(pygame.image.load('下.png'), (50, 50)),  # 向下图片
            'L': pygame.transform.scale(pygame.image.load('左.png'), (50, 50)),  # 向左图片
            'R': pygame.transform.scale(pygame.image.load('右.png'), (50, 50))   # 向右图片
        }
        self.direction = self.randDirection()  # 随机方向
        self.image = self.images[self.direction]  # 设置初始图片
        self.rect = self.image.get_rect()  # 获取图片矩形区域
        self.rect.left = left  # 设置横坐标
        self.rect.top = top  # 设置纵坐标
        self.speed = speed  # 设置速度
        self.stop = True  # 停止状态
        self.step = 30  # 移动步数

    def randDirection(self):
        num = random.randint(1, 4)  # 随机生成方向
        if num == 1:
            return 'U'  # 向上
        elif num == 2:
            return 'D'  # 向下
        elif num == 3:
            return 'L'  # 向左
        elif num == 4:
            return 'R'  # 向右

    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()  # 随机改变方向
            self.step = 50  # 重置步数
        else:
            self.move()  # 移动
            self.step -= 1  # 减少步数

    def shot(self):
        num = random.randint(1, 1000)  # 随机决定是否发射子弹
        if num <= 20:
            return Bullet(self)  # 发射子弹

    def hitMyTank(self):
        if MainGame.TANK_P1 and MainGame.TANK_P1.live:
            if pygame.sprite.collide_rect(self, MainGame.TANK_P1):  # 检测与玩家坦克的碰撞
                self.stay()  # 碰撞时恢复位置

class Bullet(BaseItem):
    def __init__(self, tank):
        self.image = pygame.transform.scale(pygame.image.load('zd.png'), (10, 10))  # 加载并缩放子弹图片
        self.direction = tank.direction  # 设置子弹方向
        self.rect = self.image.get_rect()  # 获取子弹矩形区域
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2  # 设置子弹初始位置
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        self.speed = 7  # 设置子弹速度
        self.live = True  # 存活状态

    def bulletMove(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed  # 向上移动
            else:
                self.live = False  # 超出边界，子弹消失
        elif self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed  # 向下移动
            else:
                self.live = False  # 超出边界，子弹消失
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed  # 向左移动
            else:
                self.live = False  # 超出边界，子弹消失
        elif self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed  # 向右移动
            else:
                self.live = False  # 超出边界，子弹消失

    def displayBullet(self):
        MainGame.window.blit(self.image, self.rect)  # 绘制子弹

    def hitEnemyTank(self):
        for eTank in MainGame.EnemyTank_list:
            if pygame.sprite.collide_rect(eTank, self):  # 检测与敌方坦克的碰撞
                explode = Explode(eTank)  # 创建爆炸效果
                MainGame.Explode_list.append(explode)  # 添加到爆炸效果列表
                self.live = False  # 子弹消失
                eTank.live = False  # 敌方坦克消失

    def hitMyTank(self):
        if pygame.sprite.collide_rect(self, MainGame.TANK_P1):  # 检测与玩家坦克的碰撞
            explode = Explode(MainGame.TANK_P1)  # 创建爆炸效果
            MainGame.Explode_list.append(explode)  # 添加到爆炸效果列表
            self.live = False  # 子弹消失
            MainGame.TANK_P1.live = False  # 玩家坦克消失

    def hitWalls(self):
        for wall in MainGame.Wall_list:
            if pygame.sprite.collide_rect(wall, self):  # 检测与墙壁的碰撞
                self.live = False  # 子弹消失
                wall.hp -= 1  # 墙壁生命值减少
                if wall.hp <= 0:
                    wall.live = False  # 墙壁消失

class Explode():
    def __init__(self, tank):
        self.rect = tank.rect  # 设置爆炸位置
        self.step = 0  # 当前帧数
        self.images = [
            pygame.image.load('1.png'),  # 爆炸帧0
            pygame.image.load('2.png'),  # 爆炸帧1
            pygame.image.load('3.png'),  # 爆炸帧2
            pygame.image.load('4.png'),  # 爆炸帧3
            pygame.image.load('5.png')   # 爆炸帧4
        ]
        self.image = self.images[self.step]  # 设置初始爆炸图片
        self.live = True  # 存活状态

    def displayExplode(self):
        if self.step < len(self.images):  # 如果还有帧未显示
            MainGame.window.blit(self.image, self.rect)  # 绘制爆炸效果
            self.image = self.images[self.step]  # 更新爆炸图片
            self.step += 1  # 增加帧数
        else:
            self.live = False  # 爆炸效果结束
            self.step = 0  # 重置帧数

class Wall():
    def __init__(self, left, top):
        self.image = pygame.transform.scale(pygame.image.load('q.png'), (50, 50))  # 加载并缩放墙壁图片
        self.rect = self.image.get_rect()  # 获取墙壁矩形区域
        self.rect.left = left  # 设置横坐标
        self.rect.top = top  # 设置纵坐标
        self.live = True  # 存活状态
        self.hp = 3  # 生命值

    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)  # 绘制墙壁

class Music():
    def __init__(self, fileName):
        self.fileName = fileName  # 音乐文件名
        pygame.mixer.init()  # 初始化 音频
        pygame.mixer.music.load(self.fileName)  # 加载音乐文件

    def play(self):
        pygame.mixer.music.play()  # 播放音乐

MainGame().startGame()  # 启动游戏
