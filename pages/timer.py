import time
import math

class Timer:
    POMODORO = "Pomodoro"
    SHORT_BREAK = "Short Break"
    LONG_BREAK = "Long Break"

    def __init__(self):
        self.__is_running = False
        self.__start_time = None
        self.__paused_time = None
        self.__duration = {
            Timer.POMODORO: 25 * 60,
            Timer.SHORT_BREAK: 5 * 60,
            Timer.LONG_BREAK: 15 * 60,
        }
        self.__current_mode = Timer.POMODORO
        self.__nPomodoros = 0

    def set_mode(self, mode):
        assert( mode in self.__duration.keys() )
        self.__current_mode = mode

    def get_mode(self):
        return self.__current_mode

    def reset(self):
        self.__start_time = time.time()
        self.__paused_time = None
        self.__is_running = True

    def pause(self):
        self.__paused_time = time.time()
        self.__is_running = False

    def resume(self):
        assert self.__paused_time is not None, "Resuming an unpaused time. What???"
        self.__is_running = True
        self.__start_time = time.time() - (self.__paused_time - self.__start_time)
        self.__paused_time = None

    def stop(self):
        self.__start_time = None
        self.__is_running = False

    def is_time_for_long_break(self):
        return self.__nPomodoros != 0 and self.__nPomodoros % 4 == 0

    def update_count(self):
        assert( self.get_time_left() < 0 )
        if self.__current_mode == Timer.POMODORO:
            self.__nPomodoros += 1

    def set_next_mode(self):
        if self.__current_mode == Timer.POMODORO:
            next_mode = Timer.LONG_BREAK if self.is_time_for_long_break() else Timer.SHORT_BREAK
        else:
            next_mode = Timer.POMODORO
        self.set_mode( next_mode )
        return next_mode

    def get_time_left(self):
        assert( self.__start_time is not None )
        duration = self.__duration[ self.__current_mode ]
        if self.__paused_time is not None:
            assert( not self.__is_running )
            return duration - (self.__paused_time - self.__start_time)
        return duration - (time.time() - self.__start_time)

    def get_duration(self):
        return self.__duration[ self.__current_mode ]

    def get_duration_in_min(self):
        return int( self.get_duration()/60 )

    def is_running(self):
        return self.__is_running

    def get_pomodoro_count(self):
        return self.__nPomodoros

    @staticmethod
    def get_all_modes():
        return Timer.POMODORO, Timer.SHORT_BREAK, Timer.LONG_BREAK

    @staticmethod
    def format_time(time_in_secs):
        time_in_secs = math.ceil(time_in_secs)
        nMins = int(time_in_secs / 60)
        nSecs = int(time_in_secs % 60)
        double_digit = lambda num: num if len(str(num)) > 1 else f"0{num}"
        return f"{double_digit(nMins)}:{double_digit(nSecs)}"