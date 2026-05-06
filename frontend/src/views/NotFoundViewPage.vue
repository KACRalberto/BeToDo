<template>
  <div class="not-found" ref="rootEl" tabindex="0">
    <div class="scanlines"></div>
    <div class="container">
      <div class="header">
        <div class="error-display">
          <span class="code-404">404</span>
          <div class="error-info">
            <span class="error-title">RUTA_NO_ENCONTRADA.EXE</span>
            <span class="error-sub">el proceso ha fallado — juega mientras tanto</span>
          </div>
        </div>
        <button class="home-btn" @click="goHome">
          <span class="arrow">←</span> VOLVER AL INICIO
        </button>
      </div>

      <div class="game-wrapper" @click="handleClick" @touchstart.prevent="handleClick">
        <canvas ref="canvasEl" :width="W" :height="H" class="game-canvas"></canvas>
        <transition name="fade">
          <div v-if="state !== 'playing'" class="overlay">
            <div v-if="state === 'idle'" class="overlay-content">
              <div class="prompt blink">[ CLICK O ESPACIO PARA INICIAR ]</div>
              <div class="hint-keys">
                <span class="key">SPACE</span>
                <span class="key-sep">/</span>
                <span class="key">↑</span>
                <span class="key-label">saltar</span>
              </div>
            </div>
            <div v-else-if="state === 'over'" class="overlay-content">
              <div class="over-title">// PROCESO_TERMINADO</div>
              <div class="over-score">SCORE: <span class="over-val">{{ score }}</span></div>
              <div v-if="isNewRecord" class="new-record blink-slow">★ NUEVO RÉCORD ★</div>
              <div class="prompt blink">[ CLICK O ESPACIO PARA REINTENTAR ]</div>
            </div>
          </div>
        </transition>
      </div>

      <div class="score-bar">
        <div class="score-item">
          <span class="score-label">SCORE</span>
          <span class="score-value">{{ scoreDisplay }}</span>
        </div>
        <span class="divider">|</span>
        <div class="score-item">
          <span class="score-label">BEST</span>
          <span class="score-value">{{ bestDisplay }}</span>
        </div>
        <div class="speed-block">
          <span class="score-label">VELOCIDAD</span>
          <div class="speed-track">
            <div class="speed-fill" :style="{ width: speedPct + '%' }"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const rootEl = ref(null)
const canvasEl = ref(null)

const W = 800
const H = 200
const GROUND_Y = H - 42
const PH = 30
const PLAYER_X = 85

const GRAVITY = 0.68
const JUMP_FORCE = -14.5
const BASE_SPEED = 5
const MAX_SPEED = 13

const state = ref('idle')
const score = ref(0)
const highScore = ref(0)
const isNewRecord = ref(false)

const scoreDisplay = computed(() => String(score.value).padStart(6, '0'))
const bestDisplay = computed(() => String(highScore.value).padStart(6, '0'))
const speedPct = computed(() => {
  return Math.min(100, ((currentSpeed - BASE_SPEED) / (MAX_SPEED - BASE_SPEED)) * 100)
})

let ctx = null
let raf = null
let currentSpeed = BASE_SPEED
let frameCount = 0
let player = null
let obstacles = []
let groundParticles = []

const LABELS = ['404', 'ERR', 'NUL', 'BUG', 'NaN', '???', 'UND', 'EXC']

function mkPlayer() {
  return { x: PLAYER_X, y: GROUND_Y, vy: 0, onGround: true, frame: 0, frameT: 0, dead: false }
}

