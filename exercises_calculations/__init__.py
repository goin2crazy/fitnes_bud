from . import pushups
from . import squats

from .squats import SquatExsercise
from .pushups import PushUpExercise
from .base import ExersicesBase

available_exercises = {squats.global_name: SquatExsercise, 
                       pushups.global_name: PushUpExercise}