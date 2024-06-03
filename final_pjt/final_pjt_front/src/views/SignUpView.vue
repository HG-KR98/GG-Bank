<template>
  <div class="py-3">
    <form @submit.prevent="signUp">
      <div class="container">
        <div class="text-center">
          <img src="@/assets/GG-Logo-Stop.png" alt="no-image" />
        </div>
        <div class="mb-4">
          <label for="username" class="form-label">아이디</label>
          <!-- 중복확인 버튼 -->
          <button type="button" class="button" @click="duplication">
            중복 확인
          </button>
          <!-- 중복확인 버튼 -->
          <input
            type="text"
            class="form-control"
            id="username"
            v-model.trim="username"
          />
          <div id="idCheckTrue" class="form-text" v-if="check === false">
            중복된 아이디가 없습니다.
          </div>
          <div id="idCheckFalse" class="form-text" v-else-if="check === true">
            중복된 아이디가 존재합니다.
          </div>
        </div>
        <div class="mb-4">
          <label for="Password1" class="form-label">비밀번호</label>
          <input
            type="password"
            class="form-control"
            id="Password1"
            v-model.trim="password1"
            @input="validatePassword"
          />
          <div id="idCheckFalse" class="form-text" v-if="!passwordValid">
            비밀번호는 문자, 숫자, 특수문자(~!@#$%^&*)의 조합 10자리 이상으로
            입력이 가능합니다.
          </div>
          <div v-else class="passwordInvaild form-text">
            사용가능한 비밀번호 입니다.
          </div>
        </div>
        <div class="mb-4">
          <label for="Password2" class="form-label">비밀번호 확인</label>
          <input
            type="password"
            class="form-control"
            id="Password2"
            v-model.trim="password2"
          />
        </div>
        <div class="mb-4">
          <label for="email" class="form-label">이메일</label>
          <input
            type="email"
            class="form-control"
            id="email"
            aria-describedby="emailHelp"
            v-model.trim="email"
          />
        </div>
        <div class="mb-4">
          <label for="name" class="form-label">이름</label>
          <input
            type="text"
            class="form-control"
            id="name"
            v-model.trim="name"
          />
        </div>

        <div class="mb-4">
          <label for="gender" class="form-label">성별</label>
          <select
            class="form-select me-2"
            v-model="gender"
            aria-label="Default select example"
          >
            <option value="남성">남성</option>
            <option value="여성">여성</option>
            <option value="성소수자">성소수자</option>
          </select>
        </div>
        <div class="mb-4">
          <label for="birthdate">생년월일</label>
          <div>
            <input
              type="date"
              id="birthdate"
              name="birthdate"
              v-model.trim="birthDate"
            />
          </div>
        </div>
        <div class="mb-4">
          <label for="phone-number" class="form-label">휴대폰 번호</label>
          <input
            type="text"
            class="form-control"
            id="phone-number"
            v-model.trim="phoneNumber"
          />
        </div>
        <div class="mb-4">
          <label for="assets" class="form-label">자산</label>
          <input
            type="text"
            class="form-control"
            id="assets"
            v-model.trim="assets"
          />
        </div>
        <button type="submit" class="button" v-if="check === false">
          가입하기
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

// 회원가입 항목
const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const email = ref(null);
const name = ref(null);
const gender = ref(null);
const birthDate = ref(null);
const phoneNumber = ref(null);
const assets = ref(null); // 포맷된 숫자 값

// 아이디 중복체크 변수
const check = ref(null);
// 비밀번호 10자리 체크 변수
const passwordValid = ref(false);

const store = useCounterStore();

const signUp = function () {
  if (password1.value.length > 9) {
    const payload = {
      username: username.value,
      password1: password1.value,
      password2: password2.value,
      email: email.value,
      name: name.value,
      gender: gender.value,
      birth_date: birthDate.value,
      phone_number: phoneNumber.value,
      assets: assets.value,
    };
    store.signUp(payload);
  } else {
    alert("비밀번호를 10자리 이상 입력해 주세요!");
  }
};

// 아이디 중복확인 함수
const duplication = function () {
  axios({
    method: "get",
    url: `${store.API_URL}/user/${username.value}/`,
  })
    .then((response) => {
      if (response.data.result === true) {
        check.value = true;
      } else {
        check.value = false;
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

// 비밀번호 유효성 검사 함수
const validatePassword = function () {
  const password = password1.value;
  const regex =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$%^&*])[A-Za-z\d~!@#$%^&*]{10,}$/;
  passwordValid.value = regex.test(password);
};
</script>

<style scoped>
.container {
  margin-top: 50px;
  margin-bottom: 50px;
  width: 70%;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.button {
  background-color: #b2e8ff;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 15px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
  margin: 10px;
}

.button:hover {
  background-color: #6497fc;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}

img {
  width: 240px;
  height: 220px;
}

#idCheckTrue {
  color: blue;
}

#idCheckFalse {
  color: red;
}
.passwordInvaild {
  color: blue;
}
</style>
