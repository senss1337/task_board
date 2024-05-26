<template>
  <div :class="{ 'dark-mode-content': darkMode }">
    <Navbar :darkMode="darkMode" @toggle-dark-mode="toggleDarkMode"></Navbar>
    <form @submit.prevent="addTask">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Новая задача</label>
        </div>
        <div class="field-body">
          <div class="field">
            <div class="control">
              <input class="input" type="text" placeholder="Введите задачу" v-model="newTask">
            </div>
          </div>
          <div class="field">
            <div class="control">
              <button class="button is-black">Добавить</button>
            </div>
          </div>
        </div>
      </div>
    </form>

    <table class="table is-fullwidth is-striped is-hoverable">
      <thead>
        <tr>
          <th>Задача</th>
          <th>Выполнение</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(task, index) in tasks" :key="index">
          <td>{{ task.name }}</td>
          <td><input type="checkbox" v-model="task.completed"></td>
          <td><button class="button is-dark" @click="deleteTask(index)">Удалить</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"
export default {
  components: {
    Navbar
  },
  data() {
    return {
      tasks: [],
      newTask: '',
      darkMode: false,
    };
  },
  methods: {
    deleteTask(index) {
      this.tasks.splice(index, 1);
    },
    addTask() {
      if (this.newTask.trim() !== '') { 
        this.tasks.push({ name: this.newTask, completed: false });
        this.newTask = ''; 
      }
    },
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
    toggleNavbar() {
      this.isNavbarActive = !this.isNavbarActive;
    },
  },
};
</script>

<style scoped>
.dark-mode-content {
  background-color: #1a1a1a; 
  color: #f0f0f0;
  height: 670px;
}

.dark-mode-content th {
  color: white;
  background-color: #333;
}

.dark-mode-content tr {
  color: white;
  background-color: #333;
}
.dark-mode-content td {
  color: white;
  
}
.dark-mode-content input[type="text"],
.dark-mode-content input[type="password"],
.dark-mode-content input[type="checkbox"] {
  background-color: #333;
  color: #fff;
}

.dark-mode-content .button {
  background-color: #ffc107;
  color: #333;
}

</style>