function drawPlayer(x, y, onGround, frame, dead) {
  const pw = 22
  const glow = dead ? '#ff4455' : '#00ff88'
  const bodyCol = dead ? '#882233' : '#00aa55'
  const darkCol = '#001a08'

  if (!dead) {
    ctx.fillStyle = '#00ff1112'
    ctx.fillRect(x - 3, GROUND_Y + PH - 2, pw + 6, 5)
  }

  ctx.fillStyle = bodyCol
  ctx.fillRect(x + 3, y + 8, pw - 6, PH - 8)

  ctx.fillStyle = glow
  ctx.fillRect(x, y, pw, 13)

  ctx.fillStyle = darkCol
  ctx.fillRect(x + 3, y + 3, 5, 5)
  ctx.fillRect(x + pw - 8, y + 3, 5, 5)

  if (!dead) {
    ctx.fillStyle = '#00ffaa'
    ctx.fillRect(x + 4, y + 4, 2, 2)
    ctx.fillRect(x + pw - 7, y + 4, 2, 2)
  } else {
    ctx.strokeStyle = '#ff6677'
    ctx.lineWidth = 1.5
    ctx.beginPath()
    ctx.moveTo(x + 3, y + 3)
    ctx.lineTo(x + 8, y + 8)
    ctx.moveTo(x + 8, y + 3)
    ctx.lineTo(x + 3, y + 8)
    ctx.moveTo(x + pw - 8, y + 3)
    ctx.lineTo(x + pw - 3, y + 8)
    ctx.moveTo(x + pw - 3, y + 3)
    ctx.lineTo(x + pw - 8, y + 8)
    ctx.stroke()
  }

  ctx.strokeStyle = glow
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(x + pw / 2, y)
  ctx.lineTo(x + pw / 2, y - 7)
  ctx.stroke()
  
  ctx.fillStyle = dead ? '#ff6677' : '#00ffcc'
  ctx.beginPath()
  ctx.arc(x + pw / 2, y - 9, 3, 0, Math.PI * 2)
  ctx.fill()

  ctx.fillStyle = dead ? '#882233' : '#008844'
  if (onGround && !dead) {
    const even = frame % 2 === 0
    ctx.fillRect(x + 3, y + PH - (even ? 8 : 12), 7, even ? 8 : 12)
    ctx.fillRect(x + pw - 10, y + PH - (!even ? 8 : 12), 7, !even ? 8 : 12)
  } else {
    ctx.fillRect(x + 1, y + PH - 10, 8, 10)
    ctx.fillRect(x + pw - 9, y + PH - 10, 8, 10)
  }

  ctx.fillStyle = dead ? '#ff221133' : '#00ff8820'
  ctx.fillRect(x + 5, y + 10, pw - 10, 7)
}

function spawnObstacle() {
  const h = 28 + Math.random() * 22
  const label = LABELS[Math.floor(Math.random() * LABELS.length)]
  obstacles.push({ x: W + 10, y: GROUND_Y + PH - h, w: 46, h, label })

  if (score.value > 250 && Math.random() < 0.25) {
    const h2 = 20 + Math.random() * 20
    obstacles.push({
      x: W + 70,
      y: GROUND_Y + PH - h2,
      w: 46,
      h: h2,
      label: LABELS[Math.floor(Math.random() * LABELS.length)]
    })
  }
}

function drawObstacle(obs) {
  ctx.fillStyle = '#0d0003'
  ctx.fillRect(obs.x, obs.y, obs.w, obs.h)

  ctx.strokeStyle = '#ff4455'
  ctx.lineWidth = 1.5
  ctx.strokeRect(obs.x, obs.y, obs.w, obs.h)

  ctx.strokeStyle = '#ff7788'
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.moveTo(obs.x, obs.y)
  ctx.lineTo(obs.x + obs.w, obs.y)
  ctx.stroke()

  ctx.fillStyle = '#ff5566'
  ctx.font = 'bold 10px "Courier New", monospace'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText(obs.label, obs.x + obs.w / 2, obs.y + obs.h / 2)
}

function spawnGroundParticles() {
  groundParticles.push({
    x: W + 5,
    y: GROUND_Y + PH + 3 + Math.random() * 4,
    w: 4 + Math.random() * 16,
    alpha: 0.25 + Math.random() * 0.2
  })
  if (groundParticles.length > 20) groundParticles.shift()
}

function update() {
  frameCount++
  if (frameCount % 5 === 0) score.value++

  currentSpeed = Math.min(MAX_SPEED, BASE_SPEED + score.value * 0.008)

  const interval = Math.max(44, 110 - Math.floor(score.value / 70) * 6)
  if (frameCount % interval === 0) spawnObstacle()

  if (frameCount % 12 === 0) spawnGroundParticles()

  player.vy += GRAVITY
  player.y += player.vy
  
  if (player.y >= GROUND_Y) {
    player.y = GROUND_Y
    player.vy = 0
    player.onGround = true
  }

  if (player.onGround) {
    player.frameT++
    if (player.frameT > 7) {
      player.frame = (player.frame + 1) % 4
      player.frameT = 0
    }
  }

  for (let i = obstacles.length - 1; i >= 0; i--) {
    obstacles[i].x -= currentSpeed
    if (obstacles[i].x < -60) obstacles.splice(i, 1)
  }
  
  for (let i = groundParticles.length - 1; i >= 0; i--) {
    groundParticles[i].x -= currentSpeed * 0.4
    if (groundParticles[i].x < -30) groundParticles.splice(i, 1)
  }

  const m = 5
  for (const obs of obstacles) {
    if (
      player.x + 22 - m > obs.x + m &&
      player.x + m < obs.x + obs.w - m &&
      player.y + PH - m > obs.y + m
    ) {
      endGame()
      return
    }
  }
}

