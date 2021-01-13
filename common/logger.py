log = None
def append_exc(func):
    def _append_exc(*args, **kwargs):
        if 'exc_info' not in kwargs:
            kwargs['exc_info'] = True
        return func(*args, **kwargs)
    return _append_exc

def _log_record_exception(func):
    def _func(self):
        try:
            return func(self)
        except:
            log.exception('log_exception|thread=%s:%s,file=%s:%s,func=%s:%s,log=%s',
                self.process, self.thread, self.filename, self.lineno, self.module, self.funcName, self.msg)
            raise
    return _func

def init_logger(log_dir=None):
    import os
    import sys

    if log_dir is None:
        log_dir = './log'

    # if not os.path.exists(log_dir):
    #     os.mkdir(log_dir)

    if log_dir != '@stdout':
        log_dir = os.path.abspath(log_dir)
        if log_dir and not os.path.exists(log_dir):
            os.mkdir(log_dir)

    logger_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s.%(msecs)03d|%(levelname)s|%(process)d:%(thread)d|%(filename)s:%(lineno)d|%(module)s.%(funcName)s|%(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'short': {
                'format': '%(asctime)s.%(msecs)03d|%(levelname)s|%(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'data': {
                'format': '%(asctime)s.%(msecs)03d|%(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard'
            },
            'file_fatal': {
                'level': 'CRITICAL',
                'class': 'logging.FileHandler',
                'filename': os.path.join(log_dir, 'fatal.log').replace('\\', '/'),
                'formatter': 'standard',
            },
            'file_error': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'filename': os.path.join(log_dir, 'error.log').replace('\\', '/'),
                'formatter': 'standard',
            },
            'file_info': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(log_dir, 'info.log').replace('\\', '/'),
                'formatter': 'short',
            },
            'file_data': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(log_dir, 'data.log').replace('\\', '/'),
                'formatter': 'data',
            },
        },
        'loggers': {
            'main': {
                'handlers': ['file_fatal', 'file_error', 'file_info'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'data': {
                'handlers': ['file_data'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'log_entrytask': {
                'handlers': ['file_fatal', 'file_error', 'file_info'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'data_entrytask': {
                'handlers': ['file_data'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['file_fatal', 'file_error', 'file_info'],
                'level': 'ERROR',
                'propagate': True,
            },
            'tornado.access': {
                'handlers': ['file_data'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'tornado.application': {
                'handlers': ['file_fatal', 'file_error', 'file_info'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'tornado.general': {
                'handlers': ['file_fatal', 'file_error', 'file_info'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console', 'file_fatal', 'file_error', 'file_info'],
                'propagate': True,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console', 'file_fatal', 'file_error', 'file_info'],
                'propagate': True,

            },
        }
    }

    work_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
    recover_path = False
    if work_dir not in sys.path:
        sys.path.append(work_dir)
        recover_path = True

    # import logging.config
    import logging.config
    logging.config.dictConfig(logger_config)

    if recover_path:
        sys.path.remove(work_dir)

    # _patch_print_exception()
    global log	# pylint: disable=global-statement
    # log = logging.getLogger('log_entrytask')
    log = logging.getLogger('raven')
    log.exception = append_exc(log.error)
    log.assertion = log.critical
    log.warning = log.error
    # log.data = logging.getLogger('data_entrytask').info
    log.data = logging.getLogger('data_authorization').info
    logging.LogRecord.getMessage = _log_record_exception(logging.LogRecord.getMessage)

def _patch_print_exception():
    import traceback
    import sys
    _print = traceback.print_exc()  # pylint: disable=protected-access

    def custom_print_exception(etype, value, tb, limit=None, file=None): # pylint: disable=redefined-builtin
        if file is None:
            file = sys.stderr
        exc_info = sys.exc_info()
        stack = traceback.extract_stack()
        tb = traceback.extract_tb(exc_info[2])
        i = len(stack)
        while i > 0 and ('/logging/' in stack[i - 1][0] or 'common/logger.py' in stack[i - 1][0]): # remove the tedious stacktrace log
            i -= 1
        full_tb = stack[:i]
        full_tb.extend(tb)
        exc_line = traceback.format_exception_only(*exc_info[:2])
        _print(file, "Traceback (most recent call last):")
        _print(file, "".join(traceback.format_list(full_tb)), terminator='')
        _print(file, "".join(exc_line))

    traceback.print_exception = custom_print_exception

def try_init_logger():
    try:
        import config

        setting_keys = dir(config)
        if 'LOGGER_CONFIG' in setting_keys:
            init_logger(**config.LOGGER_CONFIG)
        else:
            init_logger()
    except:
        try:
            import config
            init_logger(**config.LOGGER_CONFIG)
        except:
            try:
                init_logger()
            except:
                pass

if log is None:
    try_init_logger()
