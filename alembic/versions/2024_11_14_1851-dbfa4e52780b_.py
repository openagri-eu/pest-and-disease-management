"""empty message

Revision ID: dbfa4e52780b
Revises: 
Create Date: 2024-11-14 18:51:44.678115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbfa4e52780b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('dataset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('operator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('pest',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('geo_areas_of_application', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('unit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('symbol', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('cultivation',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('pest_model_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['pest_model_id'], ['pest.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('time', sa.Time(), nullable=True),
    sa.Column('parcel_location', sa.String(), nullable=True),
    sa.Column('atmospheric_temperature', sa.Float(), nullable=True),
    sa.Column('atmospheric_temperature_daily_min', sa.Float(), nullable=True),
    sa.Column('atmospheric_temperature_daily_max', sa.Float(), nullable=True),
    sa.Column('atmospheric_temperature_daily_average', sa.Float(), nullable=True),
    sa.Column('atmospheric_relative_humidity', sa.Float(), nullable=True),
    sa.Column('atmospheric_pressure', sa.Float(), nullable=True),
    sa.Column('precipitation', sa.Float(), nullable=True),
    sa.Column('average_wind_speed', sa.Float(), nullable=True),
    sa.Column('wind_direction', sa.String(), nullable=True),
    sa.Column('wind_gust', sa.Float(), nullable=True),
    sa.Column('leaf_relative_humidity', sa.Float(), nullable=True),
    sa.Column('leaf_temperature', sa.Float(), nullable=True),
    sa.Column('leaf_wetness', sa.Float(), nullable=True),
    sa.Column('soil_temperature_10cm', sa.Float(), nullable=True),
    sa.Column('soil_temperature_20cm', sa.Float(), nullable=True),
    sa.Column('soil_temperature_30cm', sa.Float(), nullable=True),
    sa.Column('soil_temperature_40cm', sa.Float(), nullable=True),
    sa.Column('soil_temperature_50cm', sa.Float(), nullable=True),
    sa.Column('soil_temperature_60cm', sa.Float(), nullable=True),
    sa.Column('solar_irradiance_copernicus', sa.Float(), nullable=True),
    sa.Column('dataset_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['dataset_id'], ['dataset.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('rule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('from_time', sa.TIME(), nullable=True),
    sa.Column('to_time', sa.TIME(), nullable=True),
    sa.Column('probability_value', sa.String(), nullable=True),
    sa.Column('pest_model_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['pest_model_id'], ['pest.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('condition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rule_id', sa.Integer(), nullable=False),
    sa.Column('unit_id', sa.Integer(), nullable=False),
    sa.Column('operator_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['operator_id'], ['operator.id'], ),
    sa.ForeignKeyConstraint(['rule_id'], ['rule.id'], ),
    sa.ForeignKeyConstraint(['unit_id'], ['unit.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('condition')
    op.drop_table('rule')
    op.drop_table('data')
    op.drop_table('cultivation')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('unit')
    op.drop_table('pest')
    op.drop_table('operator')
    op.drop_table('dataset')
    op.drop_table('action')
    # ### end Alembic commands ###
