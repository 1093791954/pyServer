import os
import shutil
import base64

class CFileManager :
    rootDir : str
    def __init__(self , rootDir : str) -> None:
        self.rootDir = rootDir
        if not self.rootDir.endswith('\\'):
            self.rootDir += '\\'

    def upLoadScriptFile_bin(self, userName: str, fileName: str, file_base64: str):
        """
        上传脚本文件(二进制)。

        参数：
        - username (str): 用户名
        - fileName (str): 文件名
        - file_base64 (str): 文件的Base64编码字符串

        返回值：
        无

        异常：
        无
        """
        folder_path = os.path.join(self.rootDir, userName)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        file_path = os.path.join(folder_path, fileName)
        if os.path.exists(file_path):
            mode = 'wb'
        else:
            mode = 'xb'
        
        with open(file_path, mode) as file:
            file.write(base64.b64decode(file_base64))

    
    def upLoadScriptFile_str(self, username: str, fileName: str, file_base64: str):
        """
        上传脚本文件(文本)。

        参数：
        - username (str): 用户名
        - fileName (str): 文件名
        - file_base64 (str): 文件的Base64编码字符串

        返回值：
        无

        异常：
        无
        """
        folder_path = os.path.join(self.rootDir, username)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, fileName)
        if os.path.exists(file_path):
            mode = 'w'
        else:
            mode = 'x'

        with open(file_path, mode) as file:
            file.write(base64.b64decode(file_base64).decode('utf-8'))
        
    def getUserScriptFileList(self, username: str):
        """
        获取用户脚本文件列表。

        参数：
        - username (str): 用户名

        返回值：
        - file_list (list): 用户脚本文件名列表

        异常：
        无
        """
        folder_path = os.path.join(self.rootDir, username)
        if not os.path.exists(folder_path):
            return []

        file_list = os.listdir(folder_path)
        return file_list

    def getUserScriptFile_bin(self, username: str, fileName: str):
        """
        获取用户脚本文件(二进制)。

        参数：
        - username (str): 用户名
        - fileName (str): 文件名

        返回值：
        - file_base64 (str): 文件的Base64编码字符串

        异常：
        无
        """
        folder_path = os.path.join(self.rootDir, username)
        file_path = os.path.join(folder_path, fileName)

        if not os.path.exists(folder_path) or not os.path.exists(file_path):
            return None

        with open(file_path, 'rb') as file:
            file_base64 = base64.b64encode(file.read()).decode('utf-8')

        return file_base64
    
    def getUserScriptFile_str(self, username: str, fileName: str):
        """
        获取用户脚本文件(文本)。

        参数：
        - username (str): 用户名
        - fileName (str): 文件名

        返回值：
        - file_content (str): 文件内容字符串

        异常：
        无
        """
        folder_path = os.path.join(self.rootDir, username)
        file_path = os.path.join(folder_path, fileName)

        if not os.path.exists(folder_path) or not os.path.exists(file_path):
            return None

        if os.path.isdir(file_path):
            return None

        with open(file_path, 'r') as file:
            file_content = file.read()

        return file_content

    def delUserScriptFile_str(self, username: str, fileName: str):
        """
        删除用户脚本文件(文本)。

        参数：
        - username (str): 用户名
        - fileName (str): 文件名

        返回值：
        - success (bool): 删除成功返回True，否则返回False

        异常：
        无
        """
        folder_path = os.path.join(self.rootDir, username)
        file_path = os.path.join(folder_path, fileName)

        if not os.path.exists(folder_path) or not os.path.exists(file_path):
            return False

        if os.path.isdir(file_path):
            return False

        os.remove(file_path)
        return True



scriptManager = CFileManager(os.getcwd())
