from .analysis import DataAnalysis
from .compile import CompileModule
from .pipeline import PipeLine


def GetData():
    pipeItem = PipeLine()
    cfgFilePath = pipeItem.GetConfigPath()
    pipeItem.ConfigMethod(cfgFilePath)
    pipeItem.GenHeader()
    pipeItem.LoginMethod()
    bugInfo = pipeItem.SpiderMethod()
    pipeItem.StoreData(bugInfo)


def CompileData():
    serverip = r"192.168.16.108"
    username = r"arm-cc1"
    password = r"kotei$88"
    obj = CompileModule(serverip, username, password)
    obj.ConnectServer()


def AnalysisData():
    obj = DataAnalysis()
    obj.GenDataDict()


if __name__ == "__main__":
    GetData()
    CompileData()
    AnalysisData()