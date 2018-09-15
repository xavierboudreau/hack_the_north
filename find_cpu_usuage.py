import psutil
from time import sleep

if __name__ == "__main__":
	while(True):
		print(psutil.cpu_percent(interval=1))
		#sleep(1)