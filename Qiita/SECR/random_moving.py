import random
from scipy.stats import uniform, multivariate_normal

class random_moving:
    """
    特定の中心点を中心としたランダムウォークを行うクラス
    
    Args:
        center_x (float): 中心点のx座標
        center_y (float): 中心点のy座標
        target_variance (float): 目的分布の分散
        proposal_range (float): 提案分布の範囲
        moving_range (float): 移動範囲の半径
    """
    def __init__(self, center_x:float, center_y:float, target_variance:float = 5, proposal_range:float = 5, moving_range:float = 10) -> None:
        self.center_x = center_x
        self.center_y = center_y
        self.target_variance = target_variance
        self.proposal_range = proposal_range
        self.moving_range = moving_range
        return None

    def __normal_pdf(self, x:float, y:float, mean_x:float, mean_y:float, variance:float) -> float:
        """
        2次元正規分布の確率密度を計算
        
        Args:
            x (float): x座標
            y (float): y座標
            mean_x (float): x座標の期待値
            mean_y (float): y座標の期待値
            variance (float): 分散
        
        Returns:
            float: 2次元正規分布の確率密度
        """
        return multivariate_normal.pdf([x, y], mean=[mean_x, mean_y], cov=[[variance, 0], [0, variance]])
    
    def do_random_walk(self, num_steps:int = 48) -> list:
        """
        ランダムウォークを行い、移動後の位置を返す
        
        Args:
            num_steps (int): シミュレーションのステップ数
        
        Returns:
            list: 移動後の位置のリスト
        """
        # 個体の初期位置
        positions_x = random.uniform(-self.moving_range, self.moving_range)
        positions_y = random.uniform(-self.moving_range, self.moving_range)
        
        # 移動後の位置を格納するリスト
        positions_x_list = []
        positions_y_list = []

        for _ in range(num_steps):
            # 現在の位置
            current_x, current_y = positions_x, positions_y
            
            # 提案分布から新しい位置を提案
            proposed_x = current_x + uniform.rvs(-self.proposal_range, 2 * self.proposal_range)
            proposed_y = current_y + uniform.rvs(-self.proposal_range, 2 * self.proposal_range)
            
            # 現在の位置と提案された位置の確率密度を計算
            current_pdf = self.__normal_pdf(current_x, current_y, self.center_x, self.center_y, self.target_variance)
            proposed_pdf = self.__normal_pdf(proposed_x, proposed_y, self.center_x, self.center_y, self.target_variance)
            
            # 受理率を計算
            acceptance_ratio = min(1, proposed_pdf / current_pdf)
            
            # 受理率に基づいて移動を決定
            if random.uniform(0, 1) < acceptance_ratio:
                positions_x, positions_y = proposed_x, proposed_y
            
            # 移動後の位置をリストに追加
            positions_x_list.append(positions_x)
            positions_y_list.append(positions_y)
        
        return positions_x_list, positions_y_list