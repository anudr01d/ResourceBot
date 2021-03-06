"""empty message

Revision ID: f99fd346669a
Revises: 
Create Date: 2017-10-12 14:08:26.545421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f99fd346669a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resourcelists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('empnumber', sa.String(length=255), nullable=True),
    sa.Column('designation', sa.String(length=255), nullable=True),
    sa.Column('employeetype', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('psft_id', sa.Integer(), nullable=True),
    sa.Column('date_of_joining', sa.DateTime(), nullable=True),
    sa.Column('tek_experience', sa.Float(), nullable=True),
    sa.Column('past_experience', sa.Float(), nullable=True),
    sa.Column('total_experience', sa.Float(), nullable=True),
    sa.Column('family', sa.String(length=255), nullable=True),
    sa.Column('manager', sa.String(length=255), nullable=True),
    sa.Column('reporting_manager', sa.String(length=255), nullable=True),
    sa.Column('level_1_manager', sa.String(length=255), nullable=True),
    sa.Column('project', sa.String(length=255), nullable=True),
    sa.Column('billable', sa.String(length=255), nullable=True),
    sa.Column('organization', sa.String(length=255), nullable=True),
    sa.Column('primary_skill', sa.String(length=255), nullable=True),
    sa.Column('customer', sa.String(length=255), nullable=True),
    sa.Column('tek_systems_bucket', sa.String(length=255), nullable=True),
    sa.Column('overall_bucket', sa.String(length=255), nullable=True),
    sa.Column('grouping', sa.String(length=255), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resourcelists')
    # ### end Alembic commands ###
