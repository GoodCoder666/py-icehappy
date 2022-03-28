[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://goodcoder666.github.io/post/license/) ![Python Version](https://img.shields.io/github/pipenv/locked/python-version/metabolize/rq-dashboard-on-heroku)

# py-icehappy：基于Python3+Pygame制作的开心消消乐小游戏

## 项目介绍

首先在此感谢原版项目：[Accright/python3-pygame-icehappy](https://github.com/Accright/python3-pygame-icehappy)

**本项目是原版的改进版**，建议先阅读[原版的README](https://github.com/Accright/python3-pygame-icehappy/blob/master/README.md)再查看或运行源代码，具体改进如下：

1. 整理项目文件，如下：
   - `Tree`、`Element`、`Board`三个类移动到 `sprites.py`
   - `Sounds`类移动到 `sounds.py`
   - **图片、音频分类整理**
   - **清理无用图片**
2. 优化代码，提升性能，**删除无用代码，减少重复调用**
3. 代码整理：**修改变量名、注释改为英文**
4. 修复部分bug

*游戏内容基本没有修改，后续会增加关卡等。*

### 运行方法

注意本程序要求**Python 3.5及以上**，若版本过低请安装新版Python。

打开终端，执行：

```shell
$ pip3 install -r requirements.txt
$ python main.py
```

或者

```shell
$ pip3 install pygame>=2
$ python -m main
```

已测试的操作系统：

- Windows 10/11
- Ubuntu 16.04/20.04
- WSL2 (`Windows Subsystem Linux 2`) Ubuntu 20.04

如您运行时出现任何问题，**欢迎提出Issue！**

### 文件分布

|    文件    |         主要函数名/类名         |                   简介                   |
| :--------: | :------------------------------: | :--------------------------------------: |
|  main.py  |                -                |        主程序入口，控制游戏主循环        |
| manager.py |   `TreeManager`，`Manager`   | 游戏底层逻辑，管理游戏界面显示及音频播放 |
| sprites.py | `Board`，`Element`，`Tree` |   `pygame.sprite.Sprite`精灵的继承类   |
| sounds.py |    `Sounds`，`playSound`    |      存储音频文件路径，控制音频播放      |
