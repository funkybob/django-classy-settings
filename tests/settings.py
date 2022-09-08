# File for testing __getattr__ factory

from cbs import BaseSettings, env


class Settings(BaseSettings):
    DEBUG = True

    IMMEDIATE_INT = env.int(5432)

    @env
    def STR_ENV(self):
        return "default"

    @env
    def STR_REQUIRED(self):
        raise ValueError("STR_REQUIRED not set")

    @env.bool
    def BOOL_ENV(self):
        return False

    def METHOD(self):
        return str(self.DEBUG)


class ProdSettings(Settings):
    DEBUG = False

    @env.bool
    def BOOL_ENV(self):
        return True


__getattr__ = BaseSettings.use()
