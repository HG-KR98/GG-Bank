# GG팀 프로젝트

### 프로젝트 주제

소통과 편의성에 중점을 맞춘 서비스

# 1. 팀원 정보 및 업무 분담 내역

### 팀원 : 차상곤(팀장), 김헌규(팀원)

### 업무 분담 내역

주로 프론트와 백을 나누기 보다는 기능별로 작업을 수정하였지만 중간중간에 일정 조율에 따라 프론트와 백을 나누기도 하였습니다.

하지만 작업이 겹친 비율이 작기 때문에 주로 담당한 파트를 기준으로 작성하였습니다.

1. 로그인, 로그아웃 기능 (김헌규)
2. 회원가입 (김헌규)
3. 예적금 데이터 50개 이상 가져오기 (김헌규)
4. 예적금 상품 조회 (김헌규)
5. 예적금 상세 목록 조회 (김헌규)
6. 커뮤니티 게시글 기능 (김헌규)
7. 커뮤니티 댓글 기능 (차상곤)
8. 환율 계산 기능 (차상곤)
9. 프로필 기능 (차상곤)
10. 주변 은행 검색 기능 (차상곤)
11. 금융 상품 추천 알고리즘 (차상곤)
12. AI 추천 / 검색 서비스 기능 (차상곤)

# 2. 설계 내용(아키텍처 등) 및 실제 구현 정도

1. 우선 사용한 기술에는 프론트 엔드에는 vue3와 bootstrap 프레임워크를 사용하였고 백엔드에는 django와 DRF를 사용하였고 챗봇 구현에는 openAI API를 프론트엔드에서 백엔드로 요청을 보내는 것은 axios를 마지막으로 백엔드에서 가져온 데이터를 중앙에서 저장하고 관리하기 위해 pinia를 사용하였습니다.

# 로그인, 로그아웃, 회원가입

1. 로그인, 로그아웃, 회원가입 기능에서는 우선 user모델을 커스텀하기 위해 AbstractUser를 이용하여 기본적으로 입력해야하는 아이디, 비밀번호, 이메일 등 이외에 휴대폰 번호, 이름, 그리고 성별, 생년월일, 자산 정보를 입력할 수 있도록 설계하였습니다.

2. 그 다음 원래 로그인 설정에서 아무것도 안하게 되면 dj_rest_auth의 기본 설정에 의해 아이디, 비밀번호 이외에 이메일을 입력하게 되어있는데 이메일을 입력하도록 하지 않기 위해서 LoginSerializer로 로그인을 커스텀하여 email = None을 사용해 email 입력을 받지 않도록 설계하였습니다.

3. 마지막으로 로그아웃은 페이지의 오른쪽 상단에 고정적으로 모든 페이지에서 볼 수 있도록 버튼을 배치하였고 이는 App.vue에서 navBar에 배치하도록 설계하였습니다. 이것은 position에서 absolute로 위치를 고정시켰습니다.

# 메인 페이지

1. 다음으로 메인페이지에는 총 3개의 블록으로 구성하였는데 우선 페이지의 중앙에는 페이지의 분위기를 나타내도록 carousel을 이용해 3개의 이미지가 일정시간이 지나면 바뀌도록 설계하였고 오른쪽 하단의 블록에는 현재의 조회수 순으로 현재 인기글을 출력하도록 구성하였습니다. 마지막으로 왼쪽 하단 블록에는 챗봇 대화창을 넣었습니다.

2. 보통의 사이트에는 오른쪽 하단에 고정적으로 작은 버튼을 펼쳐야 보이기 때문에 사용자의 눈에 잘 안보일 수 있기 때문에 메인 페이지에 배치를 하여 메인 페이지에 들어오자마자 사용자들이 챗봇을 바로 확인할 수 있도록 설계하였습니다.

# 예적금 금리 비교

