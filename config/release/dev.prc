# Distribution:
distribution dev

# Art assets:
model-path ../resources

# Server:
server-version toontown-dev
min-access-level 600
accountdb-type developer
shard-low-pop 50
shard-mid-pop 100

# RPC:
want-rpc-server #f
rpc-server-endpoint http://localhost:8080/

# DClass files (in reverse order):
dc-file astron/dclass/toon.dc
dc-file astron/dclass/otp.dc

# Core features:
want-pets #t
want-parties #t
want-cogdominiums #f
want-code-redemption #t

# Chat:
want-whitelist #f

# Cashbot boss:
want-resistance-toonup #t
want-resistance-restock #t
want-resistance-dance #t

# Developer options:
show-population #t
force-skip-tutorial #t
want-instant-parties #t
