# User-Defined Bridge Networks — Names, Isolation, Attach/Detach

You can create your **own** bridge network. Containers on it get two things the default
bridge doesn't give: they can call each other **by name**, and they're **isolated** from
containers on other networks. You can also **plug containers in and out** while they run,
though that works on the default bridge too. Always use your own network for real apps.

---

## 1. Create a network

```bash
docker network create milky_way
docker network ls
```

```text
NETWORK ID     NAME        DRIVER    SCOPE
a1b2c3d4e5f6   bridge      bridge    local     ← default
9f8e7d6c5b4a   milky_way   bridge    local     ← yours. Same driver, separate network
```

It's a bridge like the default one, so it has internet. It's just **a different network**.

---

## 2. Put containers on it

Add `--network milky_way` to `docker run`:

```bash
docker run -itd --rm --network milky_way --name spiderman busybox
docker run -itd --rm --network milky_way --name ironman   busybox
docker run -itd --rm --network milky_way --name dr_strange nginx
```

```bash
docker network inspect milky_way
```

```text
"Containers": {
    "spiderman":  "172.19.0.2",
    "ironman":    "172.19.0.3",
    "dr_strange": "172.19.0.4"
}
```

Notice the IPs start with **172.19**, not 172.17. Different network, different range.

```text
   YOUR LAPTOP
   ├── bridge (default, 172.17.x)        ├── milky_way (yours, 172.19.x)
   │     ├── my_container  .2            │     ├── spiderman   .2
   │     └── container_2   .3            │     ├── ironman     .3
   │                                     │     └── dr_strange  .4
   │                                     │
   └────────── cannot reach ─────────────┘
```

---

## 3. Advantage 1: call by name

On the default bridge you had to ping by IP. Here, names work:

```bash
docker exec spiderman ping ironman
```

```text
PING ironman (172.19.0.3): 56 data bytes
64 bytes from 172.19.0.3: seq=0 ttl=64 time=0.1 ms     ← found the IP by itself
```

```bash
docker exec spiderman ping dr_strange      # also works
```

This is **automatic DNS**: Docker keeps a phone book of container name → IP for every
user-defined network.

**Why it matters:** your code can say "connect to `db`" or "connect to `redis`". No IP
addresses to remember, and it keeps working even if the IP changes on restart.

---

## 4. Advantage 2: isolation

```bash
docker exec spiderman ping container_2      # container_2 is on the DEFAULT bridge
```

```text
ping: bad address 'container_2'             ← cannot see it
```

```bash
docker exec container_2 ping 172.19.0.2     # the other direction, by IP
```

```text
(no reply)                                  ← still cannot
```

| From | To | Works? |
|---|---|---|
| milky_way → milky_way | spiderman → ironman | ✅ |
| milky_way → default bridge | spiderman → container_2 | ❌ |
| default bridge → milky_way | container_2 → spiderman | ❌ |

Each network is a **separate room**. Containers only see others in the same room.

---

## 5. Attach and detach while running

You don't have to decide the network at `docker run` time. (This works on the default
bridge as well. The docs list it as an advantage only compared to the old `--link` way,
where connections were fixed at `docker run`.)

```bash
docker network connect milky_way container_2     # plug container_2 into milky_way
docker exec spiderman ping container_2           # ✅ now works
```

```bash
docker network disconnect milky_way dr_strange   # unplug dr_strange
docker exec spiderman ping dr_strange            # ❌ bad address
```

A container can be on **more than one** network at once. `container_2` is now on both
the default bridge and milky_way.

| Command | Meaning |
|---|---|
| `docker network connect <net> <container>` | add a running container to a network |
| `docker network disconnect <net> <container>` | remove it from that network |

---

## 6. Delete a network

```bash
docker network rm milky_way
```

```text
Error: network milky_way has active endpoints    ← containers still on it
```

Stop or disconnect the containers first, then `rm` again.

---

## Default vs user-defined

| | Default `bridge` | User-defined (e.g. `milky_way`) |
|---|---|---|
| How you get it | automatic | `docker network create` |
| Join it | automatic | `--network <name>` or `network connect` |
| Talk by IP | ✅ | ✅ |
| Talk by **name** | ❌ | ✅ |
| Isolated from other networks | ❌ everything lands here | ✅ |
| Attach / detach live | ✅ (same) | ✅ (same) |
| Old `--link` trick | needed for names, shares env vars, **legacy / risky** | not needed |
| Use for | quick tests | **real apps** |

---

## Remember

| Term | One line |
|---|---|
| **`docker network create X`** | make your own bridge network |
| **`--network X`** | start a container on it |
| **`docker network inspect X`** | see who's on it and their IPs |
| **automatic DNS** | containers on a user-defined network reach each other by name |
| **isolation** | different networks can't see each other |
| **`network connect` / `disconnect`** | plug a running container in or out |
| **`docker network rm X`** | delete it, after containers leave |

> **If someone asks in an interview:** "Why use a user-defined bridge instead of the
> default?" Two reasons: name-based DNS between containers, and isolation from containers
> on other networks. The default bridge only offers IP-based access and puts every
> container in one shared network.

**Next:** Docker Compose will use exactly this to connect an app to Redis and Postgres by
name.
