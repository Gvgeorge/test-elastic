import csv
from typing import IO

from fastapi import Depends
from models.posts import PostCreate
from models.rubrics import RubricCreate

from services.elastic import ElasticService
from services.posts import PostService
from services.rubrics import RubricService


class ReportService:
    def __init__(self,
                 post_service: PostService = Depends(),
                 rubric_service: RubricService = Depends(),
                 elastic_service: ElasticService = Depends()):
        self.post_service = post_service
        self.rubric_service = rubric_service
        self.elastic_service = elastic_service

    def import_csv(self, file: IO):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=['text', 'created_datetime', 'rubrics']
        )
        posts = []
        next(reader)

        for row in reader:
            row['rubrics'] = row['rubrics'].strip('[]').split(',')
            row['rubrics'] = [rubric.strip("\'\" ")
                              for rubric in row['rubrics']]
            row['rubrics'] = [RubricCreate.parse_obj({'name': rubric})
                              for rubric in row['rubrics']]
            post_data = PostCreate.parse_obj(row)
            posts.append(post_data)
        self.post_service.create_many(posts)
