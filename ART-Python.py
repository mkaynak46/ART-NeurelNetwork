# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 22:21:35 2020

@author: Mustafa Kaynak - 15542513
"""

import math
import sys

N = 3 # giriş vektöründeki bileşen sayısı.
M = 3 # Oluşturulacak maksimum küme sayısı.
SIMILARITY = 0.8 # Benzerlik katsayısı
PATTERNS = 3
TRAINING_PATTERNS = 3 #Eğitim için kullanılacak sayı

PATTERN_ARRAY = [[1, 0, 1], 
                 [1, 1, 0], 
                 [0, 0, 1], 
                 ] # Kullanılan Matris

class ART1_Example1:
    def __init__(self, inputSize, numClusters, SIMILARITY, numPatterns, numTraining, patternArray):
        self.mInputSize = inputSize
        self.mNumClusters = numClusters
        self.mSIMILARITY = SIMILARITY
        self.mNumPatterns = numPatterns
        self.mNumTraining = numTraining
        self.mPatterns = patternArray
        
        self.bw = [] # İleri Doğru ağırlıklar.
        self.tw = [] # Geri Doğru ağırlıklar.

        self.f1a = [] # Giriş katmanı.
        self.f1b = [] # Arayüz katmanı.
        self.f2 = []
        return
    
    def initialize_arrays(self):
        #  İleri doğru ağırlık matrisini başlat..
        sys.stdout.write("ileri doğru ağırlıkların değerleri:")
        for i in range(self.mNumClusters):
            self.bw.append([0.0] * self.mInputSize)
            for j in range(self.mInputSize):
                self.bw[i][j] = 1.0 / (1.0 + self.mInputSize)
                sys.stdout.write(str(self.bw[i][j]) + ", ")
            
            sys.stdout.write("\n")
        
        sys.stdout.write("\n")
        
        # Gerid oğru ağırlık matrisini başlat..
        for i in range(self.mNumClusters):
            self.tw.append([0.0] * self.mInputSize)
            for j in range(self.mInputSize):
                self.tw[i][j] = 1.0
                sys.stdout.write(str(self.tw[i][j]) + ", ")
            
            sys.stdout.write("\n")
        
        sys.stdout.write("\n")
        
        self.f1a = [0.0] * self.mInputSize
        self.f1b = [0.0] * self.mInputSize
        self.f2 = [0.0] * self.mNumClusters
        return
    
    def get_vector_sum(self, nodeArray):
        total = 0
        length = len(nodeArray)
        for i in range(length):
            total += nodeArray[i]
        
        return total
    
    def get_maximum(self, nodeArray):
        maximum = 0;
        foundNewMaximum = False;
        length = len(nodeArray)
        done = False
        
        while not done:
            foundNewMaximum = False
            for i in range(length):
                if i != maximum:
                    if nodeArray[i] > nodeArray[maximum]:
                        maximum = i
                        foundNewMaximum = True
            
            if foundNewMaximum == False:
                done = True
        
        return maximum
    
    def test_for_reset(self, activationSum, inputSum, f2Max):
        doReset = False
        
        if(float(activationSum) / float(inputSum) >= self.mSIMILARITY):
            doReset = False # Seçildi
        else:
            self.f2[f2Max] = -1.0 # iptal.
            doReset = True # Reddedildi.
        
        return doReset
    
    def update_weights(self, activationSum, f2Max):
        #  bw(f2Max) yi güncelle
        for i in range(self.mInputSize):
            self.bw[f2Max][i] = (2.0 * float(self.f1b[i])) / (1.0 + float(activationSum))
        
        for i in range(self.mNumClusters):
            for j in range(self.mInputSize):
                sys.stdout.write(str(self.bw[i][j]) + ", ")
            
            sys.stdout.write("\n")
        sys.stdout.write("\n")
        
        # tw(f2Max) yi güncelle
        for i in range(self.mInputSize):
            self.tw[f2Max][i] = self.f1b[i]
        
        for i in range(self.mNumClusters):
            for j in range(self.mInputSize):
                sys.stdout.write(str(self.tw[i][j]) + ", ")
            
            sys.stdout.write("\n")
        sys.stdout.write("\n")
        
        return
    
    def ART1(self):
        inputSum = 0
        activationSum = 0
        f2Max = 0
        reset = True
        
        sys.stdout.write("Başlangıç ART1:\n")
        for k in range(self.mNumPatterns):
            sys.stdout.write("Vektör: " + str(k) + "\n\n")
            
            #  F2 katmanı uyumluluklarını 0.0 olarak başlat
            for i in range(self.mNumClusters):
                self.f2[i] = 0.0
            
            # Deseni () f1 katmanına gir.
            for i in range(self.mInputSize):
                self.f1a[i] = self.mPatterns[k][i]
            
            # Girdi şablonunun toplamını hesapla
            inputSum = self.get_vector_sum(self.f1a)
            sys.stdout.write("Girdi Toplamı (si) = " + str(inputSum) + "\n\n")
            
            # F1 katmanındaki her düğüm için aktivasyonları hesaplayın.
            for i in range(self.mInputSize):
                self.f1b[i] = self.f1a[i]
            
            # F2 katmanındaki her düğüm için net girişi hesaplayın
            for i in range(self.mNumClusters):
                for j in range(self.mInputSize):
                    self.f2[i] += self.bw[i][j] * float(self.f1a[j])
                    sys.stdout.write(str(self.f2[i]) + ", ")
                
                sys.stdout.write("\n")
            sys.stdout.write("\n")
            
            reset = True
            while reset == True:
                # f2 en büyüğünü seç
                f2Max = self.get_maximum(self.f2)
                
                
                for i in range(self.mInputSize):
                    sys.stdout.write(str(self.f1b[i]) + " * " + str(self.tw[f2Max][i]) + " = " + str(self.f1b[i] * self.tw[f2Max][i]) + "\n")
                    self.f1b[i] = self.f1a[i] * math.floor(self.tw[f2Max][i])
                
                #  Girdi şablonunun toplamını hesapla.
                activationSum = self.get_vector_sum(self.f1b)
                sys.stdout.write("Uyumluluk Toplamı (x(i)) = " + str(activationSum) + "\n\n")
                
                reset = self.test_for_reset(activationSum, inputSum, f2Max)
            

            if k < self.mNumTraining:
                self.update_weights(activationSum, f2Max)
            
            sys.stdout.write("Vektör #" + str(k) + " Ait Olduğu Küme => #" + str(f2Max) + "\n\n")
                
        return
    
    def print_results(self):
        sys.stdout.write("Son ağırlık değerleri:\n")
        
        for i in range(self.mNumClusters):
            for j in range(self.mInputSize):
                sys.stdout.write(str(self.bw[i][j]) + ", ")
            
            sys.stdout.write("\n")
        sys.stdout.write("\n")
        
        for i in range(self.mNumClusters):
            for j in range(self.mInputSize):
                sys.stdout.write(str(self.tw[i][j]) + ", ")
            
            sys.stdout.write("\n")
        sys.stdout.write("\n")
        return

if __name__ == '__main__':
    art1 = ART1_Example1(N, M, SIMILARITY, PATTERNS, TRAINING_PATTERNS, PATTERN_ARRAY)
    art1.initialize_arrays()
    art1.ART1()
    art1.print_results()
    
    