1. 예적금 금리 비교 기능에서는 먼저 데이터를 가져올 때는 금융상품통합비교공시 API를 통해 백엔드로 가져와서 django의 모델과 drf의 serializer를 이용해 데이터의 crud를 수행할 수 있도록 구현하였습니다. 프론트엔드에서는 상품별 비교 페이지로 접속을 하면 OnMounted를 이용해 store에 설정해둔 함수를 실행시켜 axios 요청을 통해 저장을 하였습니다.

2. 예적금 금리 비교 전체 조회는 navBar에 있는 상품별 비교 탭을 통해 접근할 수 있으며 경로로 접근하면 onMounted를 통해 저장소에 있는 예적금 정보들을 가져와 출력을 하도록 설계하였습니다. 전체 조회는 데이터가 많기 때문에 스크롤바를 구현하여 사용자가 굳이 페이지의 스크롤을 안내리고 이용할 수 있도록 하였습니다. 그리고 이자율을 6개월, 12개월, 24개월, 36개월에 해당하는 데이터를 가져올 때 데이터를 이미 상품과 옵션을 따로 저장을 해놨기 때문에 역참조를 해서 가져오려고 했으나 옵션의 구조가 같은 상품에 여러 기간과 이자율로 이루어져 있기 때문에 가져오기가 까다로워 함수를 하나 더 만들어서 가공을 하여 가져왔습니다. 그 결과 깔끔하게 조회 목록을 출력할 수 있었습니다. 또한 은행별로 검색할 수 있도록 좌측에 검색 기능을 구현하여 은행회사에 따라 그 은행의 금융상품들을 조회할 수 있도록 하였습니다.

3. 상품 상세 조회에서는 ModelSerializer와 view함수를 통해 상세 조회를 할 수 있도록 설계하였으며 프론트엔드에서는 기존에 목록을 조회할 때 사용했던 store에 저장되어있는 리스트를 가져와 find를 값을 가져왔습니다. 그 다음 가입하기 기능을 구현하기 위해서 백엔드에서 포트폴리오 모델과 serializer를 만들어 사용자가 선택한 상품이 저장되도록 구현하였습니다. 그리고 중복 가입을 막기 위해 프론트엔드에서 백엔드로 요청을 보내 포트폴리오 리스트를 가져와서 그 리스트에 있으면 이미 가입된 상품이라고 공지를 하고 없으면 가입되도록 구현하였습니다. 또한 가입하기 버튼은 store에 저장된 로그인 정보를 이용해 로그인이 되어 있을 경우만 가입하기 버튼이 뜰 수 있도록 설계하였습니다.

- 그리고 일정상의 이슈로 메일 서비스는 구현하지 못했습니다.

# 환율 계산기 ★

### 기능 : 한국 화폐 <-> 외국 화폐로의 환전

1. OnMounted 기능을 활용해서 환율 페이지로 접속시 환율 데이터 API요청을 보내어 DB에 저장하게 됩니다.<br>이 때, 이미 정보가 존재한다면 다시 요청을 보내지 않게 처리해주어야 오류가 발생하지 않습니다.

2. input 이벤트가 장착된 input 태그의 값에 변동이 생길 때마다 select의 value 값으로 지정된 국가화폐코드(미국의 경우 USD)를 이용해서 get axios요청을 보내고, Back-End 에서 Exchange모델의 환율을 조회합니다.

3. 환율과 variable routing을 통해 보내진 돈의 금액을 곱(또는 나눗셈)을 통해서 계산된 값을 반환해서 출력합니다.

### 어려웠던 점

1. 한국 화폐 -> 외국 화폐로의 환전 기능만을 구현했습니다. 위의 기능을 구현했다면 외국 화폐 -> 외국 화폐의 기능도 구현하기는 매우 쉽지만(그냥 한국 돈으로 환전하는 한 번의 과정만 더 거치면 됩니다.), 부정확도가 매우 높을 것 같아서 굳이 안 하는 게 낫다고 판단해서 하지 않았습니다.

