import pytest
import pandas

from delivery_cost import calculate_delivery_cost, DeliveryImpossible


def get_test_data():
    data = pandas.read_csv('test_data.csv', sep=';')
    return list(zip(data['distance'], data['size'], data['is_fragile'], data['load'], data['cost']))


class TestGetPrice:

    def test_base_price(self):
        # Тестирование минимального расстояния с малыми габаритами и обычной загруженностью
        assert calculate_delivery_cost(1) == 400

    @pytest.mark.parametrize("distance, size, is_fragile, load, cost", get_test_data())
    def test_pairwise_positive(self, distance, size, is_fragile, load, cost):
        # Используем классы эквивалентности, граничные значения, и попарное тестирование для
        # проверки позитивных сценариев
        assert calculate_delivery_cost(distance, size, is_fragile, load) == cost

    def test_distance_and_load(self):
        # Тестирование функции с аргументами distance и load
        assert calculate_delivery_cost(distance='3', load='high') == 400

    def test_distance_and_fragility(self):
        # Тестирование функции с аргументами distance и is_fragile
        assert calculate_delivery_cost(distance=20, is_fragile='normal') == 400
        assert calculate_delivery_cost(distance=1, is_fragile='fragile') == 450

    def test_distance_and_size(self):
        # Тестирование функции с аргументами distance и size
        assert calculate_delivery_cost(distance=20, size='small') == 400
        assert calculate_delivery_cost(distance=35, size='large') == 500

    def test_delivery_impossible_01(self):
        with pytest.raises(DeliveryImpossible):
            calculate_delivery_cost(30.01, is_fragile='fragile')

    def test_delivery_impossible_02(self):
        with pytest.raises(DeliveryImpossible):
            calculate_delivery_cost(100, is_fragile='fragile')
