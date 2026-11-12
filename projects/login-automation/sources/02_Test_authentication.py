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



# ======= 기본 설정 ====================== #
BASE_URL = "http://127.0.0.1:5000"
LOGIN_URL = f"{BASE_URL}/login"

CSV_PATH = (
    Path(__file__).parent.parent
    / "01_data"
    / "login_authentication.csv"
)
# CSV 가져오기
with open(CSV_PATH, newline = "", encoding = "utf-8-sig") as file:
    reader = csv.DictReader(file)
    test_data = list(reader)
# ======================================== #


# 서버 테스트 상태 초기화
def reset_test_state():

    response = requests.post(
        f"{BASE_URL}/__test/api/reset",
        json = {"username": "all"},
        timeout = 5
    )

    response.raise_for_status()

    return response.status_code == 200

# 서버 상태 초기화
def get_test_state():

    response = requests.get(
        f"{BASE_URL}/__test/api/state",
        timeout = 5
    )

    response.raise_for_status()
    return response.json()

# 서버 상태 초기화 확인
def check_reset_state():

    state = get_test_state()

    #print("서버 상태 데이터 " , state)

    for account in state["accounts"]:
        if account["failures"] != 0:
            return False
        if account["locked_until"] is not None:
            return False

    return True
    
# 브라우저 로그인 상태 초기화
def reset_browser_state(driver):
    
    driver.get(LOGIN_URL)
    driver.delete_all_cookies()
    driver.get(LOGIN_URL)

# 로그인 요청 발생 여부 확인
def check_login_request(driver, timeout = 5):

    end_time = time.monotonic() + timeout

    while time.monotonic() < end_time:
        logs = driver.get_log("performance")

        for log in logs:
            message = json.loads(log["message"])["message"]

            if message["method"] == "Network.requestWillBeSent":
                request = message["params"]["request"]

                if (
                    request["url"].endswith("/api/login")
                    and request["method"] == "POST"
                ):
                    return True


        time.sleep(0.1)
    return False

# ====================================================
# 검증 함수
# ====================================================

# 정상 로그인 및 메인 페이지 이동 검증
def check_login_success(driver):
    #로그인 요청 확인
    request_found = check_login_request(driver)

    try:
        WebDriverWait(driver, 5).until(
            EC.url_to_be(f"{BASE_URL}/main")
        )
        main_page = True

    except TimeoutException:
        main_page = False

    # 최종 검증
    is_pass = (
        request_found
        and main_page
    )

    print("로그인 요청 발생 : ", request_found)
    print("메인 페이지 이동 : ", main_page)

    return is_pass
        

# 로그인 실패 횟수 생성
def create_login_failures(driver, username, count=2):

    for attempt in range(1, count + 1):

        driver.get(LOGIN_URL)

        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys("Wrong1234!")

        driver.find_element(By.ID, "login-button").click()

        WebDriverWait(driver, 5).until(
            lambda d: get_failure_count(username) >= attempt
        )

        print(f"로그인 실패 횟수 : {get_failure_count(username)}")
        

# 특정 계정의 로그인 실패 횟수 조회
def get_failure_count(username):

    state = get_test_state()
    for account in state["accounts"]:

        if account["username"] == username:
            return account["failures"]

    raise ValueError(f"계정을 찾을 수 없습니다 : {username}")

# 로그인 성공 후 실패 횟수 초기화 검증
def check_failure_count_reset(driver, username):

    # 로그인 성공 및 메인 페이지 이동 확인
    login_success = check_login_success(driver)

    state = get_test_state()

    # 해당 계정의 실패 횟수를 확인
    failed_count = get_failure_count(username)

    is_pass = (
        login_success
        and failed_count == 0
    )

    print("로그인 성공 : ", login_success)
    print("로그인 후 실패 횟수 : ", failed_count)

    return is_pass


# 로그인 인증 실패 및 오류 메시지 검증
def check_login_failure(driver, expected_msg):

    error_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "auth-error"))
    )

    actual_msg = error_element.text

    message_match = actual_msg == expected_msg
    main_page_not_opened = driver.current_url != f"{BASE_URL}/main"

    print("실제 오류 메시지 : ", actual_msg)
    print("오류 메시지 일치 : ", message_match)
    print("메인 페이지 미이동 : ", main_page_not_opened)

    return message_match and main_page_not_opened


# 입력 오류 메시지 우선순위 검증
def check_error_priority(driver, error_field_id, expected_msg):

    error_msg = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, error_field_id))).text

    request_found = check_login_request(driver)

    is_pass = (
        error_msg == expected_msg
        and not request_found
    )

    print("기대 오류 메시지 : " , expected_msg)
    print("실제 오류 메시지 : " , error_msg)
    print("로그인 요청 발생 : " , request_found)

    return is_pass


# 입력 오류 메시지 독립 제거 검증
def check_independent_error_clear(driver, data):

    # 최초 오류 메시지 확인
    id_error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "username-error"))).text

    pw_error = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "password-error"))).text

    initial_match = (
        id_error == data["expected_message"]
        and pw_error == data["expected_other_message"]
    )

    # 수정
    id_input = driver.find_element(By.ID, "username").send_keys("5")

    id_error_removed = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "username-error").text == ""
    )
    # 아이디를 수정했을 때 비밀번호 오류 메시지는 유지중인가 확인
    pw_error_remained = (
        driver.find_element(By.ID, "password-error").text == data["expected_other_message"]
    )

    pw_input = driver.find_element(By.ID, "password").send_keys("5")
    pw_error_removed = WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "password-error").text == ""
    )

    
    is_pass = (
        initial_match
        and id_error_removed
        and pw_error_remained
        and pw_error_removed
    )

    print("최초 오류 메시지 일치 :", initial_match)
    print("아이디 오류 메시지 제거 :", id_error_removed)
    print("비밀번호 오류 메시지 유지 :", pw_error_remained)
    print("비밀번호 오류 메시지 제거 :", pw_error_removed)

    return is_pass
    
                                                                
    


