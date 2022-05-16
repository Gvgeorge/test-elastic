from services.elastic import ElasticService
from services.posts import PostService
from services.rubrics import RubricService
from fastapi import Depends
from models.posts import PostCreate
from models.rubrics import RubricCreate
from typing import IO
import csv
from io import StringIO


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

    def export_csv(self, user_id: int) -> IO:
        '''НЕ РАБОТАЕТ'''
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=['date', 'kind', 'amount', 'description'],
            extrasaction='ignore'
        )

        operations = self.operations_service.get_list(user_id)
        writer.writeheader()
        for operation in operations:
            operation_data = Post.from_orm(operation)
            writer.writerow(operation_data.dict())
        output.seek(0)
        return output

