# -*- coding: utf-8 -*-
import pymysql
class db:
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='wechat', charset='utf8mb4')
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    ## 查询一条数据
    def select_by_sql(self,sql):
        try:
            # 使用execute方法执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取一条数据
            data = self.cursor.fetchone()
            return data
        except:
            self.db.rollback()
        #finally:
            # 关闭数据库连接
        #    self.db.close()

    ## 向数据库中插入数据
    def insert_by_sql(self,sql):
        try:
            # 使用execute方法执行SQL语句
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        #finally:
            # 关闭数据库连接
        #   self.db.close()

    ## 查询数据库
    def select_by_sql_all(self,sql):
        try:
            # 使用execute方法执行SQL语句
            self.cursor.execute(sql)
            # 使用 fetchone() 方法获取一条数据
            data = self.cursor.fetchall()
            return data
        except:
            self.db.rollback()
        #finally:
            # 关闭数据库连接
        #    self.db.close()

    def close(self):
        self.db.close()

    def insert(self,sql):
        self.cursor.execute(sql)
        self.db.commit()

##if __name__=='__main__':
##    conn=db()
##    filepath='G:\photo\hdImg_ee15c1bd8799d179d5f21cb85f4ca30c1535443047667.jpg'
##    f=open(filepath,"rb")
##    b=f.read()
##    f.close()
##    
##    conn.insert("INSERT INTO friendinfo SET headimg='%s'"%(MySQLdb.Binary(b)))
##    conn.close()
##    print('写头像')



