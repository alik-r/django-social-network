<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Reset Password</h1>
                <p class="mb-6 text-gray-500">
                    Enter your new password to reset your account password.
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <div>
                        <label>New password</label><br>
                        <input type="password" v-model="form.new_password" placeholder="Your new password"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Repeat password</label><br>
                        <input type="password" v-model="form.repeat_password" placeholder="Repeat password"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <button class="py-4 px-6 bg-blue-600 text-white rounded-lg">
                            Reset Password
                        </button>
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
            form: {
                new_password: '',
                repeat_password: '',
            },
            errors: [],
        }
    },
    methods: {
        submitForm() {
            this.errors = []
            if (this.form.new_password !== this.form.repeat_password) {
                this.errors.push('The password does not match')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/reset-password/', {
                        email: this.$route.query.email,
                        user_id: this.$route.query.id,
                        new_password: this.form.new_password,
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'Password reset successful', 'bg-green-500 text-white')
                            this.$router.push('/login')
                        } else {
                            this.toastStore.showToast(5000, 'Password reset failed', 'bg-red-500 text-white')
                            const data = JSON.parse(response.data.message)
                            for (const key in data){
                                this.errors.push(data[key][0].message)
                            }
                            this.toastStore.showToast(5000, `Password reset failed: ${this.errors[0]}`, 'bg-red-500 text-white')
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