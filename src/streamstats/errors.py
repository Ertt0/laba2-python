class StreamStatsError(Exception):
    def __init__(self, message, file=None, num=None):
        self.message = message
        self.file = file
        self.num = num
        if file is not None:
            text = str(file) + ": "
            if num is not None:
                text += str(num) + ": "
            text += str(message)
        else:
            text = str(message)
        super().__init__(text)

class UnsupportedFormat(StreamStatsError):
    pass

class InvalidEvent(StreamStatsError):
    pass

class InvalidTimestamp(StreamStatsError):
    pass

class CLIError(StreamStatsError):
    pass
