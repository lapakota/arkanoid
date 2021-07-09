import json


class ConfigData:
    def __init__(self, path: str):
        with open(path, encoding="utf8") as file:
            config = json.load(file)

            self.GAME_WIDTH = config["GAME_WIDTH"]
            self.GAME_HEIGHT = config["GAME_HEIGHT"]
            self.FPS = config["FPS"]
            self.LIVES = config["LIVES"]
            self.DAMAGED_FOR_SPEEDUP = config["DAMAGED_FOR_SPEEDUP"]

            self.PADDLE_WIDTH = config["PADDLE_WIDTH"]
            self.PADDLE_HEIGHT = config["PADDLE_HEIGHT"]
            self.PADDLE_SPEED = config["PADDLE_SPEED"]
            self.PADDLE_COLOR = config["PADDLE_COLOR"]

            self.BALL_RADIUS = config["BALL_RADIUS"]
            self.BALL_SPEED = config["BALL_SPEED"]
            self.BALL_COLOR = config["BALL_COLOR"]

            self.BLOCK_WIDTH = config["BLOCK_WIDTH"]
            self.BLOCK_HEIGHT = config["BLOCK_HEIGHT"]
            self.BLOCK_COLOR = config["BLOCK_COLOR"]

            self.BONK_SOUND = config["BONK_SOUND"]
            self.CRASH_SOUND = config["CRASH_SOUND"]
            self.LIFE_SOUND = config["LIFE_SOUND"]
            self.LOOSE_SOUND = config["LOOSE_SOUND"]
            self.WIN_SOUND = config["WIN_SOUND"]

            self.BG_PATH = config["BG_PATH"]


CONFIG = ConfigData('game_config.json')
