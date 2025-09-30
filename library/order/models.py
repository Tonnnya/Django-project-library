from django.db import models, DataError, transaction

from authentication.models import CustomUser
from book.models import Book
from django.utils import timezone
from datetime import timedelta


class Order(models.Model):
    """
           This class represents an Order. \n
           Attributes:
           -----------
           param book: foreign key Book
           type book: ForeignKey
           param user: foreign key CustomUser
           type user: ForeignKey
           param created_at: Describes the date when the order was created. Can't be changed.
           type created_at: int (timestamp)
           param end_at: Describes the actual return date of the book. (`None` if not returned)
           type end_at: int (timestamp)
           param plated_end_at: Describes the planned return period of the book (2 weeks from the moment of creation).
           type plated_end_at: int (timestamp)
       """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, blank=True)
    plated_end_at = models.DateTimeField(default=None)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'book')

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        :return: book id, book name, book description, book count, book authors
        """
        status = 'returned' if self.end_at else 'active'
        return f'Order {self.pk}: {self.user.email} - {self.book.name} ({status})'

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        """
                :return: order id, book id, user id, order created_at, order end_at, order plated_end_at
                :Example:
                | {
                |   'id': 8,
                |   'book': 8,
                |   'user': 8',
                |   'created_at': 1509393504,
                |   'end_at': 1509393504,
                |   'plated_end_at': 1509402866,
                | }
                """
        return {
            'id': self.id,
            'book': self.book.id,
            'user': self.user.id,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
            'plated_end_at': int(self.plated_end_at.timestamp()) if self.plated_end_at else None,
        }

    @property
    def is_active(self):
        '''Check if order is active (not returned).'''
        return self.end_at is None

    @property
    def is_overdue(self):
        '''Check if order is overdue.'''
        if self.is_active and self.plated_end_at:
            return timezone.now() > self.plated_end_at
        return False

    @property
    def days_remaining(self):
        '''Calculate days remaining until due date.'''
        if self.is_active and self.plated_end_at:
            delta = self.plated_end_at - timezone.now()
            return max(0, delta.days)
        return 0

    @staticmethod
    def create(user, book, plated_end_at=None):
        try:
            if plated_end_at is None:
                plated_end_at = timezone.now() + timedelta(days=14)

            if book.count <= 0:
                raise ValueError('Book is not available')

            existing_order = Order.objects.filter(
                user=user,
                book=book,
                end_at__isnull=True).first()

            if existing_order:
                raise ValueError('User already has an active order for this book')

            with transaction.atomic():
                order = Order(
                    user=user,
                    book=book,
                    plated_end_at=plated_end_at,
                )
                order.save()

                book.count -= 1
                book.save()

                return order
        except (ValueError, DataError) as e:
            print(f'Error creating order: {e}')
            return None
        except Exception as e:
            print(f'Unexpected error creating order: {e}')
            return None

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at

        if end_at is not None:
            if self.end_at is None and end_at is not None:
                with transaction.atomic():
                    self.end_at = end_at
                    self.book.count += 1
                    self.book.save()
                    self.save()
            else:
                self.end_at = end_at
                self.save()
        else:
            self.save()

    def return_book(self):
        if self.is_active:
            self.update(end_at=timezone.now())

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at__isnull=True)

    @staticmethod
    def get_active_orders():
        """Get all active orders"""
        return Order.objects.filter(end_at__isnull=True)

    @staticmethod
    def get_returned_orders():
        """Get all returned orders"""
        return Order.objects.filter(end_at__isnull=False)

    @staticmethod
    def delete_by_id(order_id):
        try:
            order = Order.objects.get(pk=order_id)

            if order.is_active:
                with transaction.atomic():
                    order.book.count += 1
                    order.book.save()
                    order.delete()
            else:
                order.delete()
            return True
        except Order.DoesNotExist:
            return False
        except Exception as e:
            print(f'Error deleting order: {e}')
            return False
