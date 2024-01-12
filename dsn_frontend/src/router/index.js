import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import FeedView from '../views/FeedView.vue'
import SearchView from '../views/SearchView.vue'
import ProfileView from '../views/ProfileView.vue'
import FriendsView from '../views/FriendsView.vue'
import PostView from '../views/PostView.vue'
import ChatView from '../views/ChatView.vue'
import TrendView from '../views/TrendView.vue'
import ProfileEditView from '../views/ProfileEditView.vue'
import PasswordEditView from '../views/PasswordEditView.vue'
import NotificationsView from '../views/NotificationsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView 
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView 
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView 
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView 
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/profile/edit',
      name: 'profile_edit',
      component: ProfileEditView
    },
    {
      path: '/profile/edit/password',
      name: 'password_edit',
      component: PasswordEditView
    },
    {
      path: '/profile/:id/friends',
      name: 'friends',
      component: FriendsView
    },
    {
      path: '/:id',
      name: 'post_view',
      component: PostView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/trends/:id',
      name: 'trend_view',
      component: TrendView
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
