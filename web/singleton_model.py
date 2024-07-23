from IntegratedInterface.main import AuditingFramework
from pympler import asizeof

class SingletonModel(AuditingFramework):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonModel,cls).__new__(cls, *args, **kwargs)
            cls._instance._setup(*args, **kwargs)
        return cls._instance

    def _setup(self, *args, **kwargs):
        self.auditing_framework = AuditingFramework()

    def get_memory_usage(self):
        return asizeof.asizeof(self.auditing_framework)