class CoreException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)

class RoomFullyBookedException(CoreException):
    detail = "Нет свободных номеров"

class ObjectNotFoundException(CoreException):
    detail = "Объект не найден"
    
class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"
    
class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"

class CheckInDateAfterCheckOutDateException(CoreException):
    # Дата заезда позже даты выезда
    detail = "Дата заезда позже даты выезда"
    
class CheckInDateEqualsCheckOutDateException(CoreException):
    # дата заезда совпадает с датой выезда.
    detail = "дата заезда совпадает с датой выезда."

class UserAlreadyExistsException(CoreException):
    detail = "Пользователь уже существует"

class BookingNotFound(CoreException):
    detail = "Booking not found"
