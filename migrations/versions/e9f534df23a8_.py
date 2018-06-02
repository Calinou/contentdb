"""empty message

Revision ID: e9f534df23a8
Revises: adad68a5e370
Create Date: 2018-06-02 18:30:54.234366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9f534df23a8'
down_revision = 'adad68a5e370'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('krock_forum_topic', 'link',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('package_release', 'link',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###
