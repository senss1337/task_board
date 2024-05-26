<template>
    <div :class="{ 'dark-mode-content': darkMode }"></div>
        <nav class="navbar has-text-white is-link">
            <div class="container">
            <div class="navbar-brand">
                <a class="navbar-item" href="/">Task Board</a>
            </div>
            <div :class="['navbar-menu', isNavbarActive ? 'is-active' : '']">
                <div class="navbar-end">
                <a class="navbar-item" @click="goToRegistrationPage">Регистрация</a>
                <a class="navbar-item" @click="goToLoginPage">Войти</a>
                <a class="navbar-item" @click="showLogoutModal = true">Выйти</a>
            
                <button class="button" @click="toggleDarkMode">Dark</button>
        
                </div>
            </div>
            </div>
            <div class="modal" :class="{ 'is-active': showLogoutModal }">
        <div class="modal-background"></div>
        <div class="modal-content">
            <div class="box">
            <p>Вы действительно хотите выйти?</p>
            </div>
            <button class="button is-danger" @click="logout">Выйти</button>
            <button class="button" @click="closeLogoutModal">Закрыть</button>
        </div>
        <button class="modal-close is-large" aria-label="close" @click="closeLogoutModal"></button>
        </div>
    </nav>
    <div/>
</template>
  
  <script>
  import axios from "axios";
  export default {
    name: "Navbar",
    props: ['darkMode'],
    data() {
      return {
        isNavbarActive: false,
        showLogoutModal: false
      };
    },
    methods: {
      toggleNavbar() {
        this.isNavbarActive = !this.isNavbarActive;
      },
      closeLogoutModal() {
        this.showLogoutModal = false;
      },
      goToRegistrationPage() {
        this.$router.push({ name: 'Registration' });
      },
      goToLoginPage() {
        this.$router.push({ name: 'Login' });
      },
      toggleDarkMode() {
      this.$emit('toggle-dark-mode');
    }
    },
    created() {
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    },
  }
  </script>
  
  <style>
  .navbar.is-link {
    background-color: #1a1a1a; 
    color: #fff; 
    font: bold;
  }
  
  .navbar.is-link .navbar-item {
    color: #fff; 
  }
  
  .navbar.is-link .navbar-item:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  .navbar.is-link .navbar-item.is-active {
    background-color: rgba(255, 255, 255, 0.2);
  }

  .dark-mode-content {
  background-color: #1a1a1a;
  color: #f0f0f0; 
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.dark-mode-content h1 {
  color: #ffc107;
}

.dark-mode-content button {
  background-color: #ffc107; 
  color: #333;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dark-mode-content button:hover {
  background-color: #ffca28; 
}

.dark-mode-content button:focus {
  outline: none;
}
  </style>
  