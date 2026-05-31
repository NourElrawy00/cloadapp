from app.extensions import db
from app.models.log import Logs, LogAction, LogEntity


class LogService:

    @staticmethod
    def record(action, entity, target_id, user_id, before=None, after=None):
        """
        Stage a log entry in the current session.
        Committed as part of the same transaction as the main operation —
        if the transaction rolls back, the log rolls back too.

        Only include fields that actually changed in before/after.

        Args:
            action    (LogAction)
            entity    (LogEntity)
            target_id (int)
            user_id   (int)
            before    (dict, optional): field values before the change.
            after     (dict, optional): field values after the change.

        Returns:
            Logs: the staged log entry.

        Usage:
            # Create
            LogService.record(LogAction.create, LogEntity.buy, buy.id, current_user.id,
                              after={'reference': buy.reference, 'supplier_id': buy.supplier_id})

            # Update — only changed fields
            LogService.record(LogAction.update, LogEntity.invoice, invoice.id, current_user.id,
                              before={'status': old_status.value},
                              after={'status': invoice.status.value})

            # Price change
            LogService.record(LogAction.update, LogEntity.buy, buy_item.buy_id, current_user.id,
                              before={'price_buy': float(old_price)},
                              after={'price_buy': float(buy_item.price_buy)})

            # Delete
            LogService.record(LogAction.delete, LogEntity.client, client.id, current_user.id,
                              before={'name': client.name})

            # Restore
            LogService.record(LogAction.restore, LogEntity.client, client.id, current_user.id,
                              before={'deleted': True}, after={'deleted': False})

            db.session.commit()
        """
        diff = {}
        if before:
            diff['before'] = before
        if after:
            diff['after'] = after

        entry = Logs(
            user_id       = user_id,
            action        = action,
            target_entity = entity,
            target_id     = target_id,
            diff          = diff or None,
        )
        db.session.add(entry)
        return entry