# =============================================================
# 검증 함수 끝
# =============================================================

# 테스트 결과 출력
def print_test_result(is_pass):

    if is_pass:
        print("테스트 결과 : PASS")
        return "PASS"

    else:
        print("테스트 결과 : FAIL")
        return "FAIL"




# 크롬 브라우저 설정
options = webdriver.ChromeOptions()

options.set_capability(
    "goog:loggingPrefs",
    {"performance": "ALL"}
)

#driver = webdriver.Chrome(options=options)

# =========================================
# 테스트 실행
# =========================================

pass_count = 0
fail_count = 0
error_count = 0

driver = None

try:

    driver = webdriver.Chrome(options=options)

    for data in test_data:

        tc_id = data["TC_ID"]
        print(f"\n========= { tc_id } ========")

        try:

            # 테스트 환경 초기화
            reset_browser_state(driver)
            reset_test_state()

            if not check_reset_state():
                raise RuntimeError("서버 상태 초기화 실패")

            print("테스트 환경 초기화 완료")
            # ====================================================================
            # 테스트 사전 조건
            # ====================================================================
            # TC-029 사전 조건 추가
            if tc_id == "TC-029":

                create_login_failures(driver, data["username"], count=2)

                state = get_test_state()
                failed_count = get_failure_count(data["username"])

                if failed_count != 2:
                    raise RuntimeError(f"사전 조건 생성 실패 : 예상 2회 / 실제 {failed_count}회")

                driver.get(LOGIN_URL)
                
            # TC-032 사전 조건 추가
            if tc_id == "TC-032":

                create_login_failures(driver, data["username"], count=5)

                state = get_test_state()

                for account in state["accounts"]:
                    if account["username"] == data["username"]:
                        is_locked = account["locked"]
                        break
                else:
                    raise RuntimeError("계정을 찾을 수 없습니다.")
                if not is_locked:
                    raise RuntimeError("사전 조건 생성 실패 : 계정이 잠기지 않았습니다.")

                print("계정 잠금 사전 조건 생성 완료")

            

            # TC-033 사전 조건 추가
            if tc_id == "TC-033":

                create_login_failures(driver, data["username"], count=4)

                failed_count = get_failure_count(data["username"])

                if failed_count != 4:
                    raise RuntimeError(f"사전 조건 생성 실패 : 예상 4회 / 실제 {failed_count}회")

                print("TC-033 사전 조건 생성 완료")

                error_element = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "auth-error"))
                )

                normal_msg = error_element.text

            #========================================================================

                
            driver.get(LOGIN_URL)
            
            driver.get_log("performance")

            driver.find_element(By.ID, "username").send_keys(data["username"])
            driver.find_element(By.ID, "password").send_keys(data["password"])

            driver.find_element(By.ID, "login-button").click()

            # TC별 검증

            # TC-028 #
            if tc_id == "TC-028":

                is_pass = check_login_success(driver)
                result = print_test_result(is_pass)

            # TC-029 #    
            elif tc_id == "TC-029":

                is_pass = check_failure_count_reset(
                    driver,
                    data["username"]
                )

                result = print_test_result(is_pass)
                                                 
                
            # TC-030 #    
            elif tc_id == "TC-030":

                is_pass = check_login_failure(
                    driver,
                    data["expected_message"]
                )

                result = print_test_result(is_pass)

            # TC-031 #   
            elif tc_id == "TC-031":

                is_pass = check_login_failure(
                    driver,
                    data["expected_message"]
                )

                result = print_test_result(is_pass)

            # TC-032 #    
            elif tc_id == "TC-032":

                is_pass = check_login_failure(
                    driver,
                    data["expected_message"]
                )

                result = print_test_result(is_pass)

            # Tc-033 #
            elif tc_id == "TC-033":

                error_element = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "auth-error"))
                )

                locked_msg = error_element.text

                message_changed = normal_msg != locked_msg

                print("4번째 실패 메시지 : ", normal_msg)
                print("5번째 실패 메시지(잠금) : ", locked_msg)
                print("메시지 갱신 여부 : ", message_changed)

                is_pass = message_changed

                result = print_test_result(is_pass)

            elif tc_id == "TC-034":

                is_pass = check_error_priority(
                    driver,
                    "username-error",
                    data["expected_message"]
                )

                result = print_test_result(is_pass)

            elif tc_id == "TC-035":

                is_pass = check_error_priority(
                    driver,
                    "password-error",
                    data["expected_message"]
                )

                result = print_test_result(is_pass)
                
            elif tc_id == "TC-036":

                is_pass = check_independent_error_clear(
                    driver,
                    data
                )

                result = print_test_result(is_pass)

            
            else:
                print("등록되지 않은 TC")
                result = "NOT_RUN"


            # 결과 집계
            if result == "PASS":
                pass_count += 1
            elif result == "FAIL":
                fail_count += 1
            elif result == "ERROR":
                error_count += 1

        except Exception as e:

            error_count += 1

            print(f"테스트 실행 중 오류 : {e}")
            print("테스트 결과 : ERROR")

finally:

    if driver is not None:
        driver.quit()

    
    print("\n========== 전체 테스트 결과 ==========")
    print("전체 TC :", len(test_data))
    print("PASS :", pass_count)
    print("FAIL :", fail_count)
    print("ERROR :", error_count)
    print("미실행 :", len(test_data) - pass_count - fail_count - error_count)

    input("\n전체 테스트가 종료되었습니다. Enter를 누르면 창이 닫힙니다.")
