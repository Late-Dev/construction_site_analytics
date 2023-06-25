<template>
    <div class="analytics">
        <BaseHeader>Аналитика загруженного видео</BaseHeader>
        <EmptyCard>
            <video :src="mainStore.video.url" controls></video>
            <p>
              {{mainStore.video.name}}
            </p>
            
        </EmptyCard>
        <BaseButton type="secondary" class="download__button" @click="downloadReport()" style="width: 300px; margin: 20px"> Скачать отчет (json) </BaseButton>

        <EmptyCard class="analytics__card">
          <template #header>
                Активность техники
            </template>
            <BaseSelect @input="selectStudent" :options="lineOptions" label="Номер техники"></BaseSelect>
        </EmptyCard>
        <div>
          <LineChartCard :dataValues="dt" v-for="dt, name in lineData" :key="dt" class="analytics__card" :header="name"></LineChartCard>
        </div>
    </div>
</template>

<script setup >
import EmptyCard from "./EmptyCard.vue"
import BaseHeader from "./BaseHeader.vue"
import BaseButton from "./BaseButton.vue";
import { useMainStore } from "@/store/index";
import { ref, computed, onMounted} from 'vue'
// import { ref, onMounted} from 'vue'

// import { BarChart, useBarChart } from "vue-chart-3";
import { Chart,  registerables } from "chart.js";
import { getVideoCard } from '@/api/index'
import BaseSelect from "./BaseSelect.vue";
import LineChartCard from "./LineChartCard.vue";
import { getReport} from '@/api/index'


const mainStore = useMainStore();

async function downloadReport () {
  await getReport(mainStore.video._id)
}

onMounted(async ()=>{
  const resp = await getVideoCard(mainStore.video._id)
  console.log(resp)
  videoCard.value = resp.data
})

const videoCard = ref({} )

Chart.register(...registerables);

// bar_data" : { "names" : [ "гнев", "грусть", "отвращение", "радость", "спокойствие", "страх", "удивление" ], "values" : [ 0.07174072510112016, 0.100061056220386, 0.025056007966937802, 0.28290127535625237, 0.468341065879695, 0.025505640514629852, 0.02639422875556299 ]

// const dataValues = computed(()=>videoCard.value.bar_data?.values);

// const dataLabels = computed(()=>videoCard.value.bar_data?.names);

const lineOptions = computed(()=>{
  if(videoCard.value.line_data !== undefined){
    console.log(videoCard.value.line_data)

    const names = Object.keys(videoCard.value.line_data)
    return names.map((item)=>({label:item, value: item,}))
  } 
  return [{label:'', value:''}]
})

const lineData = ref([])

function selectStudent(name){
  lineData.value = videoCard.value.line_data[name]
  console.log(lineData.value)
}

// const toggleLegend = ref(true); 
// console.log(toggleLegend)

// const testData = computed(() => ({
//       labels: dataLabels.value,
//       datasets: [
//         {
//           data: dataValues.value,
//           backgroundColor: [
//             "#ED2E7E",
//             "#6A96FF",
//             "#8F40F4",
//             "#F4B740",
//             "#B2FF36",
//             "#00BA88",
//             "#DC8CEC",
//           ],
//         },
//       ],
//     }));

// const options = computed(() => ({
//       scales: {
//         myScale: {
//           type: "linear",
//           position: toggleLegend.value ? "left" : "right",
//         },
//       },
//       plugins: {
//       },
//     }));


// const { barChartProps } = useBarChart({
//     // @ts-ignore
//       chartData: testData,
//       options,
//     });

// console.log(barChartRef)


</script>

<style lang="scss" scoped>
.analytics{
  margin-bottom: 300px;
  &__card{
    margin-top: 40px;
  }
}
</style>