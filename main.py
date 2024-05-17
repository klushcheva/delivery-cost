import argparse
import sys
from delivery_cost import calculate_delivery_cost, Size, Fragility, Load, DeliveryImpossible


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Расчёт стоимости доставки')
    parser.add_argument('-d', '--distance', type=float, required=True, help='Расстояние для доставки')
    parser.add_argument('-l', '--large', action='store_true', default=None, help='Габариты груза')
    parser.add_argument('-f', '--fragile', action='store_true', default=None, help='Хрупкость груза')
    parser.add_argument('-o', '--load', type=Load, choices=list(Load), default=Load.NORMAL, help='Загруженность службы доставки')

    return parser.parse_args(argv or sys.argv[1:])


if __name__ == '__main__':
    # Принимаем ввод аргументов для расчета
    args = parse_args()

    try:
        price = calculate_delivery_cost(
            distance=args.distance,
            size=Size.LARGE if args.large else Size.SMALL,
            is_fragile=Fragility.FRAGILE if args.fragile else Fragility.NORMAL,
            load=args.load,
        )
        print(f"Цена доставки составит {price} рублей.")
    except DeliveryImpossible:
        print('Невозможна доставка хрупкого груза на более чем 30 километров')
        exit(2)
