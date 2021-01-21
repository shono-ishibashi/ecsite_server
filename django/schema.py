import graphene
import pizza_graphql.schema


class Query(pizza_graphql.schema.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
)
