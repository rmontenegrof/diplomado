<template>
  <div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip
} from 'chart.js'

Chart.register(LineController, LineElement, PointElement, LinearScale, Title, CategoryScale, Tooltip)

const props = defineProps<{ data: any }>()
const canvas = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null

watch(() => props.data, (newData) => {
  if (chartInstance) chartInstance.destroy()
  if (!canvas.value) return
  chartInstance = new Chart(canvas.value, {
    type: 'line',
    data: newData,
    options: {
      responsive: true,
      plugins: {
        title: { display: true, text: 'Pronóstico de Matrículas' }
      }
    }
  })
}, { immediate: true })
</script>

