"""data

Revision ID: c29fda477230
Revises: 
Create Date: 2024-07-31 15:01:09.949976

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c29fda477230'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
                    sa.Column('actor_id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('gender', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('actor_id')
                    )
    op.create_index(op.f('ix_actors_gender'), 'actors', ['gender'], unique=False)
    op.create_index(op.f('ix_actors_name'), 'actors', ['name'], unique=False)
    op.create_table('genres',
                    sa.Column('genre_id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('genre_id')
                    )
    op.create_index(op.f('ix_genres_name'), 'genres', ['name'], unique=False)
    op.create_table('movies',
                    sa.Column('movie_id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('author', sa.String(), nullable=True),
                    sa.Column('year', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('movie_id')
                    )
    op.create_index(op.f('ix_movies_author'), 'movies', ['author'], unique=False)
    op.create_index(op.f('ix_movies_description'), 'movies', ['description'], unique=False)
    op.create_index(op.f('ix_movies_title'), 'movies', ['title'], unique=False)
    op.create_index(op.f('ix_movies_year'), 'movies', ['year'], unique=False)
    op.create_table('movie_actors',
                    sa.Column('movie_id', sa.Integer(), nullable=False),
                    sa.Column('actor_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['actor_id'], ['actors.actor_id'], ),
                    sa.ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], ),
                    sa.PrimaryKeyConstraint('movie_id', 'actor_id')
                    )
    op.create_table('movie_genres',
                    sa.Column('movie_id', sa.Integer(), nullable=False),
                    sa.Column('genre_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['genre_id'], ['genres.genre_id'], ),
                    sa.ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], ),
                    sa.PrimaryKeyConstraint('movie_id', 'genre_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_genres')
    op.drop_table('movie_actors')
    op.drop_index(op.f('ix_movies_year'), table_name='movies')
    op.drop_index(op.f('ix_movies_title'), table_name='movies')
    op.drop_index(op.f('ix_movies_description'), table_name='movies')
    op.drop_index(op.f('ix_movies_author'), table_name='movies')
    op.drop_table('movies')
    op.drop_index(op.f('ix_genres_name'), table_name='genres')
    op.drop_table('genres')
    op.drop_index(op.f('ix_actors_name'), table_name='actors')
    op.drop_index(op.f('ix_actors_gender'), table_name='actors')
    op.drop_table('actors')
    # ### end Alembic commands ###
