<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Pronósticos de Matrículas</h1>

    <div class="flex space-x-4 mb-4">
      <select v-model="filtroSexo" class="border rounded p-2">
        <option :value="null">Todos los sexos</option>
        <option value="0">Masculino</option>
        <option value="1">Femenino</option>
      </select>

      <select v-model="filtroViaIngreso" class="border rounded p-2">
        <option :value="null">Todas las vías</option>
        <option v-for="via in viasDisponibles" :key="via" :value="via">
          {{ via }}
        </option>
      </select>
    </div>

    <div v-if="pronosticosFiltrados.length > 0">
      <table class="table-auto w-full border">
        <thead>
          <tr class="bg-gray-200">
            <th class="px-4 py-2">Año</th>
            <th class="px-4 py-2">Carrera</th>
            <th class="px-4 py-2">Sexo</th>
            <th class="px-4 py-2">Vía ingreso</th>
            <th class="px-4 py-2">Yhat</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in pronosticosFiltrados" :key="item.anho + '-' + item.carrera + '-' + item.sexo + '-' + item.via_ingreso">
            <td class="border px-4 py-2">{{ item.anho }}</td>
            <td class="border px-4 py-2">{{ item.carrera }}</td>
            <td class="border px-4 py-2">{{ item.sexo }}</td>
            <td class="border px-4 py-2">{{ item.via_ingreso }}</td>
            <td class="border px-4 py-2">{{ item.yhat.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-red-600 font-semibold">
      No hay datos para los filtros seleccionados.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const pronosticos = ref([])
const filtroSexo = ref(null)
const filtroViaIngreso = ref(null)
const viasDisponibles = ref([])

onMounted(async () => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || '/api'
    const response = await axios.get(`${apiUrl}/pronosticos`)

    if (Array.isArray(response.data)) {
      pronosticos.value = response.data

      // Cargar vías únicas desde los datos
      const vias = new Set(response.data.map(p => p.via_ingreso))
      viasDisponibles.value = Array.from(vias).sort((a, b) => a - b)
    } else {
      console.error('Respuesta inesperada:', response.data)
    }
  } catch (error) {
    console.error('Error al obtener pronósticos:', error)
  }
})

const pronosticosFiltrados = computed(() => {
  return pronosticos.value.filter(p => {
    const sexoMatch = filtroSexo.value === null || p.sexo === Number(filtroSexo.value)
    const viaMatch = filtroViaIngreso.value === null || p.via_ingreso === Number(filtroViaIngreso.value)
    return sexoMatch && viaMatch
  })
})
</script>

