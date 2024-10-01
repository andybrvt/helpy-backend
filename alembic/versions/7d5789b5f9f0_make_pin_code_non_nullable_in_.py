from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7d5789b5f9f0'
down_revision = 'e0f72a8f498d'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Manually make the pin_code column non-nullable
    op.alter_column('communities', 'pin_code', nullable=False)

def downgrade() -> None:
    # In case of downgrade, allow pin_code to be nullable again
    op.alter_column('communities', 'pin_code', nullable=True)
