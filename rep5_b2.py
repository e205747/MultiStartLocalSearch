import numpy as np
import random

class MultiStartLocalSearch():
    def __init__(self, n,a,p,c):
        N = n
        self.A = a
        P = p
        C = c

        self.best_result = 0
        best_result_conv = []
        self.worst_result = 0
        worst_result_conv = []
        near_result_conv = []

        #P個の初期解をランダムに生成
        self.solution = N #初期値
        while True:
            random_soluthion = np.random.permutation(N) #Nをランダムに入れ替えたlist
            self.solution = np.vstack([self.solution,random_soluthion]) #配列に追加
            self.solution = list(map(list, set(map(tuple, self.solution)))) #ランダムな初期解が重複してたら削除
            if len(self.solution) == P+1: 
                break
        self.solution = np.delete(self.solution, 0,0) #1行目の初期値を削除

        self.perturbation = np.array(self.solution)
        while True:
            x = random.randint(0,len(N)-1) #ランダムに2箇所選んで入れ替える摂動をC回
            y = random.randint(0,len(N)-1)
            if x != y:
                self.perturbation[0:,x],self.perturbation[0:,y] = self.perturbation[0:,y],self.perturbation[0:,x].copy()
                self.solution = np.vstack([self.solution,self.perturbation]) #配列に追加
            if len(self.solution) == C*P: 
                break

    #近傍解を求めて比較し，最良解と最悪解を求める
    def result(self):

        for i in range(self.solution.shape[0]): 
            self.near_result_conv = self.solution[i]
            self.near_result = 0
            for j in range(self.solution.shape[1]): #列の長さのみ取得
                select = int(self.solution[i,j]) #
                self.near_result = self.near_result + self.A[j,select-1] #
                if i == 0 and j == self.solution.shape[1]-1: #best_scoreの初期値をiループ1週目終了時に設定する
                    self.best_result = self.near_result
                    best_result_conv = self.near_result_conv
            #print("x =",self.near_result_conv,"の時，f(x) =", self.near_result)

            #近傍解を比較し，最良解と最悪解を求める
            if self.best_result >= self.near_result:
                self.best_result = self.near_result
                best_result_conv = self.near_result_conv
            elif self.worst_result <= self.near_result:
                self.worst_result = self.near_result
                worst_result_conv = self.near_result_conv

        print("best_score : x =",best_result_conv,"の時，f(x) =", self.best_result)
        print("worst_score : x =",worst_result_conv,"の時，f(x) =", self.worst_result)

if __name__ == "__main__":
    print('練習課題B')
    #英語=1 、数学=2 、物理=3 、化学=4
    #最適解 Xm[A,B,C,D]=[2,1,3,4]
    #n=[A,B,C,D]=[1,2,3,4]
    #a=問題作成に用する作業時間(行=人，列=教科)
    #p=ランダムに生成する初期解の数
    n=[1,2,3,4]
    a=np.array([[6,1,9,3],[2,5,7,8],[6,3,5,4],[3,5,2,1]], dtype = 'int')
    p=5
    c = 2
    MultiStartLocalSearch(n,a,p,c).result()
