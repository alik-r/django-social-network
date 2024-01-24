<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Forgot Password</h1>
        <p class="mb-6 text-gray-500">
          Enter your email to receive instructions for resetting your password.
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" @submit.prevent="submitForm">
          <div>
            <label>Email</label><br>
            <input
              type="email"
              v-model="form.email"
              placeholder="Your email address"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            >
          </div>

          <template v-if="errors.length > 0">
            <div class="bg-red-500 text-white rounded-lg p-6">
              <p v-for="error in errors" :key="error">{{ error }}</p>
            </div>
          </template>

          <div>
            <button class="py-4 px-6 bg-blue-600 text-white rounded-lg">Reset Password</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'

export default {
  setup() {
    const toastStore = useToastStore()
    return {
      toastStore,
    }
  },
  data() {
    return {
      form: {
        email: '',
      },
      errors: [],
      }
  },
  methods: {
    submitForm() {
      this.errors = []
      if (this.form.email === '') {
        this.errors.push('Your email is missing')
      }

      if (this.errors.length === 0) {
        axios
          .post('/api/forgot-password/', {
            email: this.form.email,
          })
          .then(response => {
            if (response.data.message === 'sent') {
              this.toastStore.showToast(5000, 'Instructions were sent to your email', 'bg-green-500 text-white')
            } else {
              this.toastStore.showToast(5000, 'There is no user with this email', 'bg-red-500 text-white')
            }
          })
          .catch(error => {
            console.log('error', error)
          })
      }
    }
  }
}
</script>