import copy
import json
class Player:
    def __init__(self,name):
        self.name=name
class PlayerFactory:
    player=None
    def create_player(self):
        # 创建棋盘对象
        pass
# 状态模式：游戏状态
class GameState:
    def __init__(self):
        self.board = None
        self.board_size=None
        self.MAX_MAP_SIZE=19
        self.MIN_MAP_SIZE = 8
        self.players=None
        self.current_player_index = None
        self.current_player_piece=None
        self.is_game_over=False
        self.winner = None
        self.game_type=None
        self.game_start=False
        self.FILE_DIR="data/memory.json"
    def initialize_game(self):
        self.game_start=True
        # 初始化游戏状态
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

        # 初始化角色
        self.players = [Player("player1"), Player("player2")]
        self.current_player_piece = 1
        self.current_player_index = 0
    def setBoardSize(self,board_size):
        if board_size<self.MIN_MAP_SIZE or board_size>self.MAX_MAP_SIZE:
            raise "输入的棋盘大小大于最大值或小于最小值！"
        else:
            self.board_size=board_size
    def make_move(self, move):
        pass
    def switch_player(self):
        # 切换当前玩家
        self.current_player_piece = 3 - self.current_player_piece # 用3来减，3-1=2；3-2=1
        self.current_player_index = 1-self.current_player_index
    def check_game_over(self):
       pass
    def surrenderGame(self,player):
        self.is_game_over = True
        self.winner = self.players[1-self.players.index(player)]
        return self.players.index(self.winner)+1
    def save_game_state(self):
        # 保存游戏状态
        temp_state=copy.deepcopy(self)
        return temp_state

    def load_game_state(self,previous_state):
        # 加载游戏状态
        self.board=previous_state.board
        self.current_player_index=previous_state.current_player_index
        self.current_player_piece =previous_state.current_player_piece
    def save(self):
        data={
            "board":self.board,
            "board_size":self.board_size,
            "player1_name":self.players[0].name,
            "player2_name": self.players[1].name,
            "current_player_index":self.current_player_index,
            "current_player_piece":self.current_player_piece,
            "game_type":self.game_type,
        }
        # 将数据写入 JSON 文件
        with open(self.FILE_DIR, "w") as file:
            json.dump(data, file)
        file.close()
    def load(self):
        # 从 JSON 文件中读取数据
        with open(self.FILE_DIR, "r") as file:
            data = json.load(file)
        file.close()
        self.board=data['board']
        self.board_size=data['board_size']
        self.players=[Player(data['player1_name']),Player(data['player2_name'])]
        self.current_player_index=data['current_player_index']
        self.current_player_piece=data['current_player_piece']
        self.game_type=data['game_type']

    def restartGame(self):
        self.board = None
        self.board_size = 0
        self.current_player_index=None
        self.is_game_over = False
        self.winner = None
        self.game_type = None
        self.game_start = False
class GomokuGameState(GameState):
    def __init__(self,game_type,board_size):
        super().__init__()
        self.game_type=game_type
        self.board_size=board_size
        self.initialize_game()
    def make_move(self, move):
        self.board[move["pos_x"]][move["pos_y"]]=self.current_player_piece #因为index是0/1，因此要+1变成1/2
    def check_game_over(self):
        # 检查游戏是否结束
        """判断游戏的结局。0为游戏进行中，1为玩家获胜，2为电脑获胜，3为平局"""
        # 1. 判断是否横向连续五子
        for x in range(len(self.board[0])-4):
            for y in range(len(self.board)):
                if self.board[x][y] == self.current_player_piece and self.board[x + 1][y] == self.current_player_piece and self.board[x + 2][y] == self.current_player_piece and \
                        self.board[x + 3][y] == self.current_player_piece and self.board[x + 4][y] == self.current_player_piece:
                    self.is_game_over=True
                    self.winner=self.players[self.current_player_index]
                    return 1


        # 2. 判断是否纵向连续五子
        for x in range(len(self.board[0])):
            for y in range(len(self.board)-4):
                if self.board[x][y] == self.current_player_piece and self.board[x][y + 1] == self.current_player_piece and self.board[x][y + 2] == self.current_player_piece and self.board[x][
                    y + 3] == self.current_player_piece and self.board[x][y + 4] == self.current_player_piece:
                    self.is_game_over = True
                    self.winner = self.players[self.current_player_index]
                    return 1

        # 3. 判断是否有左上-右下的连续五子
        for x in range(len(self.board[0])-4):
            for y in range(len(self.board)-4):
                if self.board[x][y] == self.current_player_piece and self.board[x + 1][y + 1] == self.current_player_piece and self.board[x + 2][y + 2] == self.current_player_piece and \
                        self.board[x + 3][y + 3] == self.current_player_piece and self.board[x + 4][y + 4] == self.current_player_piece:
                    self.is_game_over = True
                    self.winner = self.players[self.current_player_index]
                    return 1

        # 4. 判断是否有右上-左下的连续五子
        for x in range(len(self.board[0])-4):
            for y in range(len(self.board)-4):
                if self.board[x + 4][y] == self.current_player_piece and self.board[x + 3][y + 1] == self.current_player_piece and self.board[x + 2][y + 2] == self.current_player_piece and \
                        self.board[x + 1][y + 3] == self.current_player_piece and self.board[x][y + 4] == self.current_player_piece:
                    self.is_game_over = True
                    self.winner = self.players[self.current_player_index]
                    return 1

        # 5. 判断是否为平局
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[x][y] == 0:  # 棋盘中还有剩余的格子，不能判断为平局
                    return 0
        self.is_game_over = True
        return 2
