<template>

    <div class="upload-popup__wrapper" @click.self="mainStore.closePopup" >
        <div class="upload-popup" >
            <div v-if="!success">
                <div class="upload-popup__close"  @click="mainStore.closePopup">
                    <img src="@/assets/close.svg" alt="">
                </div>
                <div>
                    <DragNDrop @upload="videoUpload"></DragNDrop>
                </div>
                <div class="upload-popup__row">
                    <BaseSelect 
                    :options="[
                            {label: 'Школа Архангельск', value: 'Школа Архангельск'},
                            ]"
                    
                    
                    @input="(data)=>{payload.construction_object = data}" label="Строительный объект"/>
                </div>
                <div class="upload-popup__row">
                    <input type="date" v-model="date" style="width: 360px; height: 56px; background: #EFF0F6; border-radius: 6px; border: 0px; font-size: 14px; font-family: Poppins; font-weight: 400; line-height: 28px; letter-spacing: 0.75px; padding: 0px 12px;" />
                </div>
                <div class="upload-popup__row">
                    <BaseButton @click="submitVideo" :disabled="sending" type="secondary" class="upload-popup__button">Загрузить</BaseButton>
                </div>
            </div>
            <div v-if="success">
                <div class="upload-popup__close"  @click="mainStore.closePopup">
                    <img src="@/assets/close.svg" alt="">
                </div>
                <div class="upload-popup__success">
                    <img src="@/assets/Success.svg" alt="">
                </div>
                <div class="upload-popup__success-info">
                    <h2>Успех!</h2>
                        После того как видео обработается вы сможете посмотреть аналитику по нему в видеогалереe
                </div>
                <BaseButton @click="mainStore.closePopup"  type="secondary" class="upload-popup__button">Хорошо</BaseButton>
            
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import DragNDrop from "./DragNDrop.vue";
import BaseButton from "./BaseButton.vue";
import BaseSelect from "./BaseSelect.vue";

import { useMainStore } from "@/store/index";
import { onMounted, onUnmounted, ref } from "vue";

import { addVideo, Video} from '@/api/index'

const date = ref();

const payload = ref({
    url: '',
    construction_object: '',
    date: date
} as Video)

onMounted(()=>{
    window.addEventListener('keyup', escCloseModal)
})

onUnmounted(()=>{
    window.removeEventListener('keyup',escCloseModal)
})

function escCloseModal(e: any) {
     if(e.keyCode === 27) {
         mainStore.closePopup()
    }
}

const sending = ref(false)
const success = ref(false)

async function submitVideo(){
    sending.value = true
    addVideo(payload.value).then(()=>{
        sending.value = false
        success.value = true
    }).catch((error)=>{
        console.log(error)
        sending.value = false
    })
}

const mainStore = useMainStore();

function videoUpload(url: String){
    payload.value.url = url.replaceAll(' ', '_')
}


</script>

<style scoped lang="scss">
.upload-popup{
    height: 540px;
    width: 560px;
    background: white;
    margin: 150px auto;
    border-radius: 24px;
    padding: 90px;
    box-sizing: border-box;
    &__row{
        margin-top: 25px;
        display: flex;
        height: 56px;
    }

    &__class{
        width: 140px;
    }

    &__time{
        width: 195px;
        margin-left: auto;
    }

    &__wrapper{
        position: fixed;
        top:0;
        left:0;
        height: 100vh;
        width: 100vw;
        background: rgba($color: #000000, $alpha: 0.25);
    }
    &__close{
        position: relative;
        top: -60px;
        right:-60px;
        float: right;
        cursor: pointer;
    }
    &__button{
        margin: auto;
        width: 258px;
    }

    &__success{
        top:-10px;
        width: 100%;
        display: flex;
        justify-content: center;
        img{
            margin-top: -20px;
            width: 50%;
        }
        &-info{
            font-weight: 500;
            font-size: 16px;
            line-height: 28px;
            text-align: center;

            letter-spacing: 0.75px;
            margin-bottom: 20px;

            h2{
                font-weight: 600;
                font-size: 24px;
                line-height: 28px;

                text-align: center;
                letter-spacing: 0.75px;
            }
        }
    }
}



</style>