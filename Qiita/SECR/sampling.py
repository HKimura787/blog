import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from typing import List, Tuple

class sample:
    """
    設定したサンプリング座標の一定の範囲内の点を取得するクラス
    """
    def __init__(self, min_x:float, max_x:float, step_x:float, min_y:float, max_y:float, step_y:float, range:float) -> None:
        self.min_x = min_x
        self.max_x = max_x
        self.step_x = step_x
        self.min_y = min_y
        self.max_y = max_y
        self.step_y = step_y
        self.x_points = np.arange(min_x, max_x, step_x)
        self.y_points = np.arange(min_y, max_y, step_y)
        self.range = range
        return None
    
    def get_sample(self, x_list:List[float], y_list:List[float]) -> Tuple[List[float], List[float]]:
        """
        サンプリング座標の一定の範囲内の点を取得
        
        Args:
            x_list (List[float]): x座標
            y_list (List[float]): y座標

        Returns:
            Tuple[List[float], List[float]]: サンプリング座標の一定の範囲内の点
        """
        tuple_xy = np.array([[x, y] for x in x_list for y in y_list])
        sampling_points = np.array([[x_point, y_point] for x_point in self.x_points for y_point in self.y_points])
        sample_index = np.arange(sampling_points.shape[0])

        # 総当たりで距離を計算
        xx, yy = np.meshgrid(sample_index, sample_index)
        distances = np.linalg.norm(sampling_points[xx] - sampling_points[yy], axis=2)

        # 距離が範囲内の点を取得
        filter_ = distances <= self.range
        filter_diag = np.fill_diagonal(filter_, np.nan)
        distances_sample = distances[filter_diag]
        return distances_sample

        # sample_x = []
        # sample_y = []
        # for x in x_list:
        #     for y in y_list:
        #         for x_point in self.x_points:
        #             for y_point in self.y_points:
        #                 if distance.euclidean([x, y], [x_point, y_point]) <= self.range:
        #                     # print(x, y, x_point, y_point)
        #                     sample_x.append(x)
        #                     sample_y.append(y)
        return sample_x, sample_y

    def plot_sampling_point(self, ax:plt.subplot=None, color='black', size:int=5) -> None:
        """
        サンプリング座標をプロット
        
        Args:
            ax (plt.subplot): サブプロット
            color (str): プロットの色
            size (int): プロットのサイズ
        """
        if ax is None:
            fig, ax = plt.subplots()
        for x in self.x_points:
            for y in self.y_points:
                ax.scatter(x, y, color=color, s=size)
        return None
