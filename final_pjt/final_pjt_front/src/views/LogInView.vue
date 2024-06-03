<template>
  <!-- 전체 박스 -->
  <div class="container1">
    <div class="container2">
      <!-- 이미지 박스 -->
      <div class="img-box">
        <img src="@/assets/GG_Bank_Login.png" alt="GG_Bank_Login" />
      </div>

      <!-- 세로 선 -->
      <div class="vertical-line"></div>

      <!-- 로그인 박스 -->
      <div class="login-box">
        <h2>아이디 로그인</h2>
        <form @submit.prevent="logIn">
          <div class="input-group">
            <label for="username"></label>
            <input
              type="text"
              placeholder="아이디"
              v-model.trim="username"
              id="username"
            />
          </div>
          <div class="input-group">
            <label for="password"></label>
            <input
              type="password"
              placeholder="비밀번호"
              v-model.trim="password"
              id="password"
            />
          </div>
          <button type="submit" class="login-button">로그인</button>
          <div class="checkbox-group">
            <input type="checkbox" id="save-id" v-model="saveId" />
            <label for="save-id">아이디 저장</label>
          </div>
        </form>
        <div class="extra-options">
          <a href="#">아이디 찾기 <span class="arrow">></span></a>
          <a href="#">비밀번호 찾기 <span class="arrow">></span></a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useCounterStore } from "@/stores/counter"; // assuming you have this store

const username = ref(localStorage.getItem("savedUsername") || "");
const password = ref(null);
const saveId = ref(!!localStorage.getItem("savedUsername"));
const store = useCounterStore();

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  store.logIn(payload);

  if (saveId.value) {
    localStorage.setItem("savedUsername", username.value);
  } else {
    localStorage.removeItem("savedUsername");
  }
};

// saveId 체크박스를 감시하여 로컬 스토리지를 업데이트
watch(saveId, (newValue) => {
  if (newValue) {
    localStorage.setItem("savedUsername", username.value);
  } else {
    localStorage.removeItem("savedUsername");
  }
});
</script>

<style scoped>
/* 컨테이너 박스 */
.container1 {
  display: flex;
  justify-content: center;
  padding: 50px;
}

.container2 {
  background-color: white;
  display: flex;
  width: 100%;
  max-width: 1200px;
  padding: 30px;
  border-radius: 15px;
}

/* 이미지 박스 */
.img-box {
  margin: 50px;
  width: 50%;
  display: flex;
  justify-content: center;
  border-radius: 15px;
  align-items: center;
}

.img-box img {
  max-width: 100%;
  height: auto;
  border-radius: 15px;
}

/* 구분선 */
.vertical-line {
  width: 1px;
  background-color: #969292;
  height: 100%;
}

/* 로그인 박스 */
.login-box {
  background-color: white;
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px;
  margin-left: 30px;
}

.login-box h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
  width: 100%;
}

.input-group input {
  width: 100%;
  padding: 15px;
  border: 1px solid #c3c3c3;
  border-radius: 15px;
  font-size: 16px;
}

.login-button {
  width: 100%;
  padding: 15px;
  background-color: #78b2ec;
  border: none;
  color: white;
  font-size: 16px;
  border-radius: 15px;
  cursor: pointer;
  margin-bottom: 15px; /* Added margin for spacing */
}

/* 커서를 올렸을 때 색상 변경 */
.login-button:hover {
  background-color: #0056b3;
}

.checkbox-group {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.checkbox-group input {
  margin-right: 10px;
}

.extra-options {
  display: flex;
  justify-content: space-evenly;
  width: 100%;
  font-size: 14px;
  padding: 10px 0;
}

.extra-options a {
  color: #007bff;
  text-decoration: none;
  display: flex;
  align-items: center;
}

.extra-options .arrow {
  font-size: 16px;
  margin-left: 5px;
}

/* 밑줄 제거 */
.extra-options a:hover {
  text-decoration: underline;
}
</style>
