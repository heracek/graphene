from singledispatch import singledispatch

from sqlalchemy import types
from sqlalchemy.orm import interfaces

from ...core.types.scalars import ID, Boolean, Float, Int, String
from .fields import ConnectionOrListField, SQLAlchemyModelField


def convert_sqlalchemy_relationship(relationship):
    direction = relationship.direction
    model = relationship.mapper.entity
    model_field = SQLAlchemyModelField(model, description=relationship.doc)
    if direction == interfaces.MANYTOONE:
        return model_field
    elif (direction == interfaces.ONETOMANY or
          direction == interfaces.MANYTOMANY):
        return ConnectionOrListField(model_field)


def convert_sqlalchemy_column(column):
    try:
        return convert_sqlalchemy_type(column.type, column)
    except Exception:
        raise Exception(
            "Don't know how to convert the SQLAlchemy field %s (%s)" % (column, column.__class__))


@singledispatch
def convert_sqlalchemy_type(type, column):
    raise Exception()


@convert_sqlalchemy_type.register(types.Date)
@convert_sqlalchemy_type.register(types.DateTime)
@convert_sqlalchemy_type.register(types.Time)
@convert_sqlalchemy_type.register(types.String)
@convert_sqlalchemy_type.register(types.Text)
@convert_sqlalchemy_type.register(types.Unicode)
@convert_sqlalchemy_type.register(types.UnicodeText)
@convert_sqlalchemy_type.register(types.Enum)
def convert_column_to_string(type, column):
    return String(description=column.doc)


@convert_sqlalchemy_type.register(types.SmallInteger)
@convert_sqlalchemy_type.register(types.BigInteger)
@convert_sqlalchemy_type.register(types.Integer)
def convert_column_to_int_or_id(type, column):
    if column.primary_key:
        return ID(description=column.doc)
    else:
        return Int(description=column.doc)


@convert_sqlalchemy_type.register(types.Boolean)
def convert_column_to_boolean(type, column):
    return Boolean(description=column.doc)


@convert_sqlalchemy_type.register(types.Float)
@convert_sqlalchemy_type.register(types.Numeric)
def convert_column_to_float(type, column):
    return Float(description=column.doc)