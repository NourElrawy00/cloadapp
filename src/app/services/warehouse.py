from decimal import Decimal
from app.extensions import db
from app.models.warehouse import StockMovement, MovementType, STOCK_IN_TYPES


class WarehouseService:

    @staticmethod
    def apply_movement(item, quantity, unit_price, movement_type, user_id, source_id=None, note=None):
        """
        The single correct way to change stock on a WarehouseItem.
        Updates cached stock, price (if higher), and total_value,
        and creates a StockMovement record — all in the current session.

        Call db.session.commit() after your main operation; this is
        staged in the same transaction.

        Args:
            item          (WarehouseItem)
            quantity      (Numeric): positive = in, negative = out.
            unit_price    (Numeric): price per unit for this movement.
            movement_type (MovementType)
            user_id       (int)
            source_id     (int, optional): FK to the Buy.id or Delivery.id that triggered this.
            note          (str, optional): required context for manual adjustments.

        Returns:
            StockMovement: the created movement record.

        Usage:
            # Receive 10 units at 60.00 — price goes up, updates automatically
            WarehouseService.apply_movement(item, 10, 60.00, MovementType.buy,
                                            user_id=current_user.id, source_id=buy.id)

            # Dispatch 3 units
            WarehouseService.apply_movement(item, -3, item.price, MovementType.delivery,
                                            user_id=current_user.id, source_id=delivery.id)

            # Manual write-off
            WarehouseService.apply_movement(item, -1, item.price, MovementType.adjustment,
                                            user_id=current_user.id, note='Damaged unit')
        """
        qty       = Decimal(str(quantity))
        new_price = Decimal(str(unit_price))
        old_price = Decimal(str(item.price))

        # Only update price on stock-in, and only if the new price is higher
        if movement_type in STOCK_IN_TYPES and qty > 0:
            if new_price > old_price:
                item.price = new_price
            elif new_price < old_price and old_price > 0:
                pass

        new_stock   = item.stock + qty
        new_value   = new_stock * item.price

        movement = StockMovement(
            warehouse_item_id = item.id,
            quantity          = qty,
            unit_price        = new_price,
            total_price       = abs(qty) * new_price,
            movement_type     = movement_type,
            source_id         = source_id,
            user_id           = user_id,
            note              = note,
            stock_after       = new_stock,
            value_after       = new_value,
        )

        item.stock       = new_stock
        item.total_value = new_value

        db.session.add(movement)
        return movement

    @staticmethod
    def recompute_stock(item):
        """
        Recomputes stock and total_value from full movement history.
        Use for periodic reconciliation or after a data integrity check.
        """
        total = db.session.query(
            db.func.coalesce(db.func.sum(StockMovement.quantity), 0)
        ).filter_by(warehouse_item_id=item.id).scalar()

        item.stock       = Decimal(str(total))
        item.total_value = item.stock * Decimal(str(item.price))
        return item.stock

    @staticmethod
    def warehouse_total_value(warehouse):
        """Total monetary value of all active items in a warehouse."""
        return sum(
            item.total_value for item in warehouse.items if not item.deleted
        )