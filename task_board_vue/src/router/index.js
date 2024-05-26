import { createRouter, createWebHashHistory } from 'vue-router'
import Registration from '../components/Registration.vue'
import MainPage from '../components/MainPage.vue'
import Login from '../components/Login.vue'
import Board from '../components/Board.vue'
import CreateBoard from '../components/CreateBoard.vue'
import CreateTask from '../components/CreateTask.vue'

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage
  },
  {
    path: '/api/registration/',
    name: 'Registration',
    component: Registration
  },
  {
    path: '/api/login/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/api/board/',
    name: 'Board',
    component: Board,
  },
  {
    path: '/api/board/create/',
    name: 'CreateBoard',
    component: CreateBoard,
  },
  {
    path: '/api/task/create/',
    name: 'CreateTask',
    component: CreateTask,
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
