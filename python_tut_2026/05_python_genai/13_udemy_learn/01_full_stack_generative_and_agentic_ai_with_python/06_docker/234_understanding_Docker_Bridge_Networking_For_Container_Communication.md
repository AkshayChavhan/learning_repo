# Docker Networking — The Default Bridge

When you install Docker, it creates a private network on your laptop called **bridge**.
Every container you start is plugged into it. That's why a container can reach the
internet, and why two containers can talk to each other using their IP addresses.

---

## 1. The surprise: a container has internet

```bash
docker run -it busybox
ping google.com          # works
ping piyushgarg.dev      # works
```

You never set up any network. So whose internet is it? Whose IP address?

**Answer:** Docker made a network for you. The container is plugged into it, and that
network is connected to your laptop's internet.

---

## 2. The picture

```text
   INTERNET
      │
   Wi-Fi router
      │
   YOUR LAPTOP (host)  ── IP like 192.168.x.x
      │
   docker's "bridge" network  ── 172.17.0.1   (made when Docker installed)
      ├── my_container   172.17.0.2
      └── container_2    172.17.0.3
```

| Thing | What it is |
|---|---|
| **host** | your laptop |
| **bridge** | a private network Docker creates inside your laptop |
| **container IP** | an address on that private network, given automatically (DHCP) |

Containers on the same bridge are like devices on the same Wi-Fi: they can see each other.

---

## 3. See it yourself

### List the networks

```bash
docker network ls
```

```text
NETWORK ID     NAME      DRIVER    SCOPE
a1b2c3d4e5f6   bridge    bridge    local      ← the default. Containers join this
f6e5d4c3b2a1   host      host      local
0a1b2c3d4e5f   none      null      local
```

Three come built in. **bridge** is the one used unless you say otherwise. (`host` and
`none` are later topics.)

### Start two containers

```bash
docker run -itd --rm --name my_container busybox
docker run -itd --rm --name container_2 busybox
```

| Flag | Meaning |
|---|---|
| `-itd` | interactive + terminal + **detached** (runs in background) |
| `--rm` | delete the container when it stops |
| `--name` | give it a name |

### Look inside the bridge

```bash
docker network inspect bridge
```

```text
"Containers": {
    "...": { "Name": "my_container", "IPv4Address": "172.17.0.2/16" },
    "...": { "Name": "container_2",  "IPv4Address": "172.17.0.3/16" }
}
```

Both containers are listed, each with its own IP. Same network.

---

## 4. Containers talking to each other

`docker exec` = run a command **inside** a running container.

```bash
docker exec container_2 ping 172.17.0.2      # ping my_container by IP
```

```text
64 bytes from 172.17.0.2: seq=0 ttl=64 time=0.1 ms    ← works
```

```bash
docker exec container_2 ping 172.17.0.6      # an IP nobody has
```

```text
(hangs, no reply)                                      ← nothing there
```

```bash
docker exec container_2 ping my_container    # by NAME
```

```text
ping: bad address 'my_container'                       ← does NOT work on default bridge
```

| On the default bridge | |
|---|---|
| ping by **IP** | ✅ |
| ping by **name** | ❌ (fixed by user-defined bridges, next lecture) |

---

## 5. Why this matters: microservices

```text
   INTERNET ──► node.js app (172.17.0.2, port 8000 published with -p)
                    │
                    ├──► redis     (172.17.0.3)   private, NOT published
                    └──► postgres  (172.17.0.4)   private, NOT published
```

- The **app** is exposed to the world with `-p`.
- **Redis and Postgres** stay hidden. No `-p`, no public address. Only the app can reach
  them, because they share the bridge.
- Exposing a database to the internet is a security risk. The bridge lets you avoid it.

---

## 6. Two kinds of bridge (preview)

| | Default bridge (`bridge`) | User-defined bridge (next lecture) |
|---|---|---|
| Created | automatically by Docker | by you, `docker network create` |
| Talk by IP | ✅ | ✅ |
| Talk by **name** | ❌ | ✅ automatic DNS |
| Isolation | all containers share it | only containers you add |
| Docker's advice | fine for testing | **use this** for real apps |

---

## Remember

| Term | One line |
|---|---|
| **bridge** | Docker's default private network on your laptop |
| **container IP** | 172.17.0.x, given automatically |
| **`docker network ls`** | list networks |
| **`docker network inspect bridge`** | see which containers are on it, with IPs |
| **`docker exec <container> <cmd>`** | run a command inside a running container |
| **same network = can talk** | by IP on default bridge; by name on user-defined |
| **keep databases private** | publish only the app with `-p` |

> **If someone asks in an interview:** "How do two containers on one host communicate?"
> They're both attached to Docker's bridge network, so each gets a private IP and they
> can reach each other directly. On the default bridge you use IPs; on a user-defined
> bridge you can use container names.
