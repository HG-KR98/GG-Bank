<template>
  <div class="container">
    <div class="container-out">
      <div class="container-in">
        <!-- 슬라이드 -->
        <div
          id="carouselExampleFade"
          class="carousel slide carousel-fade big-slide-box"
          data-bs-ride="carousel"
          data-bs-interval="3000"
        >
          <div class="carousel-inner">
            <div class="carousel-item active">
              <div class="d-flex align-items-center slide-content">
                <div class="slide-text">
                  <h1>편리성</h1>
                  <p>고객님들의 편리성을 최우선으로 합니다.</p>
                </div>
                <div class="slide-image">
                  <img
                    src="@/assets/homepage1.png"
                    class="d-block w-100"
                    alt="homepage1"
                  />
                </div>
              </div>
            </div>
            <div class="carousel-item">
              <div class="d-flex align-items-center slide-content">
                <div class="slide-text">
                  <h1>사회환원</h1>
                  <p>함께하는 세상을 만들어갑니다.</p>
                </div>
                <div class="slide-image">
                  <img
                    src="@/assets/homepage2.png"
                    class="d-block w-100"
                    alt="homepage2"
                  />
                </div>
              </div>
            </div>
            <div class="carousel-item">
              <div class="d-flex align-items-center slide-content">
                <div class="slide-text">
                  <h1>안정성</h1>
                  <p>안정된 미래를 위한 최고의 파트너.</p>
                </div>
                <div class="slide-image">
                  <img
                    src="@/assets/homepage3.png"
                    class="d-block w-100"
                    alt="homepage3"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- 버튼 -->
          <button
            class="carousel-control-prev"
            type="button"
            data-bs-target="#carouselExampleFade"
            data-bs-slide="prev"
          >
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>

          <button
            class="carousel-control-next"
            type="button"
            data-bs-target="#carouselExampleFade"
            data-bs-slide="next"
          >
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
          <!-- 버튼 -->
        </div>
        <!-- 슬라이드 -->

        <!-- 컨텐츠 -->
        <div class="content-section m-2">
          <!-- 챗봇 -->
          <div class="smooth-box-style">
            <h3>챗봇 서비스</h3>
            <div id="app">
              <div id="chat-container" v-if="isChatVisible">
                <div id="chat-messages">
                  <div
                    v-for="(message, index) in messages"
                    :key="index"
                    class="message"
                  >
                    {{ message.sender }}: {{ message.text }}
                  </div>
                </div>
                <div id="user-input">
                  <input
                    type="text"
                    v-model="userMessage"
                    @keydown.enter="sendMessage"
                    placeholder="메시지를 입력하세요..."
                  />
                  <button @click="sendMessage">전송</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 인기글 -->
          <div class="community-posts smooth-box-style">
            <h3>인기글</h3>
            <ul class="article-list">
              <li
                v-for="article in sortedArticles.slice(0, 3)"
                :key="article.id"
                class="article-item"
              >
                <RouterLink
                  :to="{
                    name: 'FreeDetailView',
                    params: { id: article.id },
                  }"
                  class="article-link"
                >
                  <h5 class="article-title">제목: {{ article.title }}</h5>
                  <p class="article-content">내용: {{ article.content }}</p>
                  <p class="article-views">조회수: {{ article.views }}</p>
                  <p class="article-category">
                    게시판: {{ getBoardName(article.category) }}
                  </p>
                </RouterLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useFinancialStore } from "@/stores/financial";
import { useCounterStore } from "@/stores/counter";
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const fstore = useFinancialStore();
const cstore = useCounterStore();

const sortedArticles = computed(() => {
  // Ensure articles are sorted by views in descending order
  return cstore.articles.slice().sort((a, b) => b.views - a.views);
});

const isChatVisible = ref(true);
const messages = ref([]);
const userMessage = ref("");
const apiEndpoint = "https://api.openai.com/v1/chat/completions";
const apiKey  = ref(""); // 여기에 실제 API 키를 입력하세요.


const addMessage = (sender, text) => {
  messages.value.unshift({ sender, text });
};

