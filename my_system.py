class Player:
    def __init__(self,name):
        self.name=name

# 状态模式：游戏状态
class GameState:
    def __init__(self):
        self.board = None
        self.current_player = None
        self.is_game_over=False
        self.winner = None

    def initialize_game(self):
        # 初始化游戏状态
        map_height = 15
        map_width = 15
        self.board = [[0 for _ in range(map_width)] for _ in range(map_height)]

        # 初始化角色
        self.players = [Player("player1"), Player("player2")]
        self.current_player_piece = 1
        self.current_player = self.players[0]

    def make_move(self, move):
        self.board[move["pos_x"]][move["pos_y"]]=self.current_player_piece #因为index是0/1，因此要+1变成1/2


    def switch_player(self):
        # 切换当前玩家
        self.current_player_piece = 3 - self.current_player_piece # 用3来减，3-1=2；3-2=1
        self.current_player = self.players[1-self.players.index(self.current_player)]

    def check_game_over(self,show=False):
        # 检查游戏是否结束
        """判断游戏的结局。0为游戏进行中，1为玩家获胜，2为电脑获胜，3为平局"""
        # 1. 判断是否横向连续五子
        for x in range(len(self.board[0])-4):
            for y in range(len(self.board)):
                if self.board[x][y] == self.current_player_piece and self.board[x + 1][y] == self.current_player_piece and self.board[x + 2][y] == self.current_player_piece and \
                        self.board[x + 3][y] == self.current_player_piece and self.board[x + 4][y] == self.current_player_piece:
                    self.is_game_over=True
                    self.winner=self.current_player
                    if show:
                        return 1, [(x0, y) for x0 in range(x, x + 5)]
                    else:
                        return 1

        # 2. 判断是否纵向连续五子
        for x in range(len(self.board[0])):
            for y in range(len(self.board)-4):
                if self.board[x][y] == self.current_player_piece and self.board[x][y + 1] == self.current_player_piece and self.board[x][y + 2] == self.current_player_piece and self.board[x][
                    y + 3] == self.current_player_piece and self.board[x][y + 4] == self.current_player_piece:
                    self.is_game_over = True
                    self.winner = self.current_player
                    if show:
                        return 1, [(x, y0) for y0 in range(y, y + 5)]
                    else:
                        return 1

        # 3. 判断是否有左上-右下的连续五子
        for x in range(len(self.board[0])-4):
            for y in range(len(self.board)-4):
                if self.board[x][y] == self.current_player_piece and self.board[x + 1][y + 1] == self.current_player_piece and self.board[x + 2][y + 2] == self.current_player_piece and \
                        self.board[x + 3][y + 3] == self.current_player_piece and self.board[x + 4][y + 4] == self.current_player_piece:
                    self.is_game_over = True
                    self.winner = self.current_player
                    if show:
                        return 1, [(x + t, y + t) for t in range(5)]
                    else:
                        return 1

        # 4. 判断是否有右上-左下的连续五子
        for x in range(len(self.board[0])-4):
            for y in range(len(self.board)-4):
                if self.board[x + 4][y] == self.current_player_piece and self.board[x + 3][y + 1] == self.current_player_piece and self.board[x + 2][y + 2] == self.current_player_piece and \
                        self.board[x + 1][y + 3] == self.current_player_piece and self.board[x][y + 4] == self.current_player_piece:
                    self.is_game_over = True
                    self.winner = self.current_player
                    if show:
                        return 1, [(x + t, y + 4 - t) for t in range(5)]
                    else:
                        return 1

        # 5. 判断是否为平局
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[x][y] == 0:  # 棋盘中还有剩余的格子，不能判断为平局
                    if show:
                        return 0, [(-1, -1)]
                    else:
                        return 0
        self.is_game_over = True
        if show:
            return 2, [(-1, -1)]
        else:
            return 2

    def save_game_state(self):
        # 保存游戏状态
        pass

    def load_game_state(self):
        # 加载游戏状态
        pass

# 观察者模式：游戏状态观察者
class GameStateObserver:
    def update(self, game_state):
        # 处理游戏状态更新
        pass

# 命令模式：游戏操作命令
class GameCommand:
    def execute(self):
        # 执行命令
        pass

    def undo(self):
        # 撤销命令
        pass

# 命令模式：具体的移动命令
class MoveCommand(GameCommand):
    def __init__(self, game_state, move):
        self.game_state = game_state
        self.move = move
        self.previous_state = None

    def execute(self):
        self.previous_state = self.game_state.save_game_state()
        self.game_state.make_move(self.move)

    def undo(self):
        self.game_state.load_game_state(self.previous_state)

    def judge(self):
        if 0 <= self.move["pos_y"] <= len(self.game_state.board) and 0 <= self.move["pos_x"] <= len(self.game_state.board[0]) and self.game_state.board[self.move["pos_x"]][self.move["pos_y"]]==0:
            self.judgment=True
        else:
            self.judgment=False
        return self.judgment


# 迭代器模式：棋盘迭代器
class BoardIterator:
    def __init__(self, board):
        self.board = board
        self.current_index = 0

    def __next__(self):
        if self.current_index >= len(self.board):
            raise StopIteration
        value = self.board[self.current_index]
        self.current_index += 1
        return value

# 棋盘类
class Board:
    def __init__(self):
        self.pieces = []

    def add_piece(self, piece):
        # 在棋盘上添加棋子
        pass

    def create_iterator(self):
        # 创建迭代器
        pass

# 原型模式：棋盘原型
class BoardPrototype:
    def clone(self):
        # 克隆棋盘对象
        pass


# 工厂模式：棋盘工厂
class BoardFactory:
    def create_board(self):
        # 创建棋盘对象
        pass


# 单例模式：游戏管理器
class GameManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        self.game_state = GameState()
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(self.observers.index(observer))

    def notify_observers(self,result):
        # 通知观察者
        pass

    def start_game(self):
        self.game_state.initialize_game()

    def move_1step(self,pos_x, pos_y):
        move={'pos_x':pos_x,'pos_y':pos_y}
        # 处理玩家输入等操作
        # 玩家的移动
        command = MoveCommand(self.game_state, move)
        if command.judge():
            command.execute()
            judgement = True
        else:
            judgement = False
        return judgement
