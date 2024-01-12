<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>

                        <div id="preview" v-if="url">
                            <img :src="url" class="w-[100px] mt-3 rounded-xl" />
                        </div>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                            <input type="file" ref="file" @change="onFileChange">
                            Attach image
                        </label>


                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </form>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post" />
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>

<style>
input[type="file"] {
    display: none;
}
</style>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import FeedItem from '../components/FeedItem.vue'

export default {
    name: 'FeedView',

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem
    },

    data() {
        return {
            posts: [],
            body: '',
            url: null,
            errors: [],
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {
                    console.log('getFeed response:', response.data)

                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error:', error)
                })
        },

        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },

        submitForm() {
            console.log('submitForm body:', this.body)

            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

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
                        this.$refs.file.value = null
                        this.url = null
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