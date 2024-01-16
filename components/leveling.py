from components.abstact_component import AbstactComponent

class LevelingComponent(AbstactComponent):
    def __init__(self, level_thresholds=None) -> None:
        self.level = 1
        self.pp = 0
        if level_thresholds is None:
            level_thresholds = [1000, 3000]
        self.level_thresholds = level_thresholds

    def add_pp(self, pp:int):
        self.pp += pp
        self.check_for_level_up()
        print(self.pp)

    def remove_pp(self, pp: int):
        self.pp -= pp

    def check_for_level_up(self) -> bool:
        if self.level <= len(self.level_thresholds):
            threshold = self.level_thresholds[self.level-1]
            if self.pp >= threshold:
                self.level_up()

    def level_up(self) -> int:
        self.level += 1
        return self.level