import os
import paramiko
from git import Repo

class CompileModule(object):
    def __init__(self, ip, username, password):
        self.Ssh = ""
        self.ServerIP = ip
        self.UserName = username
        self.PassWord = password

    def ConnectServer(self):
        self.Ssh = paramiko.SSHClient()
        self.Ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.Ssh.connect(self.ServerIP, 22, self.UserName, self.PassWord)

    def ExecuteCommand(self, cmd):
        stdout = self.Ssh.exec_command(cmd)
        print(stdout.readlines())

    def CloseConnection(self):
        self.Ssh.close()

    def CloneCodeFromGit(self, repoPath, srcPath):
        if not os.path.exists(srcPath):
            Repo.clone_from(repoPath, srcPath)
        else:
            Repo.clone(srcPath)