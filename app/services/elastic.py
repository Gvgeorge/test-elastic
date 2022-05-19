import asyncio
from typing import List

import tables
from elasticsearch import AsyncElasticsearch
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
        self.es = AsyncElasticsearch(
            hosts=hosts,
            basic_auth=(settings.elastic_user, settings.elastic_pass))
        self.index_name = index_name
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name)
            self.sync_with_db()

    async def get_list(self):
        return await self.es.search(index=self.index_name,
                              query={"match_all": {}}, size=1000)

    async def add_to_index(self, post_id: int):
        post = await self.post_service.get(post_id)
        idx = await self.es.index(
            index=self.index_name,
            id=post_id,
            document={'text': post.text})
        return idx

    async def delete_index(self, index=None):
        if index is None:
            index = self.index_name
        await self.es.options(ignore_status=[400, 404]).indices.delete(index=index)

    async def delete_doc(self, doc_id: int):
        # сделать тут чтобы одновременно удалялись оба или никакой
        await self.post_service.delete(post_id=doc_id)
        await self.es.delete(index=self.index_name, id=doc_id)

    async def search(self, text: str, limit: int = 20) -> List[tables.Post]:
        elastic_res = await self.es.search(
            index=self.index_name,
            query={"match": {'text': text}},
            size=limit)
        elastic_top = [int(hit['_id'])
                       for hit in elastic_res['hits']['hits'][:limit]]
        return await self.post_service.get_many(
          elastic_top, tables.Post.created_datetime)

    async def sync_with_db(self):
        # плюс удаление
        post_list = await self.post_service.get_list()
        [await self.add_to_index(post.id) for post in post_list]
