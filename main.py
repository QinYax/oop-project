from my_system import GameManager,GameStateObserver
from window import MyWindow
from PyQt5.QtWidgets import QApplication
# from game import Gomoku
import sys

class System:
    def __init__(self):
        self.game_manager = GameManager()
        # 创建观察者并添加到游戏管理器
        self.observer1 = GameStateObserver()
        self.observer2 = GameStateObserver()
        self.game_manager.add_observer(self.observer1)
        self.game_manager.add_observer(self.observer2)

        # ui
        self.app=QApplication(sys.argv)
        self.window=MyWindow(self.game_manager)
    def run(self):
        self.game_manager.start_game()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    system = System()
    system.run()