2. value 값은 실제로 "디르함 (AED)"와 같은 형태로 적혀 있었는데,
   디르함은 한국어로 읽었을 때의 화폐단위인데,
   달러,엔,유로 등과 같이 널리 알려진 화폐의 단위 외에는 대중들이 모를 가능성이 높기 때문에 단위에 같이 적어주었어야 했습니다.
   그런데 이 부분이 조금 문제가 발생했습니다. 띄어쓰기를 같이 varial routing에는 활용이 바로 할 수 없었는데 인코딩(띄어쓰기->%20)-디코딩(%20->띄어쓰기)이 필요했습니다.
   그러나 검색을 해보니 JS문법에서도 파이썬의 split과 비슷한 문법이 있었고,
   그 덕분에 AED만을 추출해서 변수로 넘길 수 있었고, value 값은 그대로 화폐의 단위로 표시할 수 있었습니다.

# 근처 은행 검색

### 기능 : 원하는 위치의 특정(또는 모든) 은행 검색 기능 <br>& 현재 위치 근처의 특정(또는 모든) 은행 검색 기능<br>

### 동작방식

1. 데이터 초기화 및 컴포넌트 마운트<br>
   데이터 객체를 초기화하고, 컴포넌트가 마운트될 때 카카오 맵 스크립트를 로드하여 지도를 초기화합니다.

2. 시/도, 시/군/구 선택 시 목록 업데이트<br>
   사용자가 시/도를 선택하면 해당 시/도의 시/군/구 목록을 업데이트합니다.<br>
   사용자가 시/군/구를 선택하면 해당 시/군/구의 읍/면/동 목록을 업데이트합니다.

3. 카카오 스크립트 로드<br>
   카카오 맵 API 스크립트를 동적으로 로드하고, 로드가 완료되면 지도를 초기화합니다.

4. 지도 초기화<br>
   지도를 초기화하고, 장소 검색 객체를 생성합니다.

5. 지정한 위치의 은행 검색<br>
   사용자가 선택한 옵션들을 기반으로 검색 쿼리를 생성하고, 해당 위치의 은행을 검색합니다.<br>
   이 때, 검색 결과 중에서 은행 이름이 포함된 항목만 필터링하여 표시합니다.

6. 현재 위치 근처의 은행 검색<br>
   사용자의 현재 위치를 가져와서 해당 위치를 중심으로 반경 2km이내의 은행을 검색합니다.<br>
   검색 결과를 지도에 마커로 표시하고, 마커를 클릭하면 인포윈도우(은행의 이름을 표시하는 창)를 추가합니다.

7. 지도에 표시된 모든 마커와 인포윈도우 제거<br>
   새로운 검색을 하면 기존에 지도에 표시돼 있던 마커와 인포윈도우를 모두 제거합니다.

### 어려웠던 점

1. 카카오 맵 API 가이드를 따라가면서 구현했기 때문에 크게 어려움은 없었습니다.<br> 다만 남들과는 조금 다르게 모든 시/도, 시/군/구, 읍/면/동에 대한 정보를 검색에 활용하려고 했기 때문에 해당 정보를 구하는 것이 조금 까다로웠습니다.<br> 이런 단순 노가다성 작업은 GPT에게 요청하였고, 수십 번의 요청을 해서 겨우 얻어냈습니다.<br> 그래서 다른 조원들에게도 나누어 주었습니다.

# 커뮤니티

1. 커뮤니티 기능으로는 기본적인 게시글 조회, 생성, 삭제 수정 및 댓글, 삭제 기능을 django와 vue3를 통해 구현하였으며 좋아요와 대댓글은 기본적인 기능을 구현부터하고 디테일한 부분을 구현하려고 했어야 했는데 디테일한 부분에 신경을 쓰느라 일정 때문에 구현을 하지 못했습니다.