class GoGameState(GameState):
    def __init__(self,game_type,board_size):
        super().__init__()
        self.game_type=game_type
        self.board_size=board_size
        self.initialize_game()
    def make_move(self, move):
        self.board[move["pos_x"]][move["pos_y"]]=self.current_player_piece #因为index是0/1，因此要+1变成1/2
        self.kill(self.deadlist)
    def check_game_over(self):
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[x][y] == 0:  # 棋盘中还有剩余的格子，不能判断为平局
                    self.is_game_over = True
                    return self.getWinner()

    def judge(self,x,y):
        self.board[x][y] = self.current_player_piece
        self.deadlist=self.getDeadList(x,y)
        # 判断是否属于有气和杀死对方其中之一
        if len(self.deadlist) > 0 or self.ifDead([[x, y]], self.current_player_piece, [x, y]) == False:
            # 当不重复棋局，且属于有气和杀死对方其中之一时，落下棋子有效
            self.board[x][y] = 0# 判断完后重新置零，在make_move时再设置为对于玩家的棋子
            return True
        else:
            # 不属于杀死对方或有气，则判断为无气，警告并弹出警告框
            self.board[x][y] = 0
            return False
    # 判断棋子（种类为yourChessman，位置为yourPosition）是否无气（死亡），有气则返回False，无气则返回无气棋子的列表
    # 本函数是游戏规则的关键，初始deadlist只包含了自己的位置，每次执行时，函数尝试寻找yourPosition周围有没有空的位置，有则结束，返回False代表有气；
    # 若找不到，则找自己四周的同类（不在deadlist中的）是否有气，即调用本函数，无气，则把该同类加入到deadlist，然后找下一个邻居，只要有一个有气，返回False代表有气；
    # 若四周没有一个有气的同类，返回deadlist,至此结束递归
    def ifDead(self, deadList, yourChessman, yourPosition):
        for i in [-1, 1]:
            if [yourPosition[0] + i, yourPosition[1]] not in deadList:
                if self.board[yourPosition[1]][yourPosition[0] + i] == 0:
                    return False
            if [yourPosition[0], yourPosition[1] + i] not in deadList:
                if self.board[yourPosition[1] + i][yourPosition[0]] == 0:
                    return False
        if ([yourPosition[0] + 1, yourPosition[1]] not in deadList) and (
                self.board[yourPosition[1]][yourPosition[0] + 1] == yourChessman):
            midvar = self.ifDead(deadList + [[yourPosition[0] + 1, yourPosition[1]]], yourChessman,
                                  [yourPosition[0] + 1, yourPosition[1]])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([yourPosition[0] - 1, yourPosition[1]] not in deadList) and (
                self.board[yourPosition[1]][yourPosition[0] - 1] == yourChessman):
            midvar = self.ifDead(deadList + [[yourPosition[0] - 1, yourPosition[1]]], yourChessman,
                                  [yourPosition[0] - 1, yourPosition[1]])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([yourPosition[0], yourPosition[1] + 1] not in deadList) and (
                self.board[yourPosition[1] + 1][yourPosition[0]] == yourChessman):
            midvar = self.ifDead(deadList + [[yourPosition[0], yourPosition[1] + 1]], yourChessman,
                                  [yourPosition[0], yourPosition[1] + 1])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        if ([yourPosition[0], yourPosition[1] - 1] not in deadList) and (
                self.board[yourPosition[1] - 1][yourPosition[0]] == yourChessman):
            midvar = self.ifDead(deadList + [[yourPosition[0], yourPosition[1] - 1]], yourChessman,
                                  [yourPosition[0], yourPosition[1] - 1])
            if not midvar:
                return False
            else:
                deadList += copy.deepcopy(midvar)
        return deadList

    # 落子后，依次判断四周是否有棋子被杀死，并返回死棋位置列表
    def getDeadList(self,x,y):
        deadlist = []
        for i in [-1, 1]:
            if self.board[y][x + i] == (2 if self.current_player_index == 0 else 1) and ([x + i, y] not in deadlist):
                killList = self.ifDead([[x + i, y]], (2 if self.current_player_index == 0 else 1), [x + i, y])
                if not killList == False:
                    deadlist += copy.deepcopy(killList)
            if self.board[y + i][x] == (2 if self.current_player_index == 0 else 1) and ([x, y + i] not in deadlist):
                killList = self.ifDead([[x, y + i]], (2 if self.current_player_index == 0 else 1), [x, y + i])
                if not killList == False:
                    deadlist += copy.deepcopy(killList)
        return deadlist

    def getWinner(self):# 通过判断谁棋子多来判断输赢
        player1_piece_num=0
        player2_piece_num = 0
        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                if self.board[x][y] == 1:  # 棋盘中还有剩余的格子，不能判断为平局
                    player1_piece_num+=1
                elif self.board[x][y] == 2:
                    player2_piece_num += 1
        if player1_piece_num!=player2_piece_num:
            self.winner = self.players[player1_piece_num<player2_piece_num]
            return 1
        else:
            return 2
    def kill(self,killList):
        if len(killList) > 0:
            for i in range(len(killList)):
                self.board[killList[i][1]][killList[i][0]]=0
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
class GomokuMoveCommand(GameCommand):
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
class GoMoveCommand(GameCommand):
    def __init__(self, game_state, move):
        self.game_state = game_state
        self.move = move
        self.previous_state = None
    def execute(self):
        self.previous_state = self.game_state.save_game_state()
    def undo(self):
        self.game_state.load_game_state(self.previous_state)
    def judge(self):
        if 0 <= self.move["pos_y"] <= len(self.game_state.board) and 0 <= self.move["pos_x"] <= len(self.game_state.board[0]) and self.game_state.board[self.move["pos_x"]][self.move["pos_y"]]==0:
            # 此时需要判断的要素太多，让game_state来判断,直接执行
            self.execute()
            self.judgment=self.game_state.judge(self.move["pos_x"],self.move["pos_y"])
        else:
            self.judgment=False
        return self.judgment
