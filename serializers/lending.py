from database import ma
from models.lending import Lending


class LendingSchema(ma.Schema):
    class Meta:
        fields = (
            "devolution_date",
            "id",
            "created_at",
            "client_id",
            "book_id"
        )
       
lending_schema = LendingSchema()
lendings_schema = LendingSchema(many=True)
