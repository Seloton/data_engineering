import unittest
import requests
from unittest.mock import patch, MagicMock
from main import CatFactProcessor, APIError


class TestCatFactProcessor(unittest.TestCase):
    # Создаем экземпляр перед каждым тестом
    def setUp(self):
        self.processor = CatFactProcessor()

    @patch('requests.get')
    def test_get_fact_success(self, mock_get):
        # Тест успешного получения факта
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fact": "Cats are awesome!"}
        mock_get.return_value = mock_response
        # Проверка корректного получения факта
        fact = self.processor.get_fact()
        self.assertEqual(fact, "Cats are awesome!")
        self.assertEqual(self.processor.last_fact, "Cats are awesome!")

    @patch('requests.get')
    def test_get_fact_connection_error(self, mock_get):
        # Тест ошибки соединения
        mock_get.side_effect = requests.exceptions.ConnectionError("No internet")
        # Вызываем ошибку APIError
        with self.assertRaises(APIError) as context:
            self.processor.get_fact()
        self.assertIn("Ошибка при запросе к API", str(context.exception))

    @patch('requests.get')
    def test_get_fact_bad_status(self, mock_get):
        # Тест неверного статус-кода
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Server error")
        mock_get.return_value = mock_response
        # Вызываем ошибку APIError
        with self.assertRaises(APIError) as context:
            self.processor.get_fact()
        self.assertIn("Ошибка при запросе к API", str(context.exception))

    def test_get_fact_analysis_empty(self):
        # Тест анализа пустого факта
        analysis = self.processor.get_fact_analysis()
        self.assertEqual(analysis, {"length": 0, "letter_frequencies": {}})

    def test_get_fact_analysis_with_fact(self):
        # Тест анализа существующего факта
        self.processor.last_fact = "Test Cat"
        analysis = self.processor.get_fact_analysis()
        # Проверяем длину и частоту символов
        expected_frequencies = {
            't': 3, 'e': 1, 's': 1, ' ': 1, 'c': 1, 'a': 1
        }

        self.assertEqual(analysis["length"], 8)
        self.assertEqual(analysis["letter_frequencies"], expected_frequencies)

    @patch('requests.get')
    def test_integration_flow(self, mock_get):
        # Интеграционный тест: получение факта и его анализ
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fact": "Cats rule"}
        mock_get.return_value = mock_response
        # Получаем факт
        fact = self.processor.get_fact()
        self.assertEqual(fact, "Cats rule")
        # Анализируем его
        analysis = self.processor.get_fact_analysis()
        expected_frequencies = {
            'c': 1, 'a': 1, 't': 1, 's': 1, ' ': 1, 'r': 1,
            'u': 1, 'l': 1, 'e': 1
        }
        self.assertEqual(analysis["length"], 9)
        self.assertEqual(analysis["letter_frequencies"], expected_frequencies)


if __name__ == '__main__':
    unittest.main()