2. 커뮤니티의 종류는 사용자들이 자유로운 주제로 작성할 수 있는 자유 게시판, 금융 서비스를 제공하기 때문에 사용자들끼리 재테크 정보 등을 공유할 수 있도록 재테크 공유 게시판, 그리고 문의사항 등을 받기 위해 고객과의 소통 게시판으로 나누었습니다. 추가로 글을 쓰는데에 좀더 편의성을 제공하기 위해 자유게시판에서 글을 작성하고 있지만 글을 작성하는 도중 다른 카테고리에 글을 쓸 수 있도록 구현하였습니다.

3. 그리고 본인이 작성한 게시글의 삭제와 수정 그리고 댓글 삭제를 구현하기 위해 store에 저장된 로그인 정보를 이용해 게시글의 user_id와 댓글의 user_id를 비교하여 같으면 띄우고 같지 않으면 보이지 않도록 하였습니다.

# 프로필 페이지

1. 프로필 페이지에서는 기본 정보와 가입한 상품의 포트폴리오 정보를 볼 수 있도록 구현하였고 차트 라이브러리를 사용하려고 했으나 이것도 일정 이슈로 구현을 하지 못하였습니다. 다만 회원가입을 할때에 입력 받은 자산정보를 바탕으로 포트폴리오에 담은 상품별로 12개월 이자율의 정보를 가져와 현재 나의 자산에서 이자율을 통해 계산을 하여 1년 후 나의 자산 정보를 띄우도록 구현하였습니다.

2. 그리고 회원 정보를 수정 할 수 있도록 게시글 수정과 같은 로직을 통해 구현하였습니다.

# 챗봇 기능

### 기능 : 메시지 입력 및 전송 & 메시지 저장 및 표시 & Open API 호출

### 동작 방식

1. 메시지 입력 및 전송<br>
   사용자는 텍스트 입력란에 메시지를 입력하고, Enter 키를 누르거나 '전송' 버튼을 클릭하여 메시지를 전송합니다.<br>
   이 메시지를 sendMessage 함수가 호출되어 메시지가 처리됩니다.

2. 메시지 저장 및 표시<br>
   입력된 메시지는 messages 배열에 저장되고, addMessage 함수를 통해 화면에 표시됩니다.<br>
   챗봇의 응답도 동일한 방식으로 messages 배열에 저장되고 표시됩니다.<br>

3. OpenAI API 호출<br>
   sendMessage 함수는 사용자가 입력한 메시지를 OpenAI API에 전달하여 챗봇의 응답을 가져옵니다.<br>
   fetchAIResponse 함수가 API 호출을 처리하며, 응답 데이터를 받아와 addMessage 함수를 통해 챗봇의 응답을 저장하고 표시합니다.<br>

4. 채팅 인터페이스<br>
   메시지들을 스크롤 가능한 형식으로 표시했고, 구분이 쉽게 색깔을 주었습니다.

5. 프롬프트<br>
   system: 챗봇의 동작 방식과 성격을 설정하는 시스템 메시지<br>
   user: 사용자가 입력한 메시지<br>
   assistant: 챗봇이 응답하는 메시지<br>
   'role'과 'content'라는 두 가지 속성으로 챗봇이 어떻게 응답해야 할지를 결정(또는 학습 시키는 것)<br>
   챗봇의 역할과 GG Bank의 서비스(투자 상품 비교, 환율 계산, 은행 찾기 등)를 설명하도록 설정<br>

# 3. 데이터베이스 모델링 (ERD)

![alt text](<GG ERD.PNG>)

# 4. 금융 상품 추천 알고리즘에 대한 기술적 설명 ★

### 기능 : 사용자의 예금 및 적금 상품을 추천

### 동작 방식

1. 사용자 입력 및 API 요청 전송
   성별, 나이, 연봉, 자산, 저축 성향을 입력하고, 검색 버튼을 눌러서 django 서버로 API 요청을 보냅니다.
2. 사용자의 위험 감수 성향 평가<br>
   사용자가 입력한 데이터를 바탕으로 점수를 계산하고, 그에 따라 등급을 평가합니다.
