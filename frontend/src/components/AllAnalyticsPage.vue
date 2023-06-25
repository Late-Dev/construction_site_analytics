<template>

    <div>
        <BaseHeader>Общая аналитика</BaseHeader>
        <EmptyCard>
            <template #header>
                Фильтр
            </template>
            <div class="row">

                <BaseSelect :options="[
                    {label: 'Школа Архангельск', value: 'Школа Архангельск'},
                ]" label="Строительный объект"
                @input="(data)=>{typeAnal = data}"
                 />
                <BaseSelect
                :options="[
                    {value:'tractor', label:'Трактор'},
                    {value:'digger', label:'Экскаватор'},
                    {value:'truck', label:'Грузовой автомобиль'},
                    {value:'crane', label:'Подъемный кран'}
                ]"
                @input="(data)=>{groupBy = data}"

                label="Техника" />
            </div>
            <div class="btn">

                <BaseButton  @click="search">Найти</BaseButton>
            </div>
        </EmptyCard>
        <div>
          <LineChartCard :dataValues="dt" v-for="dt, name in lineData" :key="dt" class="analytics__card" :header="name"></LineChartCard>
        </div>
        <!-- <BarChartCard class="cardbar" :header="name" :dataValues="graph.values" :dataLabels="graph.names"  :key="graph" v-for="graph, name in graphs">
           
        </BarChartCard> -->
    </div>

</template>
<script setup>

import BaseHeader from './BaseHeader.vue';
import EmptyCard from './EmptyCard.vue';
import BaseSelect from './BaseSelect.vue';
import { onMounted, ref } from 'vue';
import { getAnalytics } from '@/api/index'
import BaseButton from './BaseButton.vue';
import LineChartCard from "./LineChartCard.vue";
// import BarChartCard from './BarChartCard.vue';


const lineData = ref([])

const typeAnal = ref('')

const groupBy = ref('')

onMounted(async ()=>{
})

// const graphs = ref('')

async function search(){
    const resp = await getAnalytics(typeAnal.value, groupBy.value)
    lineData.value = resp.data
}




</script>

<style>
.row{
    display: flex;
    gap:25px;
}

.btn{
    width: 300px;
    margin-top: 25px;
    margin-left: auto;
}

.cardbar{
    margin-top: 25px;
}

</style>

<style lang="scss" scoped>
.analytics{
  margin-bottom: 300px;
  &__card{
    margin-top: 40px;
  }
}
</style>