"""2_posts

Revision ID: a3e5f65838f8
Revises: 4ba94b9861df
Create Date: 2022-01-25 14:50:05.625774

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3e5f65838f8'
down_revision = '4ba94b9861df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
                    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('author_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('title', sa.VARCHAR(length=100), nullable=False),
                    sa.Column('text_content', sa.TEXT(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
                    sa.ForeignKeyConstraint(('author_id',), ['user.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_post_created_at'), 'post', ['created_at'], unique=False)
    op.create_index(op.f('ix_post_title'), 'post', ['title'], unique=False)
    op.create_table('deleted_post',
                    sa.Column('post_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('soft_deleted_at', sa.TIMESTAMP(), nullable=False),
                    sa.ForeignKeyConstraint(('post_id',), ['post.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('post_id')
                    )
    op.create_index(op.f('ix_deleted_post_soft_deleted_at'), 'deleted_post', ['soft_deleted_at'], unique=False)
    op.drop_constraint('session_user_id_fkey', 'session', type_='foreignkey')
    op.create_foreign_key(None, 'session', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('session_user_id_fkey', 'session', type_='foreignkey')
    op.create_foreign_key('session_user_id_fkey', 'session', 'user', ['user_id'], ['id'])
    op.drop_index(op.f('ix_deleted_post_soft_deleted_at'), table_name='deleted_post')
    op.drop_table('deleted_post')
    op.drop_index(op.f('ix_post_title'), table_name='post')
    op.drop_index(op.f('ix_post_created_at'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###
