from fastapi import APIRouter, Depends, Response, status
from elasticsearch import Elasticsearch
import configparser
import warnings
from settings import settings
from services.posts import PostService
from services.rubrics import RubricService
import tables
from typing import List


warnings.filterwarnings("ignore")


config = configparser.ConfigParser()
config.read('auth.ini')


class ElasticService:
    def __init__(self,
                 post_service: PostService = Depends(),
                 rubric_service: RubricService = Depends(),
                 hosts: str = f'http://{settings.elastic_host}:{settings.elastic_port}',
                 index_name: str = settings.elastic_index):
        self.post_service = post_service
        self.rubric_service = rubric_service
        self.es = Elasticsearch(hosts=hosts)
        self.index_name = index_name

    def get_list(self):
        return self.es.search(index=self.index_name,
                              query={"match_all": {}}, size=1000)

    def add_to_index(self, post_id: int):
        post = self.post_service.get(post_id)
        idx = self.es.index(
            index=self.index_name,
            id=post_id,
            document={'text': post.text})
        return idx

    def delete_index(self, index=None):
        if index is None:
            index = self.index_name
        self.es.options(ignore_status=[400, 404]).indices.delete(index=index)

    def delete_doc(self, doc_id: int):
        # сделать тут чтобы одновременно удалялись оба или никакой
        self.post_service.delete(post_id=doc_id)
        self.es.delete(index=self.index_name, id=doc_id)

    def search(self, text: str, limit: int = 20) -> List[tables.Post]:
        elastic_res = self.es.search(
            index=self.index_name,
            query={"match": {'text': text}},
            size=limit)
        elastic_top = [int(hit['_id']) for hit in elastic_res['hits']['hits'][:limit]]
        return self.post_service.get_many(
          elastic_top, tables.Post.created_datetime)

    def sync_with_db(self):
        [self.add_to_index(post.id) for post in self.post_service.get_list()]
