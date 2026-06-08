import logging

import gevent
from sqlalchemy import event
from sqlalchemy.pool import Pool

from dify_app import DifyApp
from models.engine import db

logger = logging.getLogger(__name__)

# Global flag to avoid duplicate registration of event listener
_gevent_compatibility_setup: bool = False


def _disable_dm_returning_support() -> None:
    """Disable SQLAlchemy RETURNING paths for the DM dialect.

    dmSQLAlchemy currently advertises RETURNING support, but its compiler implementation is
    incompatible with SQLAlchemy 2.x default-fetch compilation. Dify generates UUIDs and
    tolerates post-fetching defaults, so disabling implicit RETURNING keeps inserts portable.
    """
    dialect = db.engine.dialect
    if dialect.name != "dm":
        return

    dialect.insert_returning = False
    dialect.update_returning = False
    dialect.delete_returning = False
    dialect.insert_executemany_returning = False


def _safe_rollback(connection):
    """Safely rollback database connection.

    Args:
        connection: Database connection object
    """
    try:
        connection.rollback()
    except Exception:  # pylint: disable=broad-exception-caught
        logger.exception("Failed to rollback connection")


def _setup_gevent_compatibility():
    global _gevent_compatibility_setup  # pylint: disable=global-statement

    # Avoid duplicate registration
    if _gevent_compatibility_setup:
        return

    @event.listens_for(Pool, "reset")
    def _safe_reset(dbapi_connection, connection_record, reset_state):  # pyright: ignore[reportUnusedFunction]
        if reset_state.terminate_only:
            return

        # Safe rollback for connection
        try:
            hub = gevent.get_hub()
            if hasattr(hub, "loop") and getattr(hub.loop, "in_callback", False):
                gevent.spawn_later(0, lambda: _safe_rollback(dbapi_connection))
            else:
                _safe_rollback(dbapi_connection)
        except (AttributeError, ImportError):
            _safe_rollback(dbapi_connection)

    _gevent_compatibility_setup = True


def init_app(app: DifyApp):
    db.init_app(app)
    _setup_gevent_compatibility()

    # Eagerly build the engine so pool_size/max_overflow/etc. come from config
    try:
        with app.app_context():
            _ = db.engine  # triggers engine creation with the configured options
            _disable_dm_returning_support()
    except Exception:
        logger.exception("Failed to initialize SQLAlchemy engine during app startup")
