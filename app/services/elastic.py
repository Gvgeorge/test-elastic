from typing import List

import tables
from elasticsearch import Elasticsearch
from fastapi import Depends
from settings import settings

from services.posts import PostService
from services.rubrics import RubricService


class ElasticService:
    def __init__(self,
                 post_service: PostService = Depends(),
                 rubric_service: RubricService = Depends(),
                 hosts: str = f'http://{settings.elastic_host}:{settings.elastic_port}',
                 index_name: str = settings.elastic_index):
        self.post_service = post_service
        self.rubric_service = rubric_service
        self.es = Elasticsearch(
            hosts=hosts,
            basic_auth=(settings.elastic_user, settings.elastic_pass))
        self.index_name = index_name
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name)
            self.sync_with_db()

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
        elastic_top = [int(hit['_id'])
                       for hit in elastic_res['hits']['hits'][:limit]]
        return self.post_service.get_many(
          elastic_top, tables.Post.created_datetime)

    def sync_with_db(self):
        post_list = self.post_service.get_list()
        [self.add_to_index(post.id) for post in post_list]
