import logging

def init_logging():

    handler_list = ["stdout"]
    log_config = {
        "version": 1,
        "formatters": {
            "telegram": {
                "class": "telegram_handler.HtmlFormatter",
                "datefmt": "%d-%b-%y %H:%M:%S",
                "format": "main" + " <code>%(asctime)s</code> - %(name)s: - %(levelname)s: %(message)s"
            },
            "basic": {
                "format": "%(name)s: %(asctime)s - %(levelname)s: %(message)s"
            },
            'detailed': {
                'class': 'logging.Formatter',
                # 'format': 'ts_log=%(asctime)s.%(msecs)d level=%(levelname)s logger_name=%(name)s location=%(filename)s:%(lineno)d trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s %(message)s',
                'format': 'ts_log=%(asctime)s.%(msecs)d level=%(levelname)s logger_name=%(name)s location=%(filename)s:%(lineno)d %(message)s',
                'datefmt': '%s',
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "detailed",
                "level": "DEBUG",
            }
        },
        "loggers": {
            "": {
                "handlers": handler_list,
                "level": "DEBUG"
            },
            "uvicorn.access": {
                "handlers": handler_list,
                "level": "DEBUG"
            },
            "uvicorn.error": {
                "handlers": handler_list,
                "level": "DEBUG"
            },
            'aiokafka': {
                "handlers": handler_list,
                "level": "WARNING"
            }
        },
        "disable_existing_loggers": False,
    }
    logging.config.dictConfig(log_config)