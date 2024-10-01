from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
import random
import string

# revision identifiers, used by Alembic.
revision = 'e0f72a8f498d'
down_revision = '5cacc5422961'
branch_labels = None
depends_on = None

# Helper function to generate a unique 5-character alphanumeric PIN
def generate_unique_pin():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def upgrade() -> None:
    # Step 1: Add the pin_code column as nullable
    op.add_column('communities', sa.Column('pin_code', sa.String(length=5), nullable=True))
    op.create_index(op.f('ix_communities_pin_code'), 'communities', ['pin_code'], unique=True)

    # Step 2: Generate and assign unique PINs for existing communities
    connection = op.get_bind()

    # Fix: Wrap the raw SQL query in the text() function
    results = connection.execute(text("SELECT id FROM communities")).fetchall()

    if not results:
        print("No communities found!")
    
    for result in results:
        pin_code = generate_unique_pin()
        print(f"Assigning PIN {pin_code} to community ID {result[0]}")  # Debugging statement
        connection.execute(text(f"UPDATE communities SET pin_code = '{pin_code}' WHERE id = {result[0]}"))

    # Step 3: After assigning PINs, alter the column to make it NOT NULL
    op.alter_column('communities', 'pin_code', nullable=False)

def downgrade() -> None:
    # Drop the pin_code column in case of downgrade
    op.drop_index(op.f('ix_communities_pin_code'), table_name='communities')
    op.drop_column('communities', 'pin_code')
