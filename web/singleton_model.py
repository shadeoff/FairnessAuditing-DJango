from IntegratedInterface.main import AuditingFramework


class SingletonModel(AuditingFramework):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonModel,cls).__new__(cls, *args, **kwargs)
            cls._instance._setup(*args, **kwargs)
        return cls._instance

    def _setup(self, *args, **kwargs):
        self.auditing_framework = AuditingFramework()