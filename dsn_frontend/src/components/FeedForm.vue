<template>
    <form v-on:submit.prevent="submitForm" method="post">
        <div class="p-4">  
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>


            <div id="preview" v-if="url">
                <img :src="url" class="w-[100px] mt-3 rounded-xl" />
            </div>
        </div>

        <div class="p-4 border-t border-gray-100 flex">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg cursor-pointer">
                <input type="file" ref="file" @change="onFileChange">
                Attach image
            </label>

            <label class="inline-block py-4 px-6 rounded-lg cursor-pointer">
                <input type="checkbox" v-model="is_private"> Private
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="inline-block w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>
            </label>

            <button class="ml-auto inline-block py-4 px-6 bg-blue-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>

<script>
import axios from 'axios'
export default {
    props: {
        user: Object,
        posts: Array
    },
    data() {
        return {
            body: '',
            is_private: false,
            url: null,
        }
    },
    methods: {
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },
        
        submitForm() {
            console.log('submitForm (create post) body:', this.body)

            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)
            formData.append('is_private', this.is_private)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('submitForm (create post) response:', response.data)

                    if (response.data.message === 'success') {
                        this.posts.unshift(response.data.post)
                        this.body = ''
                        this.is_private = false
                        this.$refs.file.value = null
                        this.url = null
                        if (this.user) {
                            this.user.posts_count += 1
                        }
                    } else {
                        const data = JSON.parse(response.data.message)
                        for (const key in data){
                            this.errors.push(data[key][0].message)
                        }
                        console.error('Errors:', this.errors)
                    }
                })
                .catch(error => {
                    console.log('error:', error)
                })
        },
    }
}
</script>