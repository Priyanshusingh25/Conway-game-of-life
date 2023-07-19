from module.base.game_status import GameStatus


class Game:

    def __init__(self, state: GameStatus) -> None:
        self.state = state
        print(f"Game current state: {self.state} ")

    def launch(self) -> None:
        self.state = GameStatus.RUNNING

    def save(self) -> None:
        pass

    def restore(self) -> None:
        pass

    def history(self) -> None:
        pass

    def exit(self) -> None:
        self.state = GameStatus.CLOSED