function draw() {
  ctx.clearRect(0, 0, W, H)

  ctx.strokeStyle = '#00ff1108'
  ctx.lineWidth = 1
  for (let x = 0; x < W; x += 50) {
    ctx.beginPath()
    ctx.moveTo(x, 0)
    ctx.lineTo(x, H)
    ctx.stroke()
  }

  for (const p of groundParticles) {
    ctx.fillStyle = `rgba(0, 255, 68, ${p.alpha})`
    ctx.fillRect(p.x, p.y, p.w, 2)
  }

  ctx.strokeStyle = '#00ff4488'
  ctx.lineWidth = 1.5
  ctx.setLineDash([])
  ctx.beginPath()
  ctx.moveTo(0, GROUND_Y + PH)
  ctx.lineTo(W, GROUND_Y + PH)
  ctx.stroke()

  ctx.strokeStyle = '#00ff4422'
  ctx.lineWidth = 1
  ctx.setLineDash([6, 12])
  ctx.beginPath()
  ctx.moveTo(0, GROUND_Y + PH + 4)
  ctx.lineTo(W, GROUND_Y + PH + 4)
  ctx.stroke()
  ctx.setLineDash([])

  for (const obs of obstacles) drawObstacle(obs)

  drawPlayer(player.x, player.y, player.onGround, player.frame, player.dead)
}

function jump() {
  if (state.value === 'idle' || state.value === 'over') {
    startGame()
    return
  }
  if (player.onGround && state.value === 'playing') {
    player.vy = JUMP_FORCE
    player.onGround = false
  }
}

function startGame() {
  player = mkPlayer()
  obstacles = []
  groundParticles = []
  frameCount = 0
  currentSpeed = BASE_SPEED
  score.value = 0
  isNewRecord.value = false
  state.value = 'playing'
  loop()
}

function endGame() {
  cancelAnimationFrame(raf)
  player.dead = true
  if (score.value > highScore.value) {
    highScore.value = score.value
    isNewRecord.value = true
  }
  state.value = 'over'
  draw()
}

function loop() {
  if (state.value !== 'playing') return
  update()
  draw()
  raf = requestAnimationFrame(loop)
}

function handleClick() {
  jump()
}

function handleKey(e) {
  if (e.code === 'Space' || e.code === 'ArrowUp') {
    e.preventDefault()
    jump()
  }
}

function goHome() {
  router.push('/')
}

function drawIdleFrame() {
  if (!ctx) return
  player = mkPlayer()
  ctx.clearRect(0, 0, W, H)
  ctx.strokeStyle = '#00ff4488'
  ctx.lineWidth = 1.5
  ctx.beginPath()
  ctx.moveTo(0, GROUND_Y + PH)
  ctx.lineTo(W, GROUND_Y + PH)
  ctx.stroke()
  drawPlayer(player.x, player.y, true, 0, false)
}

onMounted(() => {
  ctx = canvasEl.value.getContext('2d')
  drawIdleFrame()
  window.addEventListener('keydown', handleKey)
  rootEl.value?.focus()
})

onUnmounted(() => {
  cancelAnimationFrame(raf)
  window.removeEventListener('keydown', handleKey)
})
</script>

<style scoped>
.not-found {
  position: relative;
  min-height: 100%;
  width: 100%;
  background: linear-gradient(180deg, #13191f 0%, #090b0f 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Courier New', Courier, monospace;
  overflow: hidden;
  outline: none;
  padding: 3rem 0;
}

.scanlines {
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(255, 82, 82, 0.02) 2px,
    rgba(255, 82, 82, 0.02) 4px
  );
  pointer-events: none;
  z-index: 20;
}

.container {
  width: min(940px, 95vw);
  padding: 2rem;
  background: rgba(14, 19, 27, 0.94);
  border: 1px solid rgba(255, 82, 82, 0.12);
  border-radius: 28px;
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(12px);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.8rem;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem 1.2rem;
  border-radius: 24px;
  background: rgba(2, 5, 10, 0.82);
  border: 1px solid rgba(0, 255, 136, 0.12);
}

.error-display {
  display: flex;
  align-items: center;
  gap: 1.2rem;
}

.code-404 {
  font-size: clamp(3rem, 8vw, 5rem);
  font-weight: 900;
  color: #ff5252;
  letter-spacing: -4px;
  line-height: 1;
  animation: glitch 5s infinite;
}

