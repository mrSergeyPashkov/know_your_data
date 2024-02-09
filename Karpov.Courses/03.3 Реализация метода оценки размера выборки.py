
import numpy as np
import pandas as pd
from pydantic import BaseModel
from scipy import stats

class Design(BaseModel):
    """Дата-класс с описание параметров эксперимента.
    
    statistical_test - тип статтеста. ['ttest']
    effect - размер эффекта в процентах
    alpha - уровень значимости
    beta - допустимая вероятность ошибки II рода
    """
    statistical_test: str
    effect: float
    alpha: float
    beta: float

def estimate_sample_size(self, metrics, design):
        """Оцениваем необходимый размер выборки для проверки гипотезы о равенстве средних.
        
        Для метрик, у которых для одного пользователя одно значение просто вычислите размер групп по формуле.
        Для метрик, у которых для одного пользователя несколько значений (например, response_time),
            вычислите необходимый объём данных и разделите его на среднее количество значений на одного пользователя.
            Пример, если в таблице metrics 1000 наблюдений и 100 уникальных пользователей, и для эксперимента нужно
            302 наблюдения, то размер групп будет 31, тк в среднем на одного пользователя 10 наблюдений, то получится
            порядка 310 наблюдений в группе.

        :param metrics (pd.DataFrame): датафрейм со значениями метрик из MetricsService.
            columns=['user_id', 'metric']
        :param design (Design): объект с данными, описывающий параметры эксперимента
        :return (int): минимально необходимый размер групп (количество пользователей)
        """
        effect = design.effect
        alpha = design.alpha
        beta = design.beta
        std = np.std(metrics['metric'].values)
        mean = np.mean(metrics['metric'].values)
        epsilon = effect / 100 * mean
        coef = metrics['user_id'].nunique() / len(metrics)

        t_alpha = stats.norm.ppf(1 - alpha / 2, loc=0, scale=1)
        t_beta = stats.norm.ppf(1 - beta, loc=0, scale=1)
        z_scores_sum_squared = (t_alpha + t_beta) ** 2
        sample_size = int(
            np.ceil(
                z_scores_sum_squared * (2 * std ** 2) / (epsilon ** 2) * coef
            )
        )
        return sample_size