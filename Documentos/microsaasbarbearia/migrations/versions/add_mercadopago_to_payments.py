"""add mercadopago_id to payments

Revision ID: add_mercadopago_to_payments
Revises: add_products_table
Create Date: 2026-04-07
"""
from alembic import op
import sqlalchemy as sa

revision = "add_mercadopago_to_payments"
down_revision = "add_products_table"
branch_labels = None
depends_on = None


def upgrade():
    # mercadopago_id column already exists in the database.
    pass


def downgrade():
    with op.batch_alter_table("payments", schema=None) as batch_op:
        batch_op.drop_column("mercadopago_id")
