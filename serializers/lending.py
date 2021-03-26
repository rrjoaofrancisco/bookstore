from database import ma
from models.lending import Lending


class LendingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lending
        load_instance = True
        load_only = ("book","client")
        include_fk= True
       
lending_schema = LendingSchema()
lendings_schema = LendingSchema(many=True)