@keyframes glitch {
  0%, 90%, 100% { color: #ff5252; text-shadow: none; transform: translate(0); }
  91% { transform: translate(-3px, 1px); color: #00ff88; }
  92% { transform: translate(3px, -1px); text-shadow: -3px 0 #ff5252; }
  93% { transform: translate(0); color: #ff5252; text-shadow: none; }
  95% { transform: translate(2px, 0); text-shadow: -2px 0 #00ff88; }
  96% { transform: translate(0); text-shadow: none; }
}

.error-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.error-title {
  color: #ffffff;
  font-size: clamp(0.7rem, 1.4vw, 0.95rem);
  letter-spacing: 2px;
}

.error-sub {
  color: #a7b8c4;
  font-size: clamp(0.6rem, 1.2vw, 0.78rem);
  letter-spacing: 1px;
}

.home-btn {
  background: linear-gradient(135deg, #ff5252, #ff7b79);
  border: none;
  color: white;
  font-family: inherit;
  font-size: clamp(0.65rem, 1.5vw, 0.8rem);
  letter-spacing: 1.4px;
  padding: 12px 24px;
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease;
  white-space: nowrap;
  border-radius: 999px;
  box-shadow: 0 12px 24px rgba(255, 82, 82, 0.18);
}

.home-btn:hover {
  opacity: 0.98;
  transform: translateY(-1px);
  box-shadow: 0 16px 30px rgba(255, 82, 82, 0.28);
}

.home-btn .arrow {
  display: inline-block;
  transition: transform 0.2s;
}

.home-btn:hover .arrow { transform: translateX(-4px); }

.game-wrapper {
  position: relative;
  cursor: pointer;
  border: 1px solid rgba(0, 255, 136, 0.16);
  user-select: none;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: inset 0 0 35px rgba(0, 255, 136, 0.08), 0 20px 60px rgba(0, 0, 0, 0.35);
}

.game-canvas {
  display: block;
  width: 100%;
  height: auto;
  background: radial-gradient(circle at top, #0c190d 0%, #041005 100%);
}

.overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.74);
}

.overlay-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  text-align: center;
  padding: 1rem 1.2rem;
}

.over-title {
  color: #ff6e6e;
  font-size: clamp(0.75rem, 2vw, 1rem);
  letter-spacing: 3px;
  margin-bottom: 2px;
}

.over-score {
  color: #00ff88;
  font-size: clamp(0.9rem, 2.5vw, 1.3rem);
  letter-spacing: 4px;
}

.over-val {
  color: #ffffff;
}

.new-record {
  color: #ffcc22;
  font-size: clamp(0.65rem, 1.5vw, 0.82rem);
  letter-spacing: 3px;
}

.prompt {
  color: #ffffff;
  font-size: clamp(0.7rem, 1.5vw, 0.82rem);
  letter-spacing: 2px;
}

.blink { animation: blink 1.1s step-end infinite; }
.blink-slow { animation: blink 1.8s step-end infinite; }

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.hint-keys {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-top: 2px;
}

.key {
  border: 1px solid rgba(255, 255, 255, 0.12);
  padding: 5px 10px;
  color: #ffffffcc;
  font-family: inherit;
  font-size: 0.72rem;
  letter-spacing: 0.02em;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.04);
}

.key-sep {
  color: #ffffff44;
  font-size: 0.78rem;
}

.key-label {
  color: #ffffff88;
  font-size: 0.72rem;
  letter-spacing: 1px;
}

.score-bar {
  display: flex;
  align-items: center;
  gap: 1.4rem;
  padding: 14px 18px;
  border: 1px solid rgba(0, 255, 136, 0.15);
  border-top: none;
  background: rgba(7, 14, 11, 0.94);
  flex-wrap: wrap;
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.score-label {
  color: #c4f9d1;
  font-size: clamp(0.55rem, 1.2vw, 0.68rem);
  letter-spacing: 1.6px;
}

.score-value {
  color: #ffffff;
  font-size: clamp(0.8rem, 2vw, 1rem);
  letter-spacing: 2px;
}

.divider {
  color: rgba(255, 255, 255, 0.18);
  font-size: 1.2rem;
}

.speed-block {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.speed-track {
  width: 100px;
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(0, 255, 136, 0.18);
  border-radius: 999px;
}

.speed-fill {
  height: 100%;
  background: linear-gradient(90deg, #00ff88, #74ffa3);
  transition: width 0.35s ease;
  border-radius: 999px;
  box-shadow: 0 0 10px rgba(0, 255, 136, 0.35);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>