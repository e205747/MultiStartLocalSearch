import numpy as np
import random

class MultiStartLocalSearch():
    def __init__(self, p,n_perturbation,capacity,size,price):
        P = p
        N_perturbation = n_perturbation
        self.Capacity = capacity
        self.Size = size
        self.Price = price
        self.best_price = 0
        self.best_size = 0
        self.best_result_conv = []
        self.worst_price = 0
        self.worst_size = 0
        self.worst_result_conv = []
        self.near_price = 0
        self.near_size = 0
        self.near_result_conv = []
        self.m = len(self.Size)

        print("Capacity = ",self.Capacity)
        print("Size  = ",self.Size)
        print("Price = ",self.Price)
        print("P = ",P)

        #P個の初期解をランダムに生成
        self.solution = np.array([0]*self.m)
        self.zero = np.array([0]*self.m)
        while True:
            random_soluthion = ([random.randint(0, 1) for i in range(self.m)]) #初期解作成
            random_soluthion = np.array(random_soluthion)
            if np.array_equal(random_soluthion,self.zero) == False :
                self.solution = np.vstack([self.solution,random_soluthion]) #配列に追加
                self.solution = list(map(list, set(map(tuple, self.solution)))) #ランダムな初期解が重複してたら削除
                if len(self.solution) == P: 
                    break
        
        #ランダムに2箇所選んで入れ替える摂動をC回
        self.solution = np.array(self.solution)
        self.perturbation = np.array(self.solution)
        while True:
            x = random.randint(0,self.m-1)
            y = random.randint(0,self.m-1)
            if x != y :
                self.perturbation[0:,x],self.perturbation[0:,y] = self.perturbation[0:,y],self.perturbation[0:,x].copy() 
                self.solution = np.vstack([self.solution,self.perturbation]) #配列に追加
            if len(self.solution) == P*N_perturbation: 
                break

    #近傍解を求めて比較し，最良解と最悪解を求める
    def result(self):

        for i in range(self.solution.shape[0]): 
            self.near_result_conv = self.solution[i]
            for j in range(self.solution.shape[1]): #列の長さのみ取得
                if self.solution[i,j] ==1:
                    self.near_price = self.near_price + self.Price[j]
                    self.near_size = self.near_size + self.Size[j]
                    #print(self.Size[j], ":", self.Price[j], j)
                    #best_score，worst_scoreの初期値をiループ1週目終了時に設定する
            if self.worst_price == 0 and self.near_size <= self.Capacity:
                self.best_price = self.near_price
                self.best_size = self.near_size
                self.best_result_conv = self.near_result_conv
                self.worst_price = self.near_price
                self.worst_size = self.near_size
                self.worst_result_conv = self.near_result_conv  

            #近傍解を比較し，最良解と最悪解を求める
            if self.best_price <= self.near_price and self.near_size <= self.Capacity:
                self.best_price = self.near_price
                self.best_size = self.near_size
                self.best_result_conv = self.near_result_conv
                self.best_result_conv = self.near_result_conv
            elif self.worst_price >= self.near_price and self.near_price != 0:
                self.worst_price = self.near_price
                self.worst_size = self.near_size
                self.worst_result_conv = self.near_result_conv   
                
            #print(self.near_result_conv,"の時，price : ", self.near_price,"size : ",self.near_size)
            self.near_price = 0
            self.near_size = 0

        print("best_score : ",self.best_result_conv,"の時，price : ", self.best_price, "size : ",self.best_size)
        print("worst_score :",self.worst_result_conv,"の時，price : ", self.worst_price,"size : ", self.worst_size)

if __name__ == "__main__":

    print('α1')
    p = 40 #初期解の数
    n_perturbation = 2 #摂動の回数
    capacity = 25 #ナップザックの容量
    size=np.array([3,6,5,4,8,5,3,4],dtype='int') #物の大きさ，
    price=np.array([7,12,9,7,13,8,4,5],dtype='int') #値段
    MultiStartLocalSearch(p,n_perturbation,capacity,size,price).result()
    print("*"*80)


    print('β1')
    p = 40 #初期解の数
    n_perturbation = 2 #摂動の回数
    capacity = 55 #ナップザックの容量
    size=np.array([3,6,5,4,8,5,3,4,3,5,6,4,8,7,11,8,14,6,12,4],dtype='int') #物の大きさ
    price=np.array([7,12,9,7,13,8,4,5,3,10,7,5,6,14,5,9,6,12,5,9],dtype='int') #値段
    MultiStartLocalSearch(p,n_perturbation,capacity,size,price).result()
