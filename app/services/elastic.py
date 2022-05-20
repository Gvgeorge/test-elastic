from typing import List

import tables
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from settings import settings

from services.posts import PostService
from services.rubrics import RubricService
from models.posts import PostCreate, PostUpdate


class ElasticService:
    def __init__(
            self,
            post_service: PostService = Depends(),
            hosts=f'http://{settings.elastic_host}:{settings.elastic_port}',
            rubric_service: RubricService = Depends(),
            index_name: str = settings.elastic_index):
        self.post_service = post_service
        self.rubric_service = rubric_service
        self.es = AsyncElasticsearch(
            hosts=hosts,
            basic_auth=(settings.elastic_user,
                        settings.elastic_pass))
        self.index_name = index_name
        self.check_idx()  # sync actually

    async def check_idx(self):
        if not await self.es.indices.exists(index=self.index_name):
            await self.es.indices.create(index=self.index_name)
            await self.sync_with_db()

    async def get_list(self):
        return await self.es.search(
            index=self.index_name, query={"match_all": {}}, size=1000)

    async def _add(self, post_id: int, post_text: str):
        idx = await self.es.index(
            index=self.index_name,
            id=post_id,
            document={'text': post_text})
        return idx

    async def add_from_db(self, post_id: int):
        '''adds post from db to index'''
        post = await self.post_service.get(post_id)
        return await self._add(post_id, post.text)

    async def add(self, post_data: PostCreate) -> tables.Post:
        '''adds post both to db and index'''
        post = await self.post_service.create(post_data)
        return await self._add(post.id, post.text)

    async def delete_index(self, index=None):
        if index is None:
            index = self.index_name
        await self.es.options(
            ignore_status=[400, 404]).indices.delete(index=index)

    async def delete_doc(self, doc_id: int):
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

    async def sync_with_db(self) -> None:
        post_list = await self.post_service.get_list()
        [await self.add_from_db(post.id) for post in post_list]

    async def update(self, post_id: int,  post_data: PostUpdate
                     ) -> tables.Post:
        await self.es.update(
            index=self.index_name,
            id=post_id,
            doc={'text': post_data.text})
        return await self.post_service.update(post_id, post_data)
