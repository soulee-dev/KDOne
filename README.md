# KDOne Navien Home Network API Wrapper
경동원 나비엔 홈네트워크 API Wrapper

## 예제
```shell
pip install KDOne
```

```python
from KDOne.api import KDOneAPI

kd_one = KDOneAPI(username='username', password='password')

# 단지 정보를 불러온다
kd_one.get_complexes()

kd_one.login(complex_id='12341234')
# 로그인과 함께 월패드에 인증 코드가 전송된다

certify_number = input('인증번호를 입력하세요: ')
kd_one.certify(certify_number=certify_number)
kd_one.get_token()

# 로그인 후에는 아래와 같이 사용할 수 있다
from KDOne.models.device import DeviceType

devices = kd_one.get_devices(DeviceType.LIGHT)
kd_one.control_device(devices[0], status="On")
kd_one.control_device(devices[0], status="On")

# 엘리베이터 호출
kd_one.call_elevator()
```