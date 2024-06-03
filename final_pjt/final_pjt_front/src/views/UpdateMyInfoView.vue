<template>
  <div class="container">
    <div class="container-out">
      <div class="container-in">
        <form @submit.prevent="updateUserInfo">
          <div class="text-center">
            <img src="@/assets/GG-Logo.gif" alt="no-image" />
          </div>

          <!-- 기존 비밀번호 일치 확인 -->
          <div class="mb-4">
            <label for="existing_password" class="form-label"
              >기존 비밀번호</label
            >
            <!-- 확인 버튼 -->
            <button
              type="button"
              class="btn btn-primary btn-sm mx-2"
              @click="passwordMatch"
            >
              비밀번호 확인
            </button>
            <!-- 확인 버튼 -->
            <input
              type="password"
              class="form-control mb-4"
              id="existing_password"
              v-model.trim="existing_password"
            />
            <div id="pwCheckFalse" class="form-text" v-if="check === false">
              비밀번호가 일치하지 않습니다.
            </div>
            <div id="pwCheckTrue" class="form-text" v-else-if="check === true">
              비밀번호가 일치합니다.
            </div>
          </div>

          <!-- 변경할 비밀번호 -->
          <div class="mb-4">
            <label for="new_password1" class="form-label"
              >변경할 비밀번호</label
            >
            <input
              type="password"
              class="form-control"
              id="new_password1"
              v-model.trim="new_password1"
            />
            <div id="PasswordHelp" class="form-text">
              비밀번호는 문자, 숫자, 특수문자(~!@#$%^&*)의 조합 10자리 이상으로
              입력이 가능합니다.
            </div>
          </div>

          <div class="mb-4">
            <label for="new_password2" class="form-label"
              >변경할 비밀번호 확인</label
            >
            <input
              type="password"
              class="form-control"
              id="new_password2"
              v-model.trim="new_password2"
            />
          </div>
          <div class="mb-4">
            <label for="new_email" class="form-label">이메일</label>
            <input
              type="email"
              class="form-control"
              id="new_email"
              aria-describedby="emailHelp"
              v-model.trim="new_email"
            />
          </div>
          <div class="mb-4">
            <label for="new_name" class="form-label">이름</label>
            <input
              type="text"
              class="form-control"
              id="new_name"
              v-model.trim="new_name"
            />
          </div>

          <div class="mb-4">
            <label for="new_gender" class="form-label">성별</label>
            <select
              class="form-select me-2"
              v-model="new_gender"
              aria-label="Default select example"
            >
              <option value="남성">남성</option>
              <option value="여성">여성</option>
              <option value="성소수자">성소수자</option>
            </select>
          </div>

          <div class="mb-4">
            <label for="new_birth_date">생년월일</label>
            <div>
              <input
                type="date"
                id="new_birth_date"
                name="new_birth_date"
                v-model.trim="new_birth_date"
              />
            </div>
          </div>

          <div class="mb-4">
            <label for="new_phone_number" class="form-label">폰번호</label>
            <input
              type="text"
              class="form-control"
              id="new_phone_number"
              v-model.trim="new_phone_number"
            />
          </div>

          <div class="mb-4">
            <label for="new_assets" class="form-label">자산</label>
            <input
              type="text"
              class="form-control"
              id="new_assets"
              v-model.trim="new_assets"
            />
          </div>

          <button type="submit" class="btn btn-primary" v-if="check === true">
            수정
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const store = useCounterStore();
const { token } = storeToRefs(store);

// 회원정보 수정 항목
const username = store.userInfo.username;
const existing_password = ref(null);
const new_password1 = ref(null);
const new_password2 = ref(null);
const new_email = ref(store.userInfo.email);
const new_name = ref(store.userInfo.name);
const new_gender = ref(store.userInfo.gender);
const new_birth_date = ref(store.userInfo.birthDate);
const new_phone_number = ref(store.userInfo.phone_number);
const new_assets = ref(store.userInfo.assets);

// 비밀번호 일치 체크 변수
const check = ref(false);

// 비밀번호 체크 함수
const passwordMatch = function () {
  const password = existing_password.value;
  axios({
    method: "post",
    url: `${store.API_URL}/accounts/login/`,
    headers: {
      Authorization: `Token ${token.value}`,
    },
    data: {
      username,
      password,
    },
  })
    .then((response) => {
      check.value = true;
    })
    .catch((error) => {
      check.value = false;
      console.log(error);
    });
};

const updateUserInfo = function () {
  axios({
    method: "put",
    url: `${store.API_URL}/user/update/`,
    headers: {
      Authorization: `Token ${token.value}`,
    },
    data: {
      phone_number: new_phone_number.value,
      name: new_name.value,
      gender: new_gender.value,
      birth_date: new_birth_date.value,
      assets: new_assets.value,

      password: new_password1.value,
      email: new_email.value,
    },
  })
    .then((response) => {
      console.log(response.data);
      const password = new_password1.value;
      store.logIn({ username, password });
      router.push({ name: "HomeView" });
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  console.log(store.userInfo);
});
</script>

<style scoped>
.container {
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
  min-width: 750px;
  border-radius: 15px;
  background-color: white;
  padding: 15px;
}

img {
  width: 240px;
  height: 220px;
}

#pwCheckFalse {
  color: red;
}

#pwCheckTrue {
  color: blue;
}

/* 버튼 */
button {
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

button:hover {
  background-color: #6497fc;
  transform: scale(1.1); /* 호버 시 약간 확대 */
}
</style>
