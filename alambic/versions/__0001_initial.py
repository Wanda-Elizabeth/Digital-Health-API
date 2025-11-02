"""
Revision ID: 0001_initial
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create patients table
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('identifier', sa.String(length=128), nullable=False, unique=True),
        sa.Column('given_name', sa.String(length=128), nullable=False),
        sa.Column('family_name', sa.String(length=128), nullable=False),
        sa.Column('birth_date', sa.Date(), nullable=False),
        sa.Column('gender', sa.String(length=32), nullable=True),
    )
    op.create_index(op.f('ix_patients_id'), 'patients', ['id'])
    op.create_index(op.f('ix_patient_name'), 'patients', ['family_name', 'given_name'])
    op.create_index(op.f('ix_patients_identifier'), 'patients', ['identifier'])
    op.create_index(op.f('ix_patients_birth_date'), 'patients', ['birth_date'])

    # Create encounters table
    op.create_table(
        'encounters',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('patient_id', sa.Integer(), sa.ForeignKey('patients.id', ondelete="CASCADE"), nullable=False),
        sa.Column('start', sa.DateTime(), nullable=False),
        sa.Column('end', sa.DateTime(), nullable=True),
        sa.Column('encounter_class', sa.String(length=64), nullable=False),
    )
    op.create_index(op.f('ix_encounters_id'), 'encounters', ['id'])
    op.create_index(op.f('ix_encounters_patient_id'), 'encounters', ['patient_id'])

def downgrade():
    # Drop encounters first (FK to patients)
    op.drop_index(op.f('ix_encounters_patient_id'), table_name='encounters')
    op.drop_index(op.f('ix_encounters_id'), table_name='encounters')
    op.drop_table('encounters')

    # Then patients and its indexes
    op.drop_index(op.f('ix_patients_birth_date'), table_name='patients')
    op.drop_index(op.f('ix_patients_identifier'), table_name='patients')
    op.drop_index(op.f('ix_patient_name'), table_name='patients')
    op.drop_index(op.f('ix_patients_id'), table_name='patients')
    op.drop_table('patients')
