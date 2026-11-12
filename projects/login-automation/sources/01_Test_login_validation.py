import csv
import json
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

csv_path = Path(__file__).parent.parent / "01_data" / "login_validation.csv"

with open(csv_path, "r", encoding = "utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    test_data = list(reader)

options = webdriver.ChromeOptions()
options.set_capability("goog:loggingPrefs", {"performance" : "ALL"})

pass_count = 0
fail_count = 0
error_count = 0

driver = webdriver.Chrome(options)


# 로그인 요청 찾기
def check_login_request(driver, timeout=5):
    
    end_time = time.monotonic() + timeout

    while time.monotonic() < end_time:
        
        logs = driver.get_log("performance")

        for log in logs:
            message = json.loads(log["message"])["message"]

            if message["method"] == "Network.requestWillBeSent":
                request = message["params"]["request"]

                if (request["url"].endswith("/api/login")
                    and request["method"] == "POST"):
                        return True

        time.sleep(0.1)

    return False

# 테스트 시작마다 서버 리셋
def reset_test_state():

    url = "http://127.0.0.1:5000/__test/api/reset"

    response = requests.post(
        url,
        json = {"username": "all"},
        timeout = 5
    )

    # 오류 응답을 반환하면 예외 발생
    response.raise_for_status()


# 서버 상태 가져오기
def get_test_state():
    
     url = "http://127.0.0.1:5000/__test/api/state"

     response = requests.get(url, timeout = 5)

     response.raise_for_status()

     return response.json()

# 서버 초기화 상태 검증
def check_reset_state(state):

    for account in state["accounts"]:
        if account["failures"] != 0 or account["locked"] != False:
            return False

    return True


# ==== 테스트 공통화 =====================================================================================

# 1. 입력 길이 검증
def check_input_limit(actual_value, input_value, max_length):
    expected_value = input_value[:max_length]


    print("최대 허용 길이 :", max_length)
    print("기대 입력 길이 :", len(expected_value))
    print("실제 입력 길이 :", len(actual_value))
    print("입력값 일치 여부 :", actual_value == expected_value)
                
    return actual_value == expected_value


# 2. 최소 길이 미만 검증
def check_min_length_error(driver, error_field_id, other_field_id, expected_msg):

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, error_field_id))).text

    other_error_msg = driver.find_element(By.ID, other_field_id).text

    request_found = check_login_request(driver)

    is_pass = (
        error_msg == expected_msg
        and other_error_msg == ""
        and not request_found
    )

    print("기대 메시지 :", expected_msg)
    print("실제 메시지 :", error_msg)
    print("다른 입력란 메시지 : ", other_error_msg)
    print("로그인 요청 발생 :", request_found)
    
    return is_pass


# 3. 최소 길이 검증
def check_min_length_valid(driver, error_field_id):

    error_msg = driver.find_element(By.ID, error_field_id).text

    request_found = check_login_request(driver)

    is_pass = (
        error_msg == ""
        and request_found
    )

    print("입력 길이 오류 메시지 : ", error_msg)
    print("로그인 요청 발생 : ", request_found)
    
    return is_pass

# 4. 최대 길이 검증
def check_max_length_valid(driver, error_field_id, actual_value, expected_value):

    matched_value = actual_value == expected_value

    error_msg = driver.find_element(By.ID, error_field_id).text

    request_found = check_login_request(driver)

    is_pass = (
        matched_value
        and error_msg == ""
        and request_found
    )
    
    print("입력값 일치 여부 : ", matched_value)
    print("길이 오류 메시지 : ", error_msg)
    print("로그인 요청 발생 : ", request_found)
    
    return is_pass

# 5. 아이디의 잘못된 입력 형식 검증
def check_invalid_id_format(driver, actual_id, expected_id, expected_msg, check_value = False):
    
    matched_value = actual_id == expected_id

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "username-error"))).text

    pw_error_msg = driver.find_element(By.ID, "password-error").text

    request_found = check_login_request(driver)

    is_pass = (
        (not check_value or matched_value)
        and error_msg == expected_msg
        and pw_error_msg == ""
        and not request_found
    )
    
    print("입력값 일치 여부 :", matched_value)
    print("기대 오류 메시지 :", expected_msg)
    print("실제 오류 메시지 :", error_msg)
    print("비밀번호 오류 메시지 :", pw_error_msg)
    print("로그인 요청 발생 :", request_found)

    return is_pass

# 6. 비밀번호 입력 형식 오류 검증
def check_invalid_pw_format(driver, actual_pw, expected_pw, expected_msg, check_value = False):
    
    matched_value = actual_pw == expected_pw

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "password-error"))).text

    id_error_msg = driver.find_element(By.ID, "username-error").text

    request_found = check_login_request(driver)

    is_pass = (
        (not check_value or matched_value)
        and error_msg == expected_msg
        and id_error_msg == ""
        and not request_found
    )

    print("입력값 일치 여부 :", matched_value)
    print("기대 오류 메시지 :", expected_msg)
    print("실제 오류 메시지 :", error_msg)
    print("아이디 오류 메시지 :", id_error_msg)
    print("로그인 요청 발생 :", request_found)

    return is_pass