3. 금융 상품의 위험 등급 평가<br>
   DB에 저장된 예금\*적금 데이터를 조회하여 점수를 계산하고, 그에 따라 등급을 평가합니다.
4. 금융 상품 반환<br>
   사용자의 위험 감수 성향과 동일한 상품들 중 위험도가 낮은 순으로 데이터를 반환합니다.
5. 사용자의 저축 성향에 따른 상품 추천<br>
   사용자가 선택한 저축 성향(단기, 중기, 장기)에 맞는 개월수의 상품들을 추천해줍니다.

# 5. 서비스 대표 기능들에 대한 설명 ★

1. 커뮤니티에서 자유 게시판, 정보 공유 게시판, 고객과의 소통 페이지를 나누었지만 글을 작성할 때 하나의 카테고리에 갇혀 있지 않고 중간에 다른 카테고리로 바꾸고 싶으면 바꾸고 작성을 한다면 그 카테고리에 게시물이 post 됨으로써 사용자 편의성을 높혔습니다.

2. 챗봇의 위치를 한눈에 알기 쉽도록 메인 페이지에 배치를 하여 저희의 서비스를 쉽게 접근하고 이해할 수 있도록 편의성을 제공하였습니다.

3. 금융 상품 추천 서비스<br>
   사람을 성별에 따른 투자 성향 차이, 나이에 따른 투자 성향 차이, 연봉에 따른 투자 성향 차이, 자산에 따른 투자 성향 차이를 점수화하여 위험도 감수 성향을 평가 하였습니다.
   그리고 상품들에 대하여 은행의 규모와 안정성, 금리에 따른 안정성, 기간에 따른 안정성을 점수화하여 상품의 위험성을 점수화하여 위험도를 평가 하였습니다.
   그에 따라 개인의 성향에 맞게 상품을 추천하도록 서비스를 구현하였습니다.

# 기타(느낀 점, 후기 등)

# 김헌규(팀원)

- 처음하는 프로젝트라서 그런지 의욕이 넘쳐서 필수 기능 구현 이외에 몇개의 기능 추가 그리고 디테일한 부분까지 모두 구현을 하려다가 일정이 꼬였으며 또한 이미 구현했던 기능이 다음날이 되면 작동하지 않는 경우가 발생했었기에 일정상 필수 부분만 진행하게 되어 다소 아쉬웠습니다. 그리고 역할을 기능별로 나누다보니 기능간의 연결점들에 의해 충돌이 발생하여 코드가 꼬이게 되어 작동이 안한 경우도 발생하였습니다. 이러한 상황을 잘 해결하기 위해서는 커밋 메시지를 활용을 했어야 했는데 커밋 메시지도 대충 작성한 흔적이 여러 곳에서 발생하였기에 이 부분도 아쉬웠습니다. 마지막으로 처음에 ERD를 어차피 나중에 가면 많이 바뀔수도 있으므로 설계를 제대로 하지 않고 진행하였다는 점에서 프로젝트를 진행하면서 어떤 부분을 진행하고 있는지에 대해 잘 모르게 되는 경우가 발생하였고 매 순간마다 하나씩 설계하면서 진행하다보니 오히려 시간이 많이 걸리게 되었고 비효율적인 ERD를 설계하게 되어 다시 갈아엎느라 시간을 많이 소모하게 되었습니다.

- 프로젝트를 진행하면서 배우게 된 점은 로그인과 회원가입을 커스텀하는 방법과 OpenAPI를 통해 데이터를 가져와서 저장하고 가공하는 법을 배우게 되었고 기존에 배웠던 게시판 기능을 다시 복습한 계기가 되어 한층 더 실력이 발전되었다고 생각합니다.

- 이렇게 첫 프로젝트를 진행하면서 아쉬웠던 점과 배우게 된 점을 잘 숙지하여 다음 프로젝트에서는 더욱 발전된 모습으로 진행하도록 하겠습니다.
