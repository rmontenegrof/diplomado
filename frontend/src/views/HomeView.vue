<template>
  <div>
    <h1>Indicadores</h1>
    <table>
      <tr><th>Período</th><td>{{ indicadores.anio_inicio }} - {{ indicadores.anio_fin }}</td></tr>
      <tr><th>Total carreras</th><td>{{ indicadores.total_carreras }}</td></tr>
      <tr><th>Total matrículas</th><td>{{ indicadores.total_matriculas }}</td></tr>
      <tr><th>Promedio por carrera</th><td>{{ indicadores.promedio_matriculas_por_carrera }}</td></tr>
    </table>

    <h2 class="mt-5">Pronósticos</h2>
    <LineChart :data="chartData" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import axios from 'axios'
import LineChart from '../components/LineChart.vue'

const indicadores = ref<any>({})
const chartData = ref<any>({})

onMounted(async () => {
  const indRes = await axios.get('http://localhost:5000/api/indicadores')
  indicadores.value = indRes.data

  const proRes = await axios.get('http://localhost:5000/api/pronosticos')
  const pronosticos = proRes.data

  chartData.value = {
    labels: pronosticos.map((p: any) => p.ds.split(' ')[3]), // Año
    datasets: [
      {
        label: 'Pronóstico (yhat)',
        data: pronosticos.map((p: any) => p.yhat),
        fill: false,
        borderColor: 'blue',
      },
      {
        label: 'Inferior',
        data: pronosticos.map((p: any) => p.yhat_lower),
        borderDash: [5, 5],
        borderColor: 'gray',
        fill: false,
      },
      {
        label: 'Superior',
        data: pronosticos.map((p: any) => p.yhat_upper),
        borderDash: [5, 5],
        borderColor: 'gray',
        fill: false,
      },
    ]
  }
})
</script>

<style scoped>
table {
  border-collapse: collapse;
}
td, th {
  border: 1px solid #aaa;
  padding: 8px;
}
</style>

