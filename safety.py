import secrets  # 注意这个Python自带的标准库不支持Python2.7
import hashlib
import os
from config import *


class SHA3(object):
    """
    计算sha3  SHA1已经不安全了
    """

    @staticmethod
    def cal(number):
        hexdig = hashlib.sha3_256(str(number).encode('utf8'))
        return hexdig.hexdigest()

    # 验证sha
    @staticmethod
    def verify(number, sql_number):

        hexig = hashlib.sha3_256(str(number).encode('utf8'))
        b = hexig.hexdigest()

        if b == sql_number:
            print("校验正确")
        else:
            print("校验错误")


def Create_AESkey():
    """
    随机AES密码,secrets这个库还有很多用处......
    用于程序初始化使用
    """
    pwd = str(secrets.token_urlsafe(nbytes=256))
    return pwd


class AES(object):
    """
    AES加密解密类,因为调用的是系统的openssl,因此下载它并添加到系统环境变量
    """

    def __init__(self, text_name, key):
        self.text = text_name
        self.password = key

    def encrypt(self, in_path, on_path):
        # 对称加密
        # TEXT是原文件
        path = os.path.join(in_path, self.text)
        out_path = os.path.join(on_path, self.text)
        try:
            os.system("openssl enc -aes-256-cbc -e -in %s -out %s -pass file:%s"
                      % (path, out_path, self.password))
        except Exception as e:
            print(e)

        os.remove(path)  # 删除源文件

    def decrypt(self, in_path, on_path):
        # 对称解密
        path = os.path.join(in_path, self.text)
        out_path = os.path.join(on_path, self.text)
        os.system("openssl enc -aes-256-cbc -d -in %s -out %s -pass file:%s"
                  % (path, out_path, self.password))

        os.remove(path)  # 删除源文件


# 自定义一个上下文管理器，用于数据库文件的加密解密的动作，以期能表现出数据库安全性

class database_safe(object):

    def __init__(self, dbname, key=None):
        # self.name = name
        self.aes = AES(dbname, key='pwdtool.key')
        # 当秘钥不存在该程序根目录下及加密后的数据库存在data文件夹里

        if 'pwdtool.key' not in os.listdir('./') and db_path in os.listdir('./data'):
            print('数据库秘钥不存在')
        # 当密码不存在该程序根目录下及加密后的数据库不存在data文件夹里，自动创建一个随机秘钥
        elif 'pwdtool.key' not in os.listdir('./') and db_path not in os.listdir('./data'):
            with open('pwdtool.key', 'w') as f:
                f.write(Create_AESkey())

    def endb(self):
        self.aes.encrypt('./', './data')

    def dedb(self):
        self.aes.decrypt('./data', './')
