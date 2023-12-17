from PyQt5.QtWidgets import QMainWindow, QMessageBox,QLabel,QRadioButton,QVBoxLayout,QHBoxLayout,QLineEdit,QSpacerItem,QPushButton,QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette, QBrush, QPixmap, QRadialGradient,QFont
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5 import QtCore,uic
import traceback
# from game import Gomoku
from corner_widget import CornerWidget
from my_system import GameManager


def run_with_exc(f):
    """游戏运行出现错误时，用messagebox把错误信息显示出来"""
    def call(window, *args, **kwargs):
        try:
            return f(window, *args, **kwargs)
        except Exception:
            exc_info = traceback.format_exc()
            QMessageBox.about(window, '错误信息', exc_info)
    return call


class MyWindow(QMainWindow):

    def __init__(self,game_manager):
        super().__init__()
        self.init_ui()  # 初始化游戏界面
        self.game_manager=game_manager# 初始化游戏内容

    def init_ui(self):

        # 1. 确定游戏界面的标题，大小和背景颜色
        self.setObjectName('MainWindow')
        self.setWindowTitle('棋类对战平台')
        self.setFixedSize(1200, 800)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/bg.jpg').scaled(self.size())))
        self.setPalette(palette)
        # 2. 放置封面棋类图片
        cover_label= QLabel(self)
        cover_pixmap=QPixmap('imgs/cover.png')
        cover_label.setPixmap(cover_pixmap)
        cover_label.setGeometry(50,0,800,800)

        # 3. 放置游戏类型button
        type_label=QLabel(self)
        type_label.setText("游戏类型")
        font_28 = QFont()
        font_28.setPointSize(28)  # 设置字体大小为16
        type_label.setFont(font_28)
        font_20=QFont()
        font_20.setPointSize(20)
        radio_button1 = QRadioButton("五子棋", self)
        radio_button1.setObjectName('option1')
        radio_button1.setFont(font_20)
        radio_button2 = QRadioButton("围棋", self)
        radio_button2.setObjectName('option2')
        radio_button2.setFont(font_20)

        game_type_layout = QVBoxLayout()
        game_type_layout.addWidget(type_label)
        game_type_layout.addWidget(radio_button1)
        game_type_layout.addWidget(radio_button2)
        game_type_layout.setGeometry(QtCore.QRect(700, 150, 200, 100))
        radio_button1.setChecked(True)
        self.setLayout(game_type_layout)

        # 4. 放置棋盘大小输入框
        size_label = QLabel(self)
        size_label.setText("棋盘大小：\n""(输入8到19的整数):")
        size_label.setFont(font_20)
        size_spacer=QSpacerItem(20,20)
        size_line_edit=QLineEdit(self)
        size_line_edit.setObjectName('map_size')

        game_size_layout = QHBoxLayout()
        game_size_layout.addWidget(size_label)
        game_size_layout.addItem(size_spacer)
        game_size_layout.addWidget(size_line_edit)
        game_size_layout.setGeometry(QtCore.QRect(700, 300, 400, 80))
        size_line_edit.setFixedSize(50,40)
        size_line_edit.setText("19")
        self.setLayout(game_size_layout)

        # 4. 放置开始游戏的button
        start_button = QPushButton(self)
        start_button.setText("开始游戏")
        start_button.setFont(font_28)
        start_button.setGeometry(QtCore.QRect(700, 450, 400, 200))
        # 设置槽函数
        start_button.clicked.connect(self.startGame)

        self.show()
    def clearWindow(self):
        # 删除窗口上的所有小部件
        for widget in self.findChildren(QWidget):
            widget.deleteLater()
        # 删去之前的window
        self.close()
    def startGame(self):
        # 确定游戏类型
        # 得到目前的游戏类型以及棋盘大小数据
        option1=self.findChild(QWidget,name='option1')
        if option1.isChecked():
            game_type='gomoku'
        else:
            game_type='go'
        # 确定棋盘大小
        map_size = int(self.findChild(QWidget, name='map_size').text())
        self.clearWindow()
        self.game_manager.start_game(game_type,map_size)
        self.init_game()
    def init_game(self):
        self.last_pos = (-1, -1)
        self.operate_status = 0  # 游戏操作状态。0为游戏中（可操作），1为游戏结束（不可操作）
        self.init_game_ui()
    def init_game_ui(self):
        """初始化五子棋游戏界面"""
        # 1. 确定游戏界面的标题，大小和背景颜色
        self.setObjectName('MainWindow')
        self.setWindowTitle('五子棋')
        self.setFixedSize(1200, 800)
        # self.setStyleSheet('#MainWindow{background-color: green}')
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/bg.jpg').scaled(self.size())))
        self.setPalette(palette)

        # 2. 开启鼠标位置的追踪。并在鼠标位置移动时，使用特殊符号标记当前的位置
        self.setMouseTracking(True)
        # 3. 鼠标位置移动时，对鼠标位置的特殊标记
        self.corner_widget = CornerWidget(self)
        self.corner_widget.repaint()
        self.corner_widget.hide()

        # 设置玩家的菜单栏
        # 当前操作玩家,这个是全局变量，每次操作都要修改
        self.now_player_info=QLabel(self)
        self.now_player_info.setText("当前玩家："+self.game_manager.game_state.players[self.game_manager.game_state.current_player_index].name)
        font_20=QFont()
        font_20.setPointSize(20)
        self.now_player_info.setFont(font_20)
        self.now_player_info.setStyleSheet("color:white;")
        self.now_player_info.setObjectName('now_palyer_info')
        self.now_player_info.setGeometry(800,100,300,50)
        # player1的菜单栏
        player1_name=QLabel(self)
        player1_name.setText("玩家："+self.game_manager.game_state.players[0].name)
        player1_name.setFont(font_20)
        player1_name.setGeometry(800,200,200,50)
        # pass,认输和隐藏显示button
        player1_pass_button=QPushButton(self)
        player1_pass_button.setText("pass")
        player1_pass_button.clicked.connect(self.player1PassMove)
        player1_surrender_button=QPushButton(self)
        player1_surrender_button.setText("认输")
        player1_surrender_button.clicked.connect(self.player1Surrender)
        # player1_hidden_button=QPushButton(self)
        # player1_hidden_button.setText("隐藏显示")
        # player1_hidden_button.clicked.connect(self.player1Hidden)
        player1_button_layout = QHBoxLayout()
        player1_button_layout.addWidget(player1_pass_button)
        player1_button_layout.addWidget(player1_surrender_button)
        # player1_button_layout.addWidget(player1_hidden_button)
        player1_button_layout.setGeometry(QtCore.QRect(800, 230, 300, 80))
        self.setLayout(player1_button_layout)

        # player2的菜单栏
        player2_name = QLabel(self)
        player2_name.setText("玩家：" + self.game_manager.game_state.players[1].name)
        player2_name.setFont(font_20)
        player2_name.setGeometry(800, 300, 200, 50)
        # pass,认输和隐藏显示button
        player2_pass_button = QPushButton(self)
        player2_pass_button.setText("pass")
        player2_pass_button.clicked.connect(self.player2PassMove)
        player2_surrender_button = QPushButton(self)
        player2_surrender_button.setText("认输")
        player2_surrender_button.clicked.connect(self.player2Surrender)
        # player2_hidden_button = QPushButton(self)
        # player2_hidden_button.setText("隐藏显示")
        # player2_hidden_button.clicked.connect(self.player2Hidden)
        player2_button_layout = QHBoxLayout()
        player2_button_layout.addWidget(player2_pass_button)
        player2_button_layout.addWidget(player2_surrender_button)
        # player2_button_layout.addWidget(player2_hidden_button)
        player2_button_layout.setGeometry(QtCore.QRect(800, 330, 300, 80))
        self.setLayout(player2_button_layout)

        # 悔棋,保存,读档按钮
        undo_move_button=QPushButton(self)
        undo_move_button.setText("悔棋")
        undo_move_button.clicked.connect(self.undoMove)
        save_button=QPushButton(self)
        save_button.setText("保存")
        save_button.clicked.connect(self.save)
        load_button=QPushButton(self)
        load_button.setText("读档")
        load_button.clicked.connect(self.load)
        memory_button_layout = QHBoxLayout()
        memory_button_layout.addWidget(undo_move_button)
        memory_button_layout.addWidget(save_button)
        memory_button_layout.addWidget(load_button)
        undo_move_button.setFixedHeight(60)
        save_button.setFixedHeight(60)
        load_button.setFixedHeight(60)
        memory_button_layout.setGeometry(QtCore.QRect(800, 450, 300, 60))

        # 终局的按钮
        end_game_button=QPushButton(self)
        end_game_button.setText("终局")
        end_game_button.clicked.connect(self.endGame)
        end_game_button.setGeometry(QtCore.QRect(800, 550, 300, 80))

        # 重新开始的按钮
        restart_game_button = QPushButton(self)
        restart_game_button.setText("重新开始")
        restart_game_button.clicked.connect(self.restartGame)
        restart_game_button.setGeometry(QtCore.QRect(800, 650, 300, 100))

        # 5. 显示初始化的游戏界面
        self.show()
    # 设置一系列的槽函数
    def player1PassMove(self):
        if self.game_manager.game_state.game_type == 'go':
            if self.game_manager.game_state.current_player_index == 0:
                self.game_manager.pass_1step()
            else:
                QMessageBox.about(self, '错误', "现在是玩家2的回合，请误操作")
        else:
            QMessageBox.about(self, '错误', "只有围棋才能pass")
    def player2PassMove(self):
        if self.game_manager.game_state.game_type == 'go':
            if self.game_manager.game_state.current_player_index == 1:
                # 不下棋就直接切换角色即可
                self.game_manager.pass_1step()
            else:
                QMessageBox.about(self, '错误', "现在是玩家1的回合，请误操作")
        else:
            QMessageBox.about(self, '错误', "只有围棋才能pass")
    def player1Surrender(self):
        if self.game_manager.game_state.current_player_index == 0:
            self.game_manager.surrenderGame(self.game_manager.game_state.players[0])
            self.repaint(0, 0, 650, 650)
            self.operate_status = 1
            QMessageBox.about(self, '游戏结束', '玩家' + self.game_manager.game_state.winner.name + '获胜!')
        else:
            QMessageBox.about(self, '错误',"现在是玩家2的回合，请误操作")
    def player2Surrender(self):
        if self.game_manager.game_state.current_player_index == 1:
            self.game_manager.surrenderGame(self.game_manager.game_state.players[1])
            self.repaint(0, 0, 650, 650)
            self.operate_status = 1
            QMessageBox.about(self, '游戏结束', '玩家' + self.game_manager.game_state.winner.name + '获胜!')
        else:
            QMessageBox.about(self,'错误', "现在是玩家1的回合，请误操作")
    # def player1Hidden(self):
    #     pass
    # def player2Hidden(self):
    #     pass
    def undoMove(self):
        self.game_manager.undo()
        self.repaint()
    def save(self):
        self.game_manager.save()

    def load(self):
        self.game_manager.load()
        self.repaint()
    def endGame(self):
        if self.game_manager.game_state.game_type == 'go':
            self.game_manager.endGame()
        else:
            QMessageBox.about(self, '错误', "只有围棋才能中途结束游戏")
    def restartGame(self):
        self.game_manager.game_state.restartGame()
        self.clearWindow()
        self.init_ui()
    @run_with_exc
    def paintEvent(self, e):
        """绘制游戏内容"""

        def draw_map():
            """绘制棋盘"""
            qp.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidLine))  # 棋盘的颜色为黑色
            # 绘制横线
            for x in range(self.game_manager.game_state.map_size):
                map_distance=(self.game_manager.game_state.MAX_MAP_SIZE -  self.game_manager.game_state.map_size)/2*40
                pos=[40 * (x + 1), 40, 40 * (x + 1), self.game_manager.game_state.map_size*40]
                for i in range(len(pos)):
                    pos[i]+=map_distance
                qp.drawLine(*tuple(pos))
            # 绘制竖线
            for y in range(self.game_manager.game_state.map_size):
                map_distance = (self.game_manager.game_state.MAX_MAP_SIZE - self.game_manager.game_state.map_size) / 2 * 40
                pos = [40, 40 * (y + 1), self.game_manager.game_state.map_size*40, 40 * (y + 1)]
                for i in range(len(pos)):
                    pos[i]+=map_distance
                qp.drawLine(*tuple(pos))
            # 绘制棋盘中的黑点
            # qp.setBrush(QColor(0, 0, 0))
            # key_points = [(4, 4), (12, 4), (4, 12), (12, 12), (8, 8)]
            # for t in key_points:
            #     qp.drawEllipse(QPoint(40 * t[0], 40 * t[1]), 5, 5)

        def draw_pieces():
            """绘制棋子"""
            # 绘制黑棋子
            qp.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            # qp.setBrush(QColor(0, 0, 0))
            for x in range(self.game_manager.game_state.map_size):
                for y in range(self.game_manager.game_state.map_size):
                    if self.game_manager.game_state.board[x][y] == 1:
                        map_distance = (self.game_manager.game_state.MAX_MAP_SIZE - self.game_manager.game_state.map_size) / 2 * 40
                        pos = [40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35]
                        for i in range(len(pos)):
                            pos[i] += map_distance
                        radial = QRadialGradient(*tuple(pos))  # 棋子的渐变效果
                        radial.setColorAt(0, QColor(96, 96, 96))
                        radial.setColorAt(1, QColor(0, 0, 0))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(int(40 * (x + 1) + map_distance), int(40 * (y + 1)) + map_distance), 15, 15)#只有前两个坐标需要添加map_distance
            # 绘制白棋子
            qp.setPen(QPen(QColor(160, 160, 160), 1, Qt.SolidLine))
            # qp.setBrush(QColor(255, 255, 255))
            for x in range(self.game_manager.game_state.map_size):
                for y in range(self.game_manager.game_state.map_size):
                    if self.game_manager.game_state.board[x][y] == 2:
                        map_distance = (self.game_manager.game_state.MAX_MAP_SIZE - self.game_manager.game_state.map_size) / 2 * 40
                        pos = [40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35]
                        for i in range(len(pos)):
                            pos[i] += map_distance
                        radial = QRadialGradient(*tuple(pos))  # 棋子的渐变效果
                        radial.setColorAt(0, QColor(255, 255, 255))
                        radial.setColorAt(1, QColor(160, 160, 160))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(int(40 * (x + 1) + map_distance), int(40 * (y + 1)) + map_distance), 15,15)  # 只有前两个坐标需要添加map_distance

        if self.game_manager.game_state!=None:  # 游戏还没开始的话，就不用画了
            qp = QPainter()
            qp.begin(self)
            draw_map()  # 绘制棋盘
            draw_pieces()  # 绘制棋子
            qp.end()

    @run_with_exc
    def mouseMoveEvent(self, e):
        # 1. 首先判断鼠标位置对应棋盘中的哪一个格子
        map_distance = (self.game_manager.game_state.MAX_MAP_SIZE - self.game_manager.game_state.map_size) / 2 * 40
        mouse_x = e.windowPos().x()-map_distance
        mouse_y = e.windowPos().y()-map_distance

        if 25 <= mouse_x <= self.game_manager.game_state.map_size*40+15 and 25 <= mouse_y <= self.game_manager.game_state.map_size*40+15 and (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
            pos_x = int((mouse_x + 15) // 40) - 1
            pos_y = int((mouse_y + 15) // 40) - 1
        else:  # 鼠标当前的位置不对应任何一个游戏格子，将其标记为(01, 01
            pos_x = -1
            pos_y = -1

        # 2. 然后判断鼠标位置较前一时刻是否发生了变化
        pos_change = False  # 标记鼠标位置是否发生了变化
        if pos_x != self.last_pos[0] or pos_y != self.last_pos[1]:
            pos_change = True
        self.last_pos = (pos_x, pos_y)
        # 3. 最后根据鼠标位置的变化，绘制特殊标记
        if pos_change and pos_x != -1:
            self.setCursor(Qt.PointingHandCursor)
        if pos_change and pos_x == -1:
            self.setCursor(Qt.ArrowCursor)
        if pos_change and pos_x != -1:
            self.corner_widget.move(25 + pos_x * 40 + map_distance, 25 + pos_y * 40 + map_distance)
            self.corner_widget.show()

        if pos_change and pos_x == -1:
            self.corner_widget.hide()

    @run_with_exc
    def mousePressEvent(self, e):
        """根据鼠标的动作，确定落子位置"""
        if not (hasattr(self, 'operate_status') and self.operate_status == 0):
            return
        if e.button() == Qt.LeftButton:
            # 1. 首先判断按下了哪个格子
            map_distance = (self.game_manager.game_state.MAX_MAP_SIZE - self.game_manager.game_state.map_size) / 2 * 40
            mouse_x = e.windowPos().x()-map_distance
            mouse_y = e.windowPos().y()-map_distance
            if (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
                pos_x = int((mouse_x + 15) // 40) - 1
                pos_y = int((mouse_y + 15) // 40) - 1
            else:  # 鼠标点击的位置不正确
                return
            # result判断位置是否合法
            judgment=self.game_manager.move_1step( pos_x, pos_y)
            if not judgment:
                return
            # 2. 根据操作结果进行一轮游戏循环
            self.res = self.game_manager.game_state.check_game_over()  # 判断游戏结果
            if self.res != 0:  # 如果游戏结果为“已经结束”，则显示游戏内容，并退出主循环
                self.game_over()
                return
            self.game_manager.next_step()
            # 更改信息栏的信息
            self.now_player_info.setText("当前玩家："+self.game_manager.game_state.players[self.game_manager.game_state.current_player_index].name)
    def game_over(self):
        self.operate_status = 1
        # 1. 显示游戏结束的信息
        if self.res == 1:
            QMessageBox.about(self, '游戏结束', '玩家' + self.game_manager.game_state.winner.name + '获胜!')
        else:
            QMessageBox.about(self, '游戏结束', '平局!')


