from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

"""
    网站数据模型：  Movie / Ranking / RankingItem / Interaction / Admin
"""

class Movie(Base):

    """电影主表"""
    __tablename__ = "movies"

    id              =   Column(Integer, primary_key=True, index=True)
    douban_id       =   Column(String, unique=True, index=True)             # 豆瓣 _id
    title           =   Column(String, index=True)                          # 片名
    year            =   Column(String)                                      # 上映年份

    rating_ratio    =   Column(String)
    rating          =   Column(Float, default=0.0)                          # 豆瓣评分
    rating_count    =   Column(Integer, default=0)                          # 评分人数
    duration        =   Column(String)                                      # 片长
    summary         =   Column(Text)                                        # 剧情简介
    poster          =   Column(Text)                                        # 海报 url
    imdb            =   Column(String)                                      # imdb 编号

    # 多值字段，取出后 split(',')
    genres          =   Column(String)
    directors       =   Column(String)
    casts           =   Column(String)
    countries       =   Column(String)
    languages       =   Column(String)
    # 多值字段，取出后 split(',')
    pubdate         =   Column(String)                                      # 上映日期

    created_at      =   Column(DateTime(timezone=True), server_default=func.now())

    # 一部电影能被多部榜单收录
    ranking_items   =   relationship("RankingItem", back_populates="movie")
    interactions    =   relationship("Interaction", back_populates="movie")

class Ranking(Base):

    """ 榜单表 —— 管理员创建"""
    __tablename__ = "rankings"

    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String, nullable=False)                                  # 榜单名
    description     =   Column(Text)                                                    # 榜单介绍
    cover           =   Column(String)                                                  # 榜单封面
    created_at      =   Column(DateTime(timezone=True), server_default=func.now())

    items           =   relationship("RankingItem", back_populates="ranking",
                                     order_by="RankingItem.rank_order")
    

class RankingItem(Base):

    """ 榜单元素 """
    __tablename__ = "ranking_items"

    id              =   Column(Integer, primary_key=True, index=True)
    ranking_id      =   Column(Integer, ForeignKey("rankings.id", ondelete="CASCADE"))
    movie_id        =   Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))
    # 榜单内排名
    rank_order      =   Column(Integer, default=0)

    ranking         =   relationship("Ranking", back_populates="items")
    movie           =   relationship("Movie", back_populates="ranking_items")


class Interaction(Base):

    __tablename__ = "interactions"

    id              =   Column(Integer, primary_key=True, index=True)
    movie_id        =   Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"))

    type            =   Column(String, nullable=False)
    created_at      =   Column(DateTime(timezone=True), server_default=func.now())          # like - 点赞   collection - 收藏

    movie           =   relationship("Movie", back_populates="interactions")

class Admin(Base):

    __tablename__ = "admins"

    id              =   Column(Integer, primary_key=True, index=True)
    username        =   Column(String, unique=True, nullable=False)
    password_hash   =   Column(String, nullable=False)