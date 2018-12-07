# Pi-Smart-Mirror
Raspberry pi Smart Mirror

본 과제는 성균관대학교 18년도 2학기 소프트웨어 전용반 종합설계프로젝트 수업에서 만든 prototype일 뿐 상용화 및 기타 목적을 가지고 사용하시면 안됩니다... ㅠㅠ

PyQT를 활용하여 미용실에 특화된 UI를 만들었다.

<img width="508" alt="ui" src="https://user-images.githubusercontent.com/35593401/49628358-03401500-fa27-11e8-9681-2acc3ef0ea86.png">

우측 상단에 있는 카메라는 사진을 찍는 위젯이다.
그 아래에 있는 설정은 관리자 모드다.

좌측 아래에 있는 아이콘은 차례대로:
1. 유저 로그인 및 회원가입
2. 유저 염색
3. 유저 가발 씌우기
4. 유저 얼굴형에 따른 헤어스타일 추천
5. 무료한 시간을 달래기 위한 영상


사용한 라이브러리:

Dlib    - http://dlib.net/

OpenCV  - https://opencv.org/

PyQT    - https://wiki.python.org/moin/PyQt

_____________________________________________

실행 방법:

1. Terminal 3개를 연다.

2. Terminal에 각각 

                  python3 ./main_ui.py
                  
                  python3 ./timer.py
                  
                  python3 ./gif_test.py 
                  
   를 실행한다.
   
3. 기다린다...
