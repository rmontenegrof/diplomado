<template>
  <div>
    <h2>Pronóstico de Matrículas</h2>

    <div v-if="loading">Cargando datos...</div>
    <div v-else-if="error">{{ error }}</div>

    <canvas ref="grafico" width="600" height="400"></canvas>

    <table v-if="datos.length" border="1" style="margin-top: 20px;">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Pronóstico</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in datos" :key="index">
          <td>{{ item.ds }}</td>
          <td>{{ item.yhat.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

export default {
  name: 'Pronosticos',
  data() {
    return {
      datos: [],
      loading: true,
      error: null,
      chart: null,
    }
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('/api/pronosticos')
        if (!response.ok) throw new Error('Error al obtener datos de la API')
        const data = await response.json()

        if (!Array.isArray(data) || data.length === 0) {
          throw new Error('Datos vacíos o malformateados')
        }

        this.datos = data
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
        this.$nextTick(() => this.renderChart())
      }
    },
    renderChart() {
      if (!this.$refs.grafico) return console.error('Canvas no encontrado')

      const labels = this.datos.map(item => item.ds)
      const values = this.datos.map(item => item.yhat)

      if (this.chart) this.chart.destroy()

      this.chart = new Chart(this.$refs.grafico, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Total Matrículas',
            data: values,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 2,
            fill: false,
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: false,
              title: {
                display: true,
                text: 'Cantidad'
              }
            },
            x: {
              title: {
                display: true,
                text: 'Año'
              }
            }
          }
        }
      })
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>

