from dolfin import LogLevel

import dolfin as df

import m3h3


def set_log_level(level):
    """Sets the log level.

    Parameters
    ----------
    level : int
        Log level that should be set.
    """
    df.set_log_level(level)
    m3h3.parameters.update({"log_level": df.get_log_level()})
    log(LogLevel.INFO, "Log level updated to {}".format(level))


def log(level, msg):
    """Write a message to the logger.

    Parameters
    ----------
    level : int
        Log level of the message.
    msg : str
        Log message.
    """
    df.begin(level, msg)
    df.end()
