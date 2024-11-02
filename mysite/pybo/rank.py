import math
from django.utils import timezone
from django.db.models.functions import Now


def hotRank(likes, dislikes, answers):
	l = likes * 1.0
	d = dislikes * 2.0
	a = answers * 1.5
	# age_w = 2.0
	# age = (Now() - create_date)
	rank = (l - d + a)
	return rank
	## 미완(시간 적용)