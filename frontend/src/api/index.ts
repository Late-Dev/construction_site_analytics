import axios from "axios";


// const API_URL = "http://localhost:8000";
const API_URL = process.env.VUE_APP_API_URL
axios.defaults.baseURL = API_URL

export interface Video{
    url: String,
    construction_object: String,
    date: String
}

export function isAlive() {
    return axios.get(`/`)
}

export function addVideo(payload: Video){
    return axios.post('/add_video', payload)
}

export function getVideoList(){
    return axios.get('/get_video_list')
}

export function getVideoCard(_id: String){
    return axios.get('/get_video_card', { params: {_id}})
}

export function getReport(_id: String){
    axios.get('/get_report', { responseType: 'blob', params: {_id} })
      .then(response => {
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = 'report.json'
        link.click()
        URL.revokeObjectURL(link.href)
      }).catch(console.error)
}

export function getAnalytics(filter_type?: String, group?: String){
    
    return axios.get('/get_analytics', {params: {filter_type, group}})
}
//teacher, subject, student
