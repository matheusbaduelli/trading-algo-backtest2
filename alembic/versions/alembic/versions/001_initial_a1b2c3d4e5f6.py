"""Initial

Revision ID: 001_initial
Revises: 
Create Date: 2025-09-26 10:30:45.123456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create symbols table
    op.create_table('symbols',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker', sa.String(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('exchange', sa.String(), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_symbols_id'), 'symbols', ['id'], unique=False)
    op.create_index(op.f('ix_symbols_ticker'), 'symbols', ['ticker'], unique=True)

    # Create prices table
    op.create_table('prices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('open', sa.Float(), nullable=True),
        sa.Column('high', sa.Float(), nullable=True),
        sa.Column('low', sa.Float(), nullable=True),
        sa.Column('close', sa.Float(), nullable=True),
        sa.Column('volume', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('symbol_id', 'date')
    )
    op.create_index(op.f('ix_prices_date'), 'prices', ['date'], unique=False)
    op.create_index(op.f('ix_prices_id'), 'prices', ['id'], unique=False)

    # Create indicators table
    op.create_table('indicators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('params_hash', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('symbol_id', 'date', 'name', 'params_hash')
    )
    op.create_index(op.f('ix_indicators_date'), 'indicators', ['date'], unique=False)
    op.create_index(op.f('ix_indicators_id'), 'indicators', ['id'], unique=False)

    # Create backtests table
    op.create_table('backtests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('ticker', sa.String(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('strategy_type', sa.String(), nullable=True),
        sa.Column('strategy_params_json', sa.Text(), nullable=True),
        sa.Column('initial_cash', sa.Float(), nullable=True),
        sa.Column('commission', sa.Float(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_backtests_id'), 'backtests', ['id'], unique=False)
    op.create_index(op.f('ix_backtests_ticker'), 'backtests', ['ticker'], unique=False)

    # Create job_runs table
    op.create_table('job_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_name', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('finished_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_runs_id'), 'job_runs', ['id'], unique=False)

    # Create trades table
    op.create_table('trades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('backtest_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('side', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('size', sa.Float(), nullable=True),
        sa.Column('commission', sa.Float(), nullable=True),
        sa.Column('pnl', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['backtest_id'], ['backtests.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trades_id'), 'trades', ['id'], unique=False)

    # Create daily_positions table
    op.create_table('daily_positions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('backtest_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('position_size', sa.Float(), nullable=True),
        sa.Column('cash', sa.Float(), nullable=True),
        sa.Column('equity', sa.Float(), nullable=True),
        sa.Column('drawdown', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['backtest_id'], ['backtests.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_positions_id'), 'daily_positions', ['id'], unique=False)

    # Create metrics table
    op.create_table('metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('backtest_id', sa.Integer(), nullable=True),
        sa.Column('total_return', sa.Float(), nullable=True),
        sa.Column('sharpe', sa.Float(), nullable=True),
        sa.Column('max_drawdown', sa.Float(), nullable=True),
        sa.Column('win_rate', sa.Float(), nullable=True),
        sa.Column('avg_trade_return', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['backtest_id'], ['backtests.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('backtest_id')
    )
    op.create_index(op.f('ix_metrics_id'), 'metrics', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order to respect foreign key constraints
    op.drop_index(op.f('ix_metrics_id'), table_name='metrics')
    op.drop_table('metrics')
    
    op.drop_index(op.f('ix_daily_positions_id'), table_name='daily_positions')
    op.drop_table('daily_positions')
    
    op.drop_index(op.f('ix_trades_id'), table_name='trades')
    op.drop_table('trades')
    
    op.drop_index(op.f('ix_job_runs_id'), table_name='job_runs')
    op.drop_table('job_runs')
    
    op.drop_index(op.f('ix_backtests_ticker'), table_name='backtests')
    op.drop_index(op.f('ix_backtests_id'), table_name='backtests')
    op.drop_table('backtests')
    
    op.drop_index(op.f('ix_indicators_id'), table_name='indicators')
    op.drop_index(op.f('ix_indicators_date'), table_name='indicators')
    op.drop_table('indicators')
    
    op.drop_index(op.f('ix_prices_id'), table_name='prices')
    op.drop_index(op.f('ix_prices_date'), table_name='prices')
    op.drop_table('prices')
    
    op.drop_index(op.f('ix_symbols_ticker'), table_name='symbols')
    op.drop_index(op.f('ix_symbols_id'), table_name='symbols')
    op.drop_table('symbols')