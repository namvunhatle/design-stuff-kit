-- Procedural particle burst: radial launch, drag, gravity, glow (additive + feather).
-- Re-emits every `period` seconds so the effect can be reviewed on loop.
--
-- Rive Node script. Verified 2026-09-30: compiles with no diagnostics and the
-- designer saw the glowing particles when playing the scene. Add it to the
-- artboard by right-clicking the artboard, then set its X/Y to the emit origin
-- (the instance lands where you click, often outside the artboard).

type Particle = {
  x: number,
  y: number,
  vx: number,
  vy: number,
  age: number,
  life: number,
  size: number,
  tint: number,
}

type ParticleBurst = {
  count: Input<number>,
  speed: Input<number>,
  gravity: Input<number>,
  drag: Input<number>,
  period: Input<number>,
  particles: { Particle },
  paints: { Paint },
  paths: { Path },
  elapsed: number,
  seed: number,
}

local TWO_PI = math.pi * 2
local KAPPA = 0.5522847498

local function rand(self: ParticleBurst): number
  -- small deterministic LCG so every run looks the same
  self.seed = (self.seed * 1664525 + 1013904223) % 4294967296
  return self.seed / 4294967296
end

local function addCircle(path: Path, cx: number, cy: number, r: number)
  local k = r * KAPPA
  path:moveTo(Vector.xy(cx + r, cy))
  path:cubicTo(Vector.xy(cx + r, cy + k), Vector.xy(cx + k, cy + r), Vector.xy(cx, cy + r))
  path:cubicTo(Vector.xy(cx - k, cy + r), Vector.xy(cx - r, cy + k), Vector.xy(cx - r, cy))
  path:cubicTo(Vector.xy(cx - r, cy - k), Vector.xy(cx - k, cy - r), Vector.xy(cx, cy - r))
  path:cubicTo(Vector.xy(cx + k, cy - r), Vector.xy(cx + r, cy - k), Vector.xy(cx + r, cy))
  path:close()
end

local function emit(self: ParticleBurst)
  local n = math.floor(self.count)
  for _ = 1, n do
    local angle = rand(self) * TWO_PI
    local spd = self.speed * (0.25 + 0.75 * math.sqrt(rand(self)))
    table.insert(self.particles, {
      x = 0,
      y = 0,
      vx = math.cos(angle) * spd,
      vy = math.sin(angle) * spd,
      age = 0,
      life = 0.7 + rand(self) * 0.9,
      size = 1.5 + rand(self) * 3.5,
      tint = 1 + math.floor(rand(self) * 3),
    })
  end
end

function init(self: ParticleBurst): boolean
  self.particles = {}
  self.paths = { Path.new(), Path.new(), Path.new() }
  self.paints = {
    Paint.with({ style = 'fill', color = Color.rgba(255, 255, 255, 235), blendMode = 'additive', feather = 3 }),
    Paint.with({ style = 'fill', color = Color.rgba(185, 166, 255, 220), blendMode = 'additive', feather = 4 }),
    Paint.with({ style = 'fill', color = Color.rgba(139, 107, 255, 200), blendMode = 'additive', feather = 5 }),
  }
  self.elapsed = self.period -- emit on the first frame
  return true
end

function advance(self: ParticleBurst, seconds: number): boolean
  local dt = math.min(seconds, 1 / 30)

  self.elapsed += dt
  if self.elapsed >= self.period then
    self.elapsed = 0
    emit(self)
  end

  for i = 1, 3 do
    self.paths[i]:reset()
  end

  local alive = {}
  local damping = math.max(0, 1 - self.drag * dt)
  for _, p in self.particles do
    p.age += dt
    if p.age < p.life then
      p.vx *= damping
      p.vy = p.vy * damping + self.gravity * dt
      p.x += p.vx * dt
      p.y += p.vy * dt
      local t = p.age / p.life
      addCircle(self.paths[p.tint], p.x, p.y, p.size * (1 - t * t))
      table.insert(alive, p)
    end
  end
  self.particles = alive

  return true
end

function draw(self: ParticleBurst, renderer: Renderer)
  for i = 1, 3 do
    renderer:drawPath(self.paths[i], self.paints[i])
  end
end

return function(): Node<ParticleBurst>
  return {
    init = init,
    advance = advance,
    draw = draw,
    count = 72,
    speed = 520,
    gravity = 380,
    drag = 1.6,
    period = 3.2,
    particles = late(),
    paints = late(),
    paths = late(),
    elapsed = 0,
    seed = 1337,
  }
end
