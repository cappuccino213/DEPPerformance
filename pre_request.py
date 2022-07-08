"""
@File : pre_request.py
@Date : 2022/7/7 16:48
@Author: 九层风（YePing Zhang）
@Contact : yeahcheung213@163.com
"""
import requests
import time
import hashlib

TOKEN_HOST = "http://192.168.1.18:8709"


# 获取token值
def get_token():
	token_api = f"{TOKEN_HOST}/Token/RetriveInternal"
	headers = {"Content-Type": "application/json"}
	payload = {
		"ProductName": "eWordDEP",
		"HospitalCode": "QWYHZYFZX",
		"RequestIP": "192.168.1.56"
	}
	res = requests.post(
		url=token_api,
		json=payload,
		headers=headers
	)
	# print(res.json())
	return res.json()['token']


# 获取签名信息
def get_signature_info():
	time_stamp = round(time.time())  # 获取当前时间戳，四舍五入取整
	app_id = "DEP_TEST"
	app_secret = "zMxSYkrW4PanYI+Sj21PN8CKmlv1VoUthADz2rLmUpJ0jfvclj++ah7dcrB8BNFmdAIILcGlT1gFK9pzmTjT/w=="
	signature = f"{app_id}{app_secret}{time_stamp}"
	signature_md5 = hashlib.md5(bytes(signature, encoding='utf-8')).hexdigest().upper()
	# print(signature_md5)
	return {"Sign": signature_md5, "Timestamp": str(time_stamp), "AppID": app_id, "HospitalCode": "QWYHZYFZX"}


if __name__ == "__main__":
	# print(get_token())

	get_signature_info()
