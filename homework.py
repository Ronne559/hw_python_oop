from abc import abstractmethod
from dataclasses import asdict, dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Trainig info message."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Trainig, base class."""
    # constants
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in KM."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get mean speed."""
        return self.get_distance() / self.duration

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Get spent calories."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return info message about done trainig."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Trainig: running."""
    # constants
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Trainig: SportsWalking."""
    # constants
    CONST_WALK_1: float = 0.035
    CONST_WALK_2: float = 0.029
    MIN_IN_HOUR: int = 60
    KM_H_TO_M_SEC: float = 0.278
    SANT_TO_METR: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.CONST_WALK_1 * self.weight + (
            (self.get_mean_speed() * self.KM_H_TO_M_SEC) ** 2
            / (self.height / self.SANT_TO_METR)
        ) * self.CONST_WALK_2 * self.weight
        ) * (self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Trainig: swimming."""
    # constants
    LEN_STEP: float = 1.38
    CONST_SWIM_1: float = 1.1
    CONST_SWIM_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CONST_SWIM_1)
                * self.CONST_SWIM_2
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: List[float]) -> Training:
    """Read data from module."""
    types_workout: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking
                                                }
    if workout_type not in types_workout:
        raise ValueError("Unsignet trainig code.")
    return types_workout[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
