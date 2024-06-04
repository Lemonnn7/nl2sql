from vanna.remote import VannaDefault
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
from vanna.flask import VannaFlaskApp
from openai import OpenAI
import pandas as pd
import pymysql
from sqlalchemy import create_engine, pool
client = OpenAI(
    base_url='http://localhost:11435/v1/',
    api_key='ollama',
)


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, client=None, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, client=client, config=config)


vn = MyVanna(client=client, config={"model": "llama3"})
vn.max_tokens = 1000
vn.temperature = 0.5

# # MySQL数据库连接参数
conn_details = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "test",
    "charset": "utf8mb3",
}

# conn_details = {
#     "host": "f824261c75.goho.co",
#     "port": 56671,
#     "user": "dbuser0511",
#     "password": "j#41!&jsDa*",
#     "database": "carsale_chat2sql",
#     "charset": "utf8mb3",
# }

# 创建MySQL数据库连接字符串URI
db_uri = f"mysql+pymysql://{conn_details['user']}:{conn_details['password']}@{conn_details['host']}:{conn_details['port']}/{conn_details['database']}?charset={conn_details['charset']}"

# 创建SQLAlchemy引擎
engine = create_engine(db_uri)

# # 建立MySQL数据库连接
# conn = pymysql.connect(**conn_details)
#
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/test?charset=utf8mb3')

# 定义一个函数,用于执行SQL查询并返回一个Pandas DataFrame
def run_sql(sql: str) -> pd.DataFrame:
    # df = pd.read_sql_query(sql, conn)
    df = pd.read_sql_query(sql, engine)
    return df


# 将函数设置到vn.run_sql中
vn.run_sql = run_sql
vn.run_sql_is_set = True


# vn.train(ddl="""
# CREATE TABLE IF NOT EXISTS car_sales (
#     yearmonth VARCHAR(254) COMMENT '年月',
#     fuel VARCHAR(50) COMMENT '燃料',
#     body_type VARCHAR(50) COMMENT '车身形式',
#     province VARCHAR(50) COMMENT '省份',
#     city VARCHAR(50) COMMENT '城市',
#     sales INT COMMENT '销量',
#     brand VARCHAR(50) COMMENT '品牌',
#     model VARCHAR(100) COMMENT '车型'
# );
# """)


# vn.train(ddl="""
# INSERT INTO users (id, username, email, age, gender, city) VALUES
# (1, '张三', 'zhangsan@example.com', 30, '男', '北京'),
# (2, '李四', 'lisi@example.com', 25, '女', '上海'),
# (3, '王五', 'wangwu@example.com', 40, '男', '广州'),
# (4, '赵六', 'zhaoliu@example.com', 35, '女', '深圳'),
# (5, '小明', 'xiaoming@example.com', 28, '男', '成都'),
# (6, '小红', 'xiaohong@example.com', 45, '女', '重庆'),
# (7, '小华', 'xiaohua@example.com', 32, '男', '天津'),
# (8, '小丽', 'xiaoli@example.com', 27, '女', '南京'),
# (9, '小李', 'xiaoli2@example.com', 38, '男', '武汉'),
# (10, '小美', 'xiaomei@example.com', 33, '女', '西安');
# """)

VannaFlaskApp(vn,allow_llm_to_see_data=True).run()
