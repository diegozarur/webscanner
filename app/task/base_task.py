from app import make_logger, celery


class BaseTask(celery.Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        logger = make_logger()
        logger.info('task start')
        try:
            return self.run(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            raise
        finally:
            logger.info('task end')
