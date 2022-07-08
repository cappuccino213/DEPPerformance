"""
@File : test_diagnosis_script.py
@Date : 2022/5/18 9:45
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import math

from locust import task, between, constant
from locust import LoadTestShape

from locust_request_encapsulation import *
from pre_request import *
from config import LOAD_SHAPE


class InternalCaller(HttpRequestUser):
	weight = 6
	# wait_time = between(3, 5)
	wait_time = constant(2)  # 每隔两秒钟执行一次任务
	request_header = {"Content-Type": "application/json"}

	# 执行请求前先获取token
	def on_start(self):
		logging.info("获取token.....")
		self.request_header['Authorization'] = get_token()

	# 获取患者基本信息
	@task(1)
	def get_patient_info(self):
		api = '/api/PatientInfo/PatientInfo'
		payload = {
			"OrganizationHISCode": "QWYHZYFZX",
			"systemCode": "HISMZ",
			"MedrecNo": "11111"
		}
		self.http_request(api, headers=self.request_header, api_name='获取患者基本信息', json_body=payload)

	@task(1)
	def get_electronic_info(self):
		api = '/api/Electronic/ElectronicList'
		payload = {
			"organizationHISCode": "QWYHZYFZX",
			"systemCode": "HISMZ",
			"placerOrderNO": "",
			"medrecNo": "2008050778"
		}
		self.http_request(api, headers=self.request_header, api_name='获取电子申请单信息', json_body=payload)

	@task(1)
	def notify_print_result(self):
		api = '/api/Notify/ReportPrintResult'
		payload = {
			"AutoPrinterInfo": {
				"PrinterIP": None,
				"PrintType": 1,
				"PrinterSource": None
			},
			"ExamInfo": {
				"PatientId": None,
				"Name": None,
				"Sex": None,
				"BirthDate": None,
				"PhoneNumber": None,
				"AccessionNumber": "DY021882",
				"ServiceSect": None,
				"ServiceSectID": None,
				"PatientClass": None,
				"ExamDate": None,
				"ResultStatusCode": None,
				"ResultStatus": None,
				"PatientType": None,
				"ExamDeptName": None,
				"ExamDeptID": None,
				"PreliminaryDate": None,
				"AuditDate": None,
				"ReviseDate": None,
				"OrganizationCode": "QWYHZYFZX",
				"Token": None,
				"PartnerId": None
			}
		}
		self.http_request(api, headers=self.request_header, api_name='报告打印结果通知', json_body=payload)

	@task(1)
	def get_report_status(self):
		api = '/api/PrintFilmStatusNotify/ReportStatus'
		payload = {
			"CardNo": "112233",
			"OrganizationCode": "QWYHZYFZX"
		}
		self.http_request(api, headers=self.request_header, api_name='报告状态获取', json_body=payload)

	@task(1)
	def notify_his(self):
		api = '/api/Notify/NotifyHIS'
		payload = {
			"systemCode": "HIS",
			"placerOrderNO": "U0372494",
			"OrganizationCode": "QWYHZYFZX",
			"WorkState": "10",
			"ImagingFinding": "所见",
			"ImagingDiagnosis": "诊断"
		}
		self.http_request(api, headers=self.request_header, api_name='通知HIS接口', json_body=payload)

	@task(1)
	def barcode_convert(self):
		api = '/api/BarCode/Convert'
		payload = {
			"CardNo": "123",
			"CardType": "",
			"CardId": "",
			"OrganizationCode": "QWYHZYFZX"
		}
		self.http_request(api, headers=self.request_header, api_name='条码转化接口', json_body=payload)

	# 执行完任务后执行，每个user执行一次
	def on_stop(self):
		pass


class ThirdCaller(HttpRequestUser):
	weight = 0
	# wait_time = between(3, 5)
	wait_time = constant(2)  # 每隔两秒钟执行一次任务
	request_header = {}

	# 执行请求前先获取token
	def on_start(self):
		logging.info("准备签名头信息.....")
		self.request_header = get_signature_info()

	# 云胶片收费接口
	@task(1)
	def get_patient_info(self):
		api = '/api/ExternalNotify/Charges'
		payload = {
			"Id": "0B21599F-E924-4B8C-A18F-AD9100FAB0F2",
			"Order_id": "16ADD794-762C-443A-B818-AD9100FAB0EB",
			"Transaction_id": "55",
			"Pay_channel": 0,
			"Price": 50,
			"Name": "王五",
			"Organization_id": "QWYHZYFZX",
			"Observation_uid": "120F3BD0-0DE0-4F87-B2F4-ABD100A6A627",
			"Accession_number": "DY021882",
			"Card_no": "1",
			"Patient_id": "CT-009922",
			"Med_rec_no": "0021778"
		}
		self.http_request(api, headers=self.request_header, api_name='云胶片收费接口', json_body=payload)


# 步进加载模式，不支持命令行模式，如果是命令行的话以下需要注释
# class StepLoadShape(LoadTestShape):
# 	"""
# 	A step load shape
# 	Keyword arguments:
# 		step_time -- Time between steps-每步间隔时间
# 		step_load -- User increase amount at each step-每步用户增加数量
# 		spawn_rate -- Users to stop/start per second at every step-每一步用户启动停止的数量/秒
# 		time_limit -- Time limit in seconds-运行限制时间
# 	"""
#
# 	step_time = LOAD_SHAPE['STEP_TIME']
# 	step_load = LOAD_SHAPE['STEP_LOAD']
# 	spawn_rate = LOAD_SHAPE['SPAWN_RATE']
# 	time_limit = LOAD_SHAPE['TIME_LIMIT']
#
# 	def tick(self):
# 		# 运行时间# 运行时间
# 		run_time = self.get_run_time()
#
# 		if run_time > self.time_limit:
# 			return None
# 		current_step = math.floor(run_time / self.step_time) + 1
# 		return current_step * self.step_load, self.spawn_rate


# 单独测试脚本时执行，正式测试运行run.py
def start():
	import subprocess
	cli = f"locust -f test_dep_script.py -H {LOCUST_CONF['TEST_HOST']} --web-host {LOCUST_CONF['SHOW_URL']} -P {LOCUST_CONF['SHOW_PORT']}"
	try:
		cl = subprocess.Popen(cli, stdout=subprocess.PIPE, shell=True)
		print(cl.stdout.readlines())  # 打印控制台信息
	except Exception as e:
		raise str(e)


if __name__ == '__main__':
	start()