# 7. 필수 입력 오류 및 메시지 제거 검증
def check_required_field_error(driver, field_id, error_field_id, input_value, expected_msg):
    
    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, error_field_id))).text

    request_found = check_login_request(driver)

    input_field = driver.find_element(By.ID, field_id)
    input_field.send_keys(input_value)

    # 오류 메시지 제거 확인
    error_removed = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, error_field_id).text ==""
    )

    is_pass = (
        error_msg == expected_msg
        and not request_found
        and error_removed
    )

    print("기대 오류 메시지 :", expected_msg)
    print("실제 오류 메시지 :", error_msg)
    print("로그인 요청 발생 :", request_found)
    print("오류 메시지 제거 여부 :", error_removed)

    return is_pass

# 8. 동시 미입력 및 오류 메시지 독립 제거 검증
def check_required_both_error(driver, expected_id_msg, expected_pw_msg):
    id_error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "username-error"))).text

    pw_error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "password-error"))).text

    request_found = check_login_request(driver)

    # 아이디 입력 및 메시지 제거 확인
    driver.find_element(By.ID, "username").send_keys("testuser01")

    id_error_removed = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "username-error").text == "")

    # 5. 비밀번호 오류 메시지가 유지되는지 확인
    pw_error_remained = (
        driver.find_element(By.ID, "password-error").text == expected_pw_msg
    )

    driver.find_element(By.ID, "password").send_keys("Test1234!")

    pw_error_removed = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "password-error").text == ""

    )

    is_pass = (
        id_error == expected_id_msg
        and pw_error == expected_pw_msg
        and not request_found
        and id_error_removed
        and pw_error_remained
        and pw_error_removed
    )

    print("아이디 기대 메시지 :", expected_id_msg)
    print("아이디 실제 메시지 :", id_error)
    print("비밀번호 기대 메시지 :", expected_pw_msg)
    print("비밀번호 실제 메시지 :", pw_error)
    print("로그인 요청 발생 :", request_found)
    print("아이디 오류 제거 여부 :", id_error_removed)
    print("비밀번호 오류 유지 여부 :", pw_error_remained)
    print("비밀번호 오류 제거 여부 :", pw_error_removed)

    return is_pass        
    
        
#===============================================================================================

# 검증
def print_test_result(is_pass):
    if is_pass:
        print("테스트 결과 : PASS")
        return "PASS"
    else:
        print("테스트 결과 : FAIL")
        return "FAIL"
        