class PassCommand(GameCommand):
    def __init__(self, game_state):
        self.game_state = game_state
    def execute(self):
        # 执行命令
        # 不下棋就直接切换角色即可
        self.game_state.switch_player()
        pass
    def undo(self):
        # 撤销命令
        # 继续切换角色
        self.game_state.switch_player()
# 单例模式：游戏管理器
class GameManager:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    def __init__(self):
        self.game_state = None
        self.observers = []
        self.command=None
    def add_observer(self, observer):
        self.observers.append(observer)
    def remove_observer(self, observer):
        self.observers.remove(self.observers.index(observer))
    def notify_observers(self,result):
        # 通知观察者
        pass
    def start_game(self,game_type,board_size):
        if game_type=='gomoku':
            self.game_state=GomokuGameState(game_type,board_size)
        else:
            self.game_state = GoGameState(game_type, board_size)
    def move_1step(self,pos_x, pos_y):
        move={'pos_x':pos_x,'pos_y':pos_y}
        # 处理玩家输入等操作
        # 玩家的移动
        if self.game_state.game_type=='gomoku':
            self.command = GomokuMoveCommand(self.game_state, move)
            if self.command.judge():
                self.command.execute()
                judgement = True
            else:
                judgement = False
            return judgement
        else:
            self.command = GoMoveCommand(self.game_state, move)
            if self.command.judge():
                self.command.execute()
                judgement = True
            else:
                judgement = False
            return judgement
    def pass_1step(self):
        self.command = PassCommand(self.game_state)
        self.command.execute()
    def next_step(self):
        self.game_state.switch_player()
    def undo(self):
        self.command.undo()
    def save(self):
        self.game_state.save()
    def load(self):
        self.game_state.load()
    def surrenderGame(self,player):
        self.game_state.surrenderGame(player)
    def endGame(self):
        pass
