from rock_paper_sissors import RockPaperScissors
from menu.interface import Menu
if __name__ == "__main__":
        menu = Menu()
        choice = menu.run()
        print(choice)
        
        rpc = RockPaperScissors()
        rpc.run()