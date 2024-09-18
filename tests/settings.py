# File for testing __getattr__ factory

from cbs import BaseSettings, env

GLOBAL = "global"


class Settings(BaseSettings):
    DEBUG = True

    private = True

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

    def NESTED(self):
        return self.METHOD


class ProdSettings(Settings):
    DEBUG = False

    @env.bool
    def BOOL_ENV(self):
        return True


class GlobalSettings(Settings):
    GLOBAL = "local"

    IMMEDIATE_INT = Settings.Unset


__getattr__, __dir__ = BaseSettings.use()
