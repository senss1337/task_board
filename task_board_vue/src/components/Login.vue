<template>
  <div :class="{ 'dark-mode-content': darkMode }">
    <Navbar :darkMode="darkMode" @toggle-dark-mode="toggleDarkMode"></Navbar>
    <div class="login-form is-center" :class="{ 'dark-mode-content': darkMode }">
      <form @submit.prevent="submitForm">
        <div class="field">
          <label class="label">Имя пользователя</label>
          <div class="control">
            <input class="input" type="text" v-model="form.username" placeholder="Введите имя пользователя">
          </div>
        </div>
        <div class="field">
          <label class="label">Пароль</label>
          <div class="control">
            <input class="input" type="password" v-model="form.password" placeholder="Введите пароль">
          </div>
        </div>
        <div class="field">
          <div class="control">
            <button class="button is-black" type="submit">Войти</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Navbar from "../components/Navbar.vue"

export default {
  components: {
    Navbar
  },
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      darkMode: false,
    }
  },
  methods: {
    submitForm() {
      this.goToBoard();
    },
    goToBoard() {
      this.$router.push({ name: 'Board' });
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    }
  }
}
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  height: 680px;
}

.login-form .field {
  margin-bottom: 20px;
}

.login-form .label {
  font-weight: bold;
}

.login-form .input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff; 
  border: 1px solid #ccc; 
}

.login-form .button {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-form .button:hover {
  background-color: #f0f0f0; 
}

.dark-mode-content {
  background-color: #1a1a1a; 
  color: #f0f0f0;
}

.dark-mode-content .label {
  color: #fff; 
}

.dark-mode-content .input {
  background-color: #333; 
  color: #fff; 
}

.dark-mode-content .button {
  background-color: #ffc107; 
  color: #333; 
}
</style>
