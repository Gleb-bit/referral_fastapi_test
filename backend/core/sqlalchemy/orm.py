from typing import Union, Any, Sequence

from sqlalchemy import select, Result, Row, RowMapping, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class Orm:

    @staticmethod
    def get_query_with_relations(query, relations="*"):
        return query.options(selectinload(relations))

    @classmethod
    async def all(
        cls, model, session: AsyncSession, relations=None
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        Method to retrieve all records for the specified model.

        :param:
        - `model`: SQLAlchemy model.
        - `session`: SQLAlchemy asynchronous session.
        - `relations`: related fields.

        :return:
         `List of all records for the model.`
        """

        query = select(model)

        if relations:
            query = cls.get_query_with_relations(query, relations)

        execution = await session.execute(query)

        return execution.scalars().all()

    @classmethod
    async def create(cls, model, data: dict, session: AsyncSession):
        """
        Method to create the instance in the model based on a dictionary of fields.

        :param:
        - `model`: SQLAlchemy model.
        - `data`: Dictionary with model data.
        - `session`: SQLAlchemy asynchronous session.

        :return:
            `Created object.`
        """

        instance = model(**data)
        session.add(instance)

        await session.commit()
        await session.refresh(instance)

        return instance

    @classmethod
    async def filter_by(
        cls,
        model,
        filter_data: dict,
        session: AsyncSession,
        exclude_data: dict = None,
        relations=None,
    ) -> Result:
        """
        Method to filter records in the model based on a dictionary of fields.

        :param:
        - `model`: SQLAlchemy model.
        - `filter_data`: Dictionary with filter conditions.
        - `session`: SQLAlchemy asynchronous session.
        - `relations`: related fields.

        :return:
            `Query result filtered by the dictionary fields.`
        """

        query = select(model)

        if relations:
            query = cls.get_query_with_relations(query, relations)

        if exclude_data:
            exclude_query = select(model).filter_by(**exclude_data)
            query = query.except_(exclude_query)

        return await session.execute(query.filter_by(**filter_data))

    @classmethod
    async def insert(cls, model, data: list, session: AsyncSession, return_data=None):
        """
        Method to insert data in the model based on a dictionary of fields.

        :param:
        - `model`: SQLAlchemy model.
        - `data`: Dictionary with model data.
        - `session`: SQLAlchemy asynchronous session.
        - `return_data`: Fields to return after insert.

        :return:
            `ids of inserted objects.`
        """
        if not return_data:
            return_data = model.id

        stmt = insert(model).values(data).returning(return_data)

        result = await session.execute(stmt)
        await session.commit()

        return result

    @classmethod
    async def scalar(
        cls,
        model,
        session: AsyncSession,
        filters: Union[dict, bool] = dict,
        relations=None,
    ):
        """
        Method to execute a query and retrieve a single record from the model based on filter conditions.

        :param:
        - `model`: SQLAlchemy model to query.
        - `session`: SQLAlchemy asynchronous session.
        - `filters`: Dictionary or boolean condition for filtering (default is empty dictionary).
        - `relations`: related fields.

        :return:
            `First field value from the first row of the query result, or None if no record is found.`
        """

        if isinstance(filters, dict):
            query = await cls.filter_by(model, filters, session, relations)
        else:
            query = await cls.where(model, filters, session, relations)

        return query.scalar()

    @classmethod
    async def where(
        cls, model, filter_expr, session: AsyncSession, relations=None
    ) -> Result:
        """
        Method to filter records in the model based on a filter expression.

        :param:
        - `model`: SQLAlchemy model.
        - `filter_expr`: SQLAlchemy expression or boolean condition.
        - `session`: SQLAlchemy asynchronous session.
        - `relations`: related fields.

        :return:
            `Query result filtered by the given expression.`
        """
        query = select(model)
        if relations:
            query = cls.get_query_with_relations(query, relations)

        return await session.execute(query.where(filter_expr))
