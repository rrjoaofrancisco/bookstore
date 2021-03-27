from database import ma


class LendingSchema(ma.Schema):
    class Meta:
        fields = (
            "devolution_date",
            "id",
            "created_at",
            "client_id",
            "book_id",
            "value"
        )


lending_schema = LendingSchema()
lendings_schema = LendingSchema(many=True)