const fetchAIResponse = async (prompt) => {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey.value}`,
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [
        {
          role: "system",
          content:
            "당신은 GG Bank의 유용한 어시스턴트입니다. GG Bank의 서비스는 투자 상품 비교, 환율 계산, 근처 은행 검색, 커뮤니티, 저축 상품 추천 등을 포함합니다. 또한 사용자가 은행 및 금융 서비스에 대해 궁금한 점을 편리하게 해결할 수 있도록 도와줍니다.",
        },
        {
          role: "user",
          content: "안녕하세요! GG Bank에서 제공하는 서비스는 무엇인가요?",
        },
        {
          role: "assistant",
          content:
            "안녕하세요! GG Bank는 투자 상품 비교, 환율 계산, 근처 은행 찾기, 커뮤니티, 저축 상품 추천 등 다양한 은행 서비스를 제공합니다. 오늘 어떤 도움을 드릴까요?",
        },
        { role: "user", content: "어떤 투자 옵션이 있나요?" },
        {
          role: "assistant",
          content:
            "GG Bank는 다양한 투자 상품을 제공합니다. 이러한 옵션은 웹사이트나 앱의 '투자' 섹션에서 확인할 수 있습니다. 맞춤형 투자 상담이 필요하시면 언제든지 물어보세요!",
        },
        { role: "user", content: "가장 가까운 은행 지점을 찾을 수 있나요?" },
        {
          role: "assistant",
          content:
            "물론입니다! 웹사이트나 앱의 '은행 찾기' 기능을 사용하여 가장 가까운 은행 지점을 찾을 수 있습니다. 위치를 입력하면 가까운 지점과 연락처 정보, 운영 시간을 확인할 수 있습니다.",
        },
        { role: "user", content: "현재 환율을 어떻게 확인할 수 있나요?" },
        {
          role: "assistant",
          content:
            "현재 환율은 웹사이트나 앱의 '환율' 섹션에서 확인할 수 있습니다. 이 섹션에서는 실시간 환율 정보를 제공합니다. 환율 변환이 필요하면 저희의 환율 변환 도구를 사용하세요.",
        },
        { role: "user", content: "고객 지원을 어떻게 받을 수 있나요?" },
        {
          role: "assistant",
          content:
            "고객 지원이 필요하시면 웹사이트나 앱의 '고객 소통' 섹션을 통해 문의할 수 있습니다. 저희 고객 지원 팀은 24시간 내내 문제를 도와드릴 준비가 되어 있습니다.",
        },
        {
          role: "user",
          content: "저축 상품에 대한 자세한 정보를 알고 싶어요.",
        },
        {
          role: "assistant",
          content:
            "GG Bank의 저축 상품에 대한 자세한 정보는 웹사이트나 앱의 '저축 상품' 섹션에서 확인할 수 있습니다. 이 섹션에서는 다양한 저축 상품의 이자율, 조건 및 혜택을 제공합니다.",
        },
        ...prompt,
      ],
      temperature: 0.7,
      max_tokens: 150,
      top_p: 1,
      frequency_penalty: 0,
      presence_penalty: 0,
    }),
  };
  try {
    const response = await fetch(apiEndpoint, requestOptions);
    const data = await response.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error("OpenAI API 호출 중 오류 발생:", error);
    return "OpenAI API 호출 중 오류 발생";
  }
};

const sendMessage = async () => {
  const message = userMessage.value.trim();
  if (message.length === 0) return;

  addMessage("나", message);
  userMessage.value = "";

  const prompt = messages.value.map((m) => ({
    role: m.sender === "나" ? "user" : "assistant",
    content: m.text,
  }));
  prompt.push({ role: "user", content: message });

  const aiResponse = await fetchAIResponse(prompt);
  addMessage("챗봇", aiResponse);
};

const getBoardName = (category) => {
  switch (category) {
    case "free":
      return "자유게시판";
    case "investment":
      return "재테크 정보공유";
    case "customer":
      return "고객과의 소통";
    default:
      return "기타";
  }
};

onMounted(() => {
  // Fetch articles to ensure the latest data is available
  cstore.getArticles();
  fstore.saveSaving();
  fstore.saveDeposit();
  fstore.getDepositBaseList();
  fstore.getSavingBaseList();


  axios
    .get("http://127.0.0.1:8000/chatbot/")
    .then((response) => {
      apiKey.value = response.data.API_KEY;
    
    })
    .catch((error) => {
      console.log(error);
    });
});
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  padding-top: 50px;
  padding-bottom: 50px;
}

.container-out {
  width: 100%;
  padding: 10px;
  min-width: 750px;
  border-radius: 15px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
  background-color: rgb(203, 230, 253);
}

.container-in {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 750px;
  border-radius: 15px;
  background-color: rgb(203, 230, 253);
}

.big-slide-box {
  width: 100%;
  max-width: 1200px;
  border-radius: 15px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
}

.slide-content {
  height: 500px;
  background-color: white;
  border-radius: 15px;
}

.slide-text {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.slide-image {
  flex: 2;
}

.slide-image img {
  height: 500px;
  object-fit: cover;
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
}

.content-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.smooth-box-style {
  width: 49.5%;
  height: 380px;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
  display: flex;
  flex-direction: column;
}

#chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 300px; /* Fixed height to match the popular posts container */
  overflow: hidden;
}

#chat-messages {
  flex: 1;
  overflow-y: auto; /* Scroll for overflowing messages */
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
}

.message {
  padding: 10px 15px; /* Added padding for consistent height */
  margin-bottom: 10px; /* Added margin for spacing */
  border-radius: 10px;
  word-wrap: break-word;
  display: flex; /* Ensure consistent height */
  align-items: center; /* Vertically center content */
}

.message:nth-child(odd) {
  background-color: #c0d5ff;
  font-weight: bold;
  color: #ffffff;
}

.message:nth-child(even) {
  background-color: #c8ff98;
  font-weight: bold;
  color: #8d8d8d;
}

#user-input {
  display: flex;
  align-items: center;
}

#user-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  margin-right: 10px;
  font-size: 1em;
}

#user-input button {
  padding: 10px 20px;
  background-color: #87cef2;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

#user-input button:hover {
  background-color: #6497fc;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

.article-list {
  list-style: none;
}

.article-item {
  width: 90%;
  height: 130px;
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 10px;
  background-color: #ffffff;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.article-item:hover {
  background-color: #f1f1f1;
  box-shadow: 0 4px 8px #6497fc;
}

.article-link {
  text-decoration: none;
  color: inherit;
}

.article-title {
  font-size: 1.1em;
  font-weight: bold;
  margin: 0 0 10px 0;
  color: #000000;
}

.article-content {
  margin: 0;
  color: #555;
}

.article-views,
.article-category {
  margin: 0;
  color: #999;
}
</style>