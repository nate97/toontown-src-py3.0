# Window settings:
window-title Toontown Online
win-origin -1 -1
icon-filename phase_3/etc/icon.ico
cursor-filename phase_3/etc/toonmono.cur

# Audio:
# Broken on linux
# audio-library-name p3fmod_audio

# Graphics:
aux-display pandagl
aux-display pandadx9
aux-display p3tinydisplay

# Disable antialiasing
framebuffer-multisample 1
multisamples 2

show-frame-rate-meter #t

# Models:
model-cache-models #t
model-cache-textures #t
default-model-extension .bam

# Textures:
texture-anisotropic-degree 16

# Performance
#matrix-palette 1
#vertex-buffers 1
#display-list-animation 1
#hardware-animated-vertices 1

# Preferences:
preferences-filename preferences.json

# Content packs:
content-packs-filepath contentpacks/
content-packs-sort-filename sort.yaml

# Injector:
want-injector #f

# Backups:
backups-filepath backups/
backups-extension .json

# Server:
server-timezone EST/EDT/-6
server-port 7199 # Port for directly connecting to Astron
#server-port 7555 # Port used for reverse proxy server
account-server-endpoint https://toontowninfinite.com/api/
account-bridge-filename astron/databases/account-bridge.db

# SSL
#server-force-ssl #t
#client-unverified-ssl #t

# Performance:
sync-video #f
texture-power-2 none
gl-check-errors #f
#Garbage collect status is currently broken
#garbage-collect-states #f


# Egg object types:
egg-object-type-barrier <Scalar> collide-mask { 0x01 } <Collide> { Polyset descend }
egg-object-type-trigger <Scalar> collide-mask { 0x01 } <Collide> { Polyset descend intangible }
egg-object-type-sphere <Scalar> collide-mask { 0x01 } <Collide> { Sphere descend }
egg-object-type-trigger-sphere <Scalar> collide-mask { 0x01 } <Collide> { Sphere descend intangible }
egg-object-type-floor <Scalar> collide-mask { 0x02 } <Collide> { Polyset descend }
egg-object-type-dupefloor <Scalar> collide-mask { 0x02 } <Collide> { Polyset keep descend }
egg-object-type-camera-collide <Scalar> collide-mask { 0x04 } <Collide> { Polyset descend }
egg-object-type-camera-collide-sphere <Scalar> collide-mask { 0x04 } <Collide> { Sphere descend }
egg-object-type-camera-barrier <Scalar> collide-mask { 0x05 } <Collide> { Polyset descend }
egg-object-type-camera-barrier-sphere <Scalar> collide-mask { 0x05 } <Collide> { Sphere descend }
egg-object-type-model <Model> { 1 }
egg-object-type-dcs <DCS> { 1 }

# Safe zones:
want-safe-zones #t
want-toontown-central #t
want-donalds-dock #t
want-daisys-garden #t
want-minnies-melodyland #t
want-the-burrrgh #t
want-donalds-dreamland #t
want-goofy-speedway #t
want-outdoor-zone #t
want-golf-zone #t

# Safe zone settings:
want-treasure-planners #t
want-suit-planners #t
want-butterflies #t

# Classic characters:
want-classic-chars #t
want-mickey #t
want-donald-dock #t
want-daisy #t
want-minnie #t
want-pluto #t
want-donald-dreamland #t
want-chip-and-dale #t
want-goofy #t

# Trolley minigames:
want-minigames #t
want-photo-game #t
want-travel-game #t

# Picnic table board games:
want-game-tables #f

# Cog headquarters:
want-cog-headquarters #t
want-sellbot-headquarters #t
want-cashbot-headquarters #t
want-lawbot-headquarters #t
want-bossbot-headquarters #t

# Cashbot boss:
want-resistance-toonup #t
want-resistance-restock #t
want-resistance-dance #t

# Cog battles:
base-xp-multiplier 1.0

# Cog buildings:
want-cogbuildings #t

# Optional:
show-total-population #t
want-mat-all-tailors #t
want-long-pattern-game #f
want-code-redemption #t

want-parties #t

# Developer options:
want-dev #f
want-pstats 0

# Temporary:
smooth-lag 0.4

# Live updates:
want-live-updates #t


# Halloween
#want-halloween #t
#active-holidays 60, 64, 65, 66, 3, 26, 27, 13

#side-by-side-stereo 1



