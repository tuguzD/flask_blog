"""1_sessions

Revision ID: 4ba94b9861df
Revises: 
Create Date: 2022-01-24 17:21:36.718513

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4ba94b9861df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash', existing_type=sa.CHAR(60), type_=sa.VARCHAR(128))
    op.create_table('session',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.ForeignKeyConstraint(('user_id',), ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('user_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'password_hash', existing_type=sa.VARCHAR(128), type_=sa.CHAR(60))
    op.drop_table('session')
    # ### end Alembic commands ###
