import os
import sys
from decimal import Decimal

from .functions import rev_comp

class RBSscorer():
	def __init__(self, dna):
		background = [1] * 28
		for i, base in enumerate(dna):
			background[self.score(dna[i:i+21])] += 1
			background[self.score(rev_comp(dna[i:i+21]))] += 1
		y = Decimal(sum(background))
		background[:] = [x/y for x in background]
		self.background = background	
		self.observed = [1] * 28

	def add(self, seq):
		self.observed[self.score(seq)] += 1

	def weight(self, seq):
		y = Decimal(sum(self.observed))
		observed = [x/y for x in self.observed]
		return observed[self.score(seq)] / self.background[self.score(seq)]

	def score(self, seq):
		s = seq[::-1]
		score = 0

		if 'GGAGGA' in (s[5:11],s[6:12],s[7:13],s[8:14],s[9:15],s[10:16]):
			score = 27
		elif 'GGAGGA' in (s[3:9],s[4:10]):
			score = 26
		elif 'GGAGGA' in (s[11:17],s[12:18]):
			score = 25
		elif 'GGAGG' in (s[5:10],s[6:11],s[7:12],s[8:13],s[9:14],s[10:15]):
			score = 24
		elif 'GGAGG' in (s[3:8],s[4:9]):
			score = 23
		elif 'GAGGA' in (s[5:10],s[6:11],s[7:12],s[8:13],s[9:14],s[10:15]):
			score = 22
		elif 'GAGGA' in (s[3:8],s[4:9]):
			score = 21
		elif 'GAGGA' in (s[11:16],s[12:17]) or 'GGAGG' in (s[11:16],s[12:17]):
			score = 20
		elif 'GGACGA' in (s[5:11],s[6:12],s[7:13],s[8:14],s[9:15],s[10:16]):
			score = 19
		elif 'GGATGA' in (s[5:11],s[6:12],s[7:13],s[8:14],s[9:15],s[10:16]):
			score = 19
		elif 'GGAAGA' in (s[5:11],s[6:12],s[7:13],s[8:14],s[9:15],s[10:16]):
			score = 19
		elif 'GGCGGA' in (s[5:11],s[6:12],s[7:13],s[8:14],s[9:15],s[10:16]):
			score = 19
		elif 'GGGGGA' in (s[5:11],s[6:12],s[7:13],s[8:14],s[9:15],s[10:16]):
			score = 19
		elif 'GGTGGA' in (s[5:11],s[6:12],s[7:13],s[8:14],s[9:15],s[10:16]):
			score = 19
		elif 'GGAAGA' in (s[3:9],s[4:10]) or 'GGATGA' in (s[3:9],s[4:10]) or 'GGACGA' in (s[3:9],s[4:10]):
			score = 18
		elif 'GGTGGA' in (s[3:9],s[4:10]) or 'GGGGGA' in (s[3:9],s[4:10]) or 'GGCGGA' in (s[3:9],s[4:10]):
			score = 18
		elif 'GGAAGA' in (s[11:17],s[12:18]) or 'GGATGA' in (s[11:17],s[12:18]) or 'GGACGA' in (s[11:17],s[12:18]):
			score = 17
		elif 'GGTGGA' in (s[11:17],s[12:18]) or 'GGGGGA' in (s[11:17],s[12:18]) or 'GGCGGA' in (s[11:17],s[12:18]):
			score = 17
		elif 'GGAG' in (s[5:9],s[6:10],s[7:11],s[8:12],s[9:13],s[10:14]):
			score = 16
		elif 'GAGG' in (s[5:9],s[6:10],s[7:11],s[8:12],s[9:13],s[10:14]):
			score = 16
		elif 'AGGA' in (s[5:9],s[6:10],s[7:11],s[8:12],s[9:13],s[10:14]):
			score = 15
		elif 'GGTGG' in (s[5:10],s[6:11],s[7:12],s[8:13],s[9:14],s[10:15]):
			score = 14
		elif 'GGGGG' in (s[5:10],s[6:11],s[7:12],s[8:13],s[9:14],s[10:15]):
			score = 14
		elif 'GGCGG' in (s[5:10],s[6:11],s[7:12],s[8:13],s[9:14],s[10:15]):
			score = 14
		elif 'AGG' in (s[5:8],s[6:9],s[7:10],s[8:11],s[9:12],s[10:13]):
			score = 13
		elif 'GAG' in (s[5:8],s[6:9],s[7:10],s[8:11],s[9:12],s[10:13]):
			score = 13
		elif 'GGA' in (s[5:8],s[6:9],s[7:10],s[8:11],s[9:12],s[10:13]):
			score = 13
		elif 'AGGA' in (s[11:15],s[12:16]) or 'GAGG' in (s[11:15],s[12:16]) or 'GGAG' in (s[11:15],s[12:16]):
			score = 12
		elif 'AGGA' in (s[3:7],s[4:8]) or 'GAGG' in (s[3:7],s[4:8]) or 'GGAG' in (s[3:7],s[4:8]):
			score = 11
		elif 'GAGGA' in (s[13:18],s[14:19],s[15:20]) or 'GGAGG' in (s[13:18],s[14:19],s[15:20]) or 'GGAGGA' in (s[13:19],s[14:20],s[15:21]):
			score = 10
		elif 'GAAGA' in (s[5:10],s[6:11],s[7:12],s[8:13],s[9:14],s[10:15]):
			score = 9
		elif 'GATGA' in (s[5:10],s[6:11],s[7:12],s[8:13],s[9:14],s[10:15]):
			score = 9
		elif 'GACGA' in (s[5:10],s[6:11],s[7:12],s[8:13],s[9:14],s[10:15]):
			score = 9
		elif 'GGTGG' in (s[3:8],s[4:9]) or 'GGGGG' in (s[3:8],s[4:9]) or 'GGCGG' in (s[3:8],s[4:9]):
			score = 8
		elif 'GGTGG' in (s[11:16],s[12:17]) or 'GGGGG' in (s[11:16],s[12:17]) or 'GGCGG' in (s[11:16],s[12:17]):
			score = 7
		elif 'AGG' in (s[11:14],s[12:15]) or 'GAG' in (s[11:14],s[12:15]) or 'GGA' in (s[11:14],s[12:15]):
			score = 6
		elif 'GAAGA' in (s[3:8],s[4:9]) or 'GATGA' in (s[3:8],s[4:9]) or 'GACGA' in (s[3:8],s[4:9]):
			score = 5
		elif 'GAAGA' in (s[11:16],s[12:17]) or 'GATGA' in (s[11:16],s[12:17]) or 'GACGA' in (s[11:16],s[12:17]):
			score = 4
		elif 'AGGA' in (s[13:17],s[14:18],s[15:19]) or 'GAGG' in (s[13:17],s[14:18],s[15:19]) or 'GGAG' in (s[13:17],s[14:18],s[15:19]):
			score = 3
		elif 'AGG' in (s[13:16],s[14:17],s[15:18]) or 'GAG' in (s[13:16],s[14:17],s[15:18]) or 'GGA' in (s[13:16],s[14:17],s[15:18]):
			score = 2
		elif 'GGAAGA' in (s[13:19],s[14:20],s[15:21]) or 'GGATGA' in (s[13:19],s[14:20],s[15:21]) or 'GGACGA' in (s[13:19],s[14:20],s[15:21]):
			score = 2
		elif 'GGTGG' in (s[13:18],s[14:19],s[15:20]) or 'GGGGG' in (s[13:18],s[14:19],s[15:20]) or 'GGCGG' in (s[13:18],s[14:19],s[15:20]):
			score = 2
		elif 'AGG' in (s[3:6],s[4:7]) or 'GAG' in (s[3:6],s[4:7]) or 'GGA' in (s[3:6],s[4:7]):
			score = 1
		return score


