from enum import Enum


class Load(Enum):
    HIGH = 'high'
    VERY_HIGH = 'very_high'
    ELEVATED = 'elevated'
    NORMAL = 'normal'

    def __str__(self):
        return self.value


class Size(Enum):
    LARGE = 'large'
    SMALL = 'small'

    def __str__(self):
        return self.value


class Fragility(Enum):
    FRAGILE = 'fragile'
    NORMAL = 'normal'

    def __str__(self):
        return self.value


# Эксепшен для обработки случаев невозможности доставки
class DeliveryImpossible(Exception):
    def __init__(self, msg):
        self.msg = msg
        print(msg)


# Функция для расчета стоимости
def calculate_delivery_cost(distance, size: Size = Size.SMALL.value, is_fragile: Fragility = Fragility.NORMAL.value,
                            load: Load = Load.NORMAL.value):
    delivery_cost = 0

    if isinstance(distance, str):
        distance = float(distance)

    # Условия для расстояния
    if distance > 30:
        delivery_cost += 300
    elif distance > 10:
        delivery_cost += 200
    elif distance > 2:
        delivery_cost += 100
    elif distance < 0:
        raise DeliveryImpossible("Введите положительное значение дистанции!")
    else:
        delivery_cost += 50

    # Условия для хрукого груза
    if is_fragile == Fragility.FRAGILE.value:
        delivery_cost += 300
        if distance > 30:
            raise DeliveryImpossible("Хрупкие грузы не могут быть доставлены на расстояние более 30 км")

    # Условия для размера груза
    if size == Size.LARGE.value:
        delivery_cost += 200
    elif size == Size.SMALL.value:
        delivery_cost += 100
    else:
        raise DeliveryImpossible("Некорректно указаны габариты груза")

    # Коэффициенты загруженности службы доставки
    load_coef = {
        'very_high': 1.6,
        'high': 1.4,
        'elevated': 1.2,
        'normal': 1.0
    }

    # Применение коэффициента загруженности
    if load in load_coef:
        delivery_cost *= load_coef[load]
    else:
        raise ValueError("Некорректно указана загруженность службы доставки")

    # Если сумма доставки меньше 400, возвращаем 400

    return max(400, round(delivery_cost))
