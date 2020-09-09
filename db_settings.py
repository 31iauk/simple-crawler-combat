from sqlalchemy import create_engine,Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 用declarative_base()来创建对象的基类
Base = declarative_base()


# 定义Movies对象
class Movies(Base):
    # 表的名字
    __tablename__ = 'movies'
    # 表的结构
    index = Column(Integer, primary_key=True, autoincrement=True)
    src = Column(Text, nullable=False)
    name = Column(String(50), nullable=False)
    actor = Column(String(50), nullable=False)
    time = Column(String(50), nullable=False)
    score = Column(String(50), nullable=False)


# create_engine()用来初始化数据库连接
engine = create_engine('mysql+pymysql://root:0926yyy@127.0.0.1:3306/movies?charset=utf8mb4')
# 根据映射类创建表，通过engine发送到数据库上执行
Base.metadata.create_all(engine)

# 创建DBSession类型，通过session类的实例来使用会话
DBSession = sessionmaker(bind=engine)
# DBSession实例化对象session能进行增、删、改、查
session = DBSession()
