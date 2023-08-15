from consts import PLAYER, AI, ENGINE, DEBUG

class Logging:
    def __init__(self):
        self.set_out_file(None)

    def set_out_file(self, out_file):
        self.log_to_file = out_file is not None
        if self.log_to_file:
            self.out_file = out_file

    def log(self, msg):
        print(msg, end="")
        if self.log_to_file:
            self.out_file.write(msg)

    def log_debug(self, msg):
        if DEBUG['LOG']: print("\n[DEBUG] " + msg)

    def log_move(self, turn, turn_number, move):
        if DEBUG['LOG'] or turn: self.log(f"\n{str(turn_number)}. {move}   ")
        else: self.log(f"\t{move}")
    
logging = Logging()
