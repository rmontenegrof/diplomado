<template>
  <div class="w-full h-96">
    <ResponsiveContainer>
      <LineChart :data="data">
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="anho" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="yhat" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  </div>
</template>

<script setup>
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const props = defineProps({
  data: Array
})
</script>

