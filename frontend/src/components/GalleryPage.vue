<template>
    <div class="gallery">
        <BaseHeader>Видеогалерея</BaseHeader>
        <EmptyCard class="filter">
            <template #header>
                Фильтр
            </template>
            <div class="filter__filters">           
                <div class="filter__row">                    
                    <BaseSelect @input="(value)=>{ subfilter = value}"  label="Строительный объект" :options="filter.subOption"></BaseSelect>
                </div>
                <div class="filter__datetime">
                    <BaseSelect @input="(value)=>{ datesfilter = value}"  label="Дата"  :options="filter.datesoption"></BaseSelect>
                </div>
             </div>

        </EmptyCard>
        <div class="gallery__videos">
            <VideoCard @click="openVideo(video)" v-for="video in filteredvideos" :video="video" :key="video" />
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import BaseHeader from './BaseHeader.vue'
import EmptyCard from './EmptyCard.vue';
import {getVideoList} from '@/api/index';
import VideoCard from './VideoCard.vue';
import BaseSelect from './BaseSelect.vue';
import { useMainStore } from "@/store/index";

const mainStore = useMainStore();


const videos = ref([])

const filter = computed(()=>{
    const subjects = [...new Set(videos.value.map((item)=>item.construction_object))]

    const subOption = subjects.map(item=>({label:item, value: item}))

    const dates = [...new Set(videos.value.map((item)=>item.date))]

    const datesoption = dates.map(item=>({label:item, value: item}))
     
    return {subOption, datesoption}
})

const subfilter = ref('')
const datesfilter = ref('')

function openVideo(video){
    mainStore.changePage('videoanalytics')
    mainStore.video = video
}

const filteredvideos = computed(()=>{
    return videos.value.filter((video)=>{
        if(subfilter.value && video.construction_object !== subfilter.value){
            return
        }
        const day = video.date

        if(datesfilter.value && day !== datesfilter.value){
            return
        }

        return video
    })
})


// const BUCKET_DOWNLOAD_NAME = 'http://localhost:9000/videos/' // processed-videos
const BUCKET_DOWNLOAD_NAME = process.env.VUE_APP_BUCKET_DOWNLOAD_NAME

onMounted(async ()=>{
    const resp = await getVideoList()
    const data = resp.data
    videos.value = data.map((video)=>{video.url=BUCKET_DOWNLOAD_NAME+video.url 
    return video})
})


</script>


<style scoped lang="scss">
.gallery{
    &__videos{
        margin-top: 35px;
        display: flex;
        gap: 30px;
        flex-wrap: wrap;
    }
}

.filter{
    &__row{
        display: flex;
        width: 825px;
        gap: 25px;
    }

    &__item{
        flex-shrink: 2;
    }
    &__class{
        max-width: 160px;
    }
    &__filters{
        display: flex;
    }
    &__datetime{
        display: flex;
        margin-left: 75px;
        flex-grow: 1;
        gap: 25px;
    }
}
</style>