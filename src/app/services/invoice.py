from decimal import Decimal
from app.extensions import db
from app.models.transactions import Invoice, Payment, InvoiceStatus


class InvoiceService:

    @staticmethod
    def finalise(invoice):
        """
        Lock the invoice total from its current items and move status to issued.
        Call once all InvoiceItems are added and the invoice is ready to send.

        Usage:
            InvoiceService.finalise(invoice)
            db.session.commit()
        """
        invoice.total_amount = sum(
            Decimal(str(item.quantity)) * Decimal(str(item.price_sell))
            for item in invoice.items
        )
        invoice.status = InvoiceStatus.issued

    @staticmethod
    def add_payment(invoice, amount, method, date, user_id, reference=None, note=None):
        """
        Record a payment against an invoice and update its status atomically.
        Raises ValueError if the payment would exceed the remaining balance.

        Args:
            invoice   (Invoice)
            amount    (Numeric): amount being paid.
            method    (PaymentMethod)
            date      (date)
            user_id   (int)
            reference (str, optional): bank transfer ref, cheque number, etc.
            note      (str, optional)

        Returns:
            Payment: the created payment record.

        Usage:
            payment = InvoiceService.add_payment(
                invoice, amount=500, method=PaymentMethod.bank_transfer,
                date=date.today(), user_id=current_user.id, reference='TRF-001'
            )
            db.session.commit()
        """
        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError('Payment amount must be greater than zero.')

        if amount > invoice.remaining_amount:
            raise ValueError(
                f'Payment of {amount} exceeds remaining balance of {invoice.remaining_amount}.'
            )

        payment = Payment(
            invoice_id = invoice.id,
            user_id    = user_id,
            date       = date,
            amount     = amount,
            method     = method,
            reference  = reference,
            note       = note,
        )
        db.session.add(payment)

        # Update invoice status based on new balance
        paid_so_far = invoice.paid_amount + amount
        if paid_so_far >= Decimal(str(invoice.total_amount)):
            invoice.status = InvoiceStatus.paid
        elif paid_so_far > 0:
            invoice.status = InvoiceStatus.partial

        return payment

    @staticmethod
    def mark_overdue(invoice):
        """
        Mark an unpaid or partially paid invoice as overdue.
        Typically called by a scheduled job checking due_date.

        Usage:
            from datetime import date
            if invoice.due_date and invoice.due_date < date.today():
                InvoiceService.mark_overdue(invoice)
                db.session.commit()
        """
        if invoice.status in (InvoiceStatus.issued, InvoiceStatus.partial):
            invoice.status = InvoiceStatus.overdue

    @staticmethod
    def cancel(invoice):
        """
        Cancel an invoice. Cannot cancel a fully paid invoice.

        Usage:
            InvoiceService.cancel(invoice)
            db.session.commit()
        """
        if invoice.status == InvoiceStatus.paid:
            raise ValueError('Cannot cancel a fully paid invoice.')
        invoice.status = InvoiceStatus.cancelled