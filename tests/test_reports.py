import pytest
import tempfile
import os
from reports import generate_median_coffee_report


@pytest.fixture
def sample_csv():
    content = """student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика
Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика
Иван Кузнецов,2024-06-01,600,3.0,15,зомби,Математика
Иван Кузнецов,2024-06-02,700,2.0,18,не выжил,Математика
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(content)
        return f.name


def test_median_report(sample_csv):
    headers, data = generate_median_coffee_report([sample_csv])
    assert headers == ['Студент', 'Медиана трат на кофе (руб)']
    assert len(data) == 2
    assert data[0][0] == 'Иван Кузнецов'      # 650
    assert data[1][0] == 'Алексей Смирнов'    # 475


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        generate_median_coffee_report(['nonexistent.csv'])


def test_empty_files():
    headers, data = generate_median_coffee_report([])
    assert data == [['Нет данных']]