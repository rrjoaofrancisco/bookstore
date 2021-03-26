from database import ma


class BookSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'title',
            'avaiable'
        )


book_schema = BookSchema()
books_schema = BookSchema(many=True)