try:
    for data in test_data:

        try:

            driver.get("http://127.0.0.1:5000/login")

            # 이전 TC의 로그인 쿠키 제거
            driver.delete_all_cookies()

            # 쿠키 삭제 후 로그인 페이지 다시 접근
            driver.get("http://127.0.0.1:5000/login")

            # 테스트 서버 초기화
            reset_test_state()
            

            state = get_test_state()
            if not check_reset_state(state):
                raise RuntimeError("서버 초기화 상태 검증 실패")
            print("\n" + "=" * 30)
            print("서버 초기화 상태 : 정상")
            print("=" * 30)

            # ID, PW 입력
            id_input = driver.find_element(By.ID, "username")
            id_input.send_keys(data["username"])

            actual_id = id_input.get_attribute("value")

            pw_input = driver.find_element(By.ID, "password")
            pw_input.send_keys(data["password"])

            actual_pw = pw_input.get_attribute("value")

            # 로그인 요청 기록 초기화하기
            #driver.execute_script("performance.clearResourceTimings()")

            driver.get_log("performance")

            if data["TC_ID"] not in ("TC-004", "TC-008"):
                login_btn = driver.find_element(By.ID, "login-button")
                login_btn.click()
            print("\n" + "=" * 30)
            print("실행한 TC : ", data["TC_ID"])
            print("=" * 30)
        # ====== TC-001, TC-005 ====== #
            if data["TC_ID"] in ("TC-001", "TC-005"):

                if data["TC_ID"] == "TC-001":
                    error_field_id = "username-error"
                    other_field_id = "password-error"

                else:
                    error_field_id = "password-error"
                    other_field_id = "username-error"

                is_pass = check_min_length_error(
                    driver,
                    error_field_id,
                    other_field_id,
                    data["expected_message"]
                )

                result = print_test_result(is_pass)
                
        # ====== TC-001, TC-005 끝 ====== #


        # ====== TC-002, TC-006 ====== #
            elif data["TC_ID"] in ("TC-002", "TC-006"):

                if data["TC_ID"] == "TC-002":
                    error_field_id = "username-error"

                else:
                    error_field_id = "password-error"

                is_pass = check_min_length_valid(
                    driver,
                    error_field_id
                )

                result = print_test_result(is_pass)


                
        # ====== TC-002, TC-006 끝 ====== #


        # ====== TC-003, TC-007 ====== #
            elif data["TC_ID"] in ("TC-003", "TC-007"):

                if data["TC_ID"] == "TC-003":
                    error_field_id = "username-error"
                    actual_value = actual_id
                    expected_value = data["username"]

                else:
                    error_field_id = "password-error"
                    actual_value = actual_pw
                    expected_value = data["password"]


                is_pass = check_max_length_valid(
                    driver,
                    error_field_id,
                    actual_value,
                    expected_value
                )

                result = print_test_result(is_pass)
                
        # ====== TC-003, TC-007 끝 ====== #

        # ====== TC-004, TC-008 ====== #
            elif data["TC_ID"] in ("TC-004", "TC-008"):

                if data["TC_ID"] == "TC-004":
                    actual_value = actual_id
                    input_value = data["username"]
                    max_length = 15 # 아이디는 15글자까지

                else:
                    actual_value = actual_pw
                    input_value = data["password"]
                    max_length = 20 # 비밀번호는 20글자
                    

                expected_value = input_value[:max_length]

                is_pass = check_input_limit(
                    actual_value,
                    input_value,
                    max_length
                )

                result = print_test_result(is_pass)

        # ====== TC-004, TC-008 끝 ====== #

        # ====== TC-009, TC-012, TC-013, TC-014 ====== #
            elif data["TC_ID"] in ("TC-009", "TC-012", "TC-013", "TC-014"):

                is_pass = check_invalid_id_format(
                    driver,
                    actual_id,
                    data["username"],
                    data["expected_message"],
                    check_value = (data["TC_ID"] == "TC-009")
                )

                result = print_test_result(is_pass)

        # ====== TC-009, TC-012, TC-013, TC-014 끝 ====== #
        

        # ====== TC-010, TC-011 ====== #
            elif data["TC_ID"] in ("TC-010", "TC-011"):

                # 기존 함수로 검증 가능하여 사용
                is_pass = check_min_length_valid(
                    driver,
                    "username-error"
                )

                result = print_test_result(is_pass)

        # ====== TC-010, TC-011 끝 ====== #

        # ====== TC-015 ====== #
            elif data["TC_ID"] == "TC-015":
                is_pass = check_min_length_valid(
                    driver,
                    "password-error"
                )

                result = print_test_result(is_pass)
    
        # ====== TC-015 끝 ====== #

        # ====== TC-016, TC-071, TC-018, TC-019, TC-020, TC-021, TC-022 ====== #
            elif data["TC_ID"] in ("TC-016", "TC-017", "TC-018", "TC-019", "TC-020", "TC-021", "TC-022"):

                is_pass = check_invalid_pw_format(
                    driver,
                    actual_pw,
                    data["password"],
                    data["expected_message"]
                )

                result = print_test_result(is_pass)
        
        # ====== TC-016, TC-071, TC-018, TC-019, TC-020, TC-021, TC-022 끝 ====== #

        # ====== TC-025, TC-026 ====== #
            elif data["TC_ID"] in ("TC-025", "TC-026"):
                if data["TC_ID"] == "TC-025":
                    field_id = "username"
                    error_field_id = "username-error"
                    input_value = "testuser01"
                else:
                    field_id = "password"
                    error_field_id = "password-error"
                    input_value = "Test1234!"

                is_pass = check_required_field_error(
                    driver,
                    field_id,
                    error_field_id,
                    input_value,
                    data["expected_message"]
                )

                result = print_test_result(is_pass)


        # ====== TC-027 ====== #
            elif data["TC_ID"] == "TC-027":

                expected_id_msg, expected_pw_msg = data["expected_message"].split(" / ")

                is_pass = check_required_both_error(
                    driver,
                    expected_id_msg,
                    expected_pw_msg
                )

                result = print_test_result(is_pass)
                
        
        #---------------------------------------------------------------------------
            else:
                raise ValueError(f"구현되지 않은 TC입니다 : {data['TC_ID']}")

            if result == "PASS":
                pass_count += 1
            else:
                fail_count += 1
                
        # ====== 예외 처리 ====== #
        except Exception as e:
            error_count += 1
            print("실행한 TC : ", data["TC_ID"])
            print("테스트 결과 :  Error ")
            print("오류 내용 : ", e)                                        
            
    print("\n========== 테스트 실행 결과 ==========")

    print("전체 TC : ", len(test_data))
    print("PASS : ", pass_count)
    print("FAIL : ", fail_count)
    print("ERROR : ", error_count)
    print("========================================")
    
    input("종료하려면 Enter를 누르세요.")
    
    
finally:
    driver.quit()
