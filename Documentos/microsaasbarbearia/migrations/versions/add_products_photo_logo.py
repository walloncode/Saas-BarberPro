"""add products table and photo/logo columns

Revision ID: add_products_table
Revises: 750b270bffb9
Create Date: 2026-04-07
"""
from alembic import op
import sqlalchemy as sa

revision = "add_products_table"
down_revision = "750b270bffb9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("photo_url", sa.String(300), nullable=True))
    op.add_column("barber_shops", sa.Column("logo_url", sa.String(300), nullable=True))

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("barber_shop_id", sa.Integer(), sa.ForeignKey("barber_shops.id"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("stock", sa.Integer(), server_default="0", nullable=False),
        sa.Column("image_url", sa.String(300), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="1", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.current_timestamp()),
    )


def downgrade():
    op.drop_table("products")
    op.drop_column("barber_shops", "logo_url")
    op.drop_column("users", "photo_url")
