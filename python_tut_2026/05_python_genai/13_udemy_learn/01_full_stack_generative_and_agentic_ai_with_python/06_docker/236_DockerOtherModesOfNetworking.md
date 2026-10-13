# Other Docker Network Modes — host, none, overlay, ipvlan, macvlan

Docker has more network modes than bridge. In practice you'll use **user-defined bridge**
almost always, **none** sometimes, and the rest rarely. This note tells you what each one
is so you recognise it when you see it.

---

## The whole list

| Mode | One line | How often you'll use it |
|---|---|---|
| **bridge** | Docker's private network on your laptop (notes 234, 235) | default |
| **user-defined bridge** | your own bridge, with names + isolation | **98% of real apps** |
| **host** | no isolation, container uses your laptop's network directly | rarely, and not on Mac |
| **none** | no network at all | sometimes, for sealed-off work |
| **overlay** | one network across **several** Docker machines | advanced (Swarm / clusters) |
| **ipvlan** | you control the container's IP addresses | advanced |
| **macvlan** | container looks like a **separate physical machine** on your Wi-Fi | advanced |

---

## 1. host

```bash
docker run -it --network host nginx
```

The container is **not** put in its own network. It shares your laptop's network
interface, like any normal program running on your machine.

| Effect | |
|---|---|
| No `-p` needed | if the app listens on 8000, it's already on `localhost:8000` |
| Same IP as your laptop | the container has no IP of its own |
| No isolation | the main safety feature of containers is gone |
| **Does not work properly on Mac** | known bug at the time of the lecture. Linux only, really |

**Verdict:** not recommended. Use `-p` with a bridge instead.

---

## 2. none

```bash
docker run -it --rm --network none busybox
```

```text
/ # ping google.com
ping: bad address 'google.com'
/ # ping 1.1.1.1
ping: sendto: Network is unreachable
```

No network at all. Not even to your laptop. Nothing in, nothing out.

**When you want this:**

- running untrusted code and you must be sure it can't call home
- processing sensitive data where no outward call should be possible
- a pure calculation job that needs no network anyway

---

## 3. overlay

```text
   Docker machine A ───┐
                       ├── one overlay network ── containers on A and B talk as if on one bridge
   Docker machine B ───┘
```

Connects containers running on **different** Docker hosts. Used by Docker Swarm and
cluster setups. Not something you set up on one laptop.

---

## 4. ipvlan

You decide the container's IP addresses yourself instead of letting Docker hand them out.
For people who need exact control over IP ranges. Lots of configuration, advanced.

---

## 5. macvlan

```text
   Wi-Fi router
   ├── your laptop        (MAC aa:bb..., IP 192.168.1.10)
   ├── your phone         (MAC cc:dd..., IP 192.168.1.11)
   └── container          (MAC ee:ff..., IP 192.168.1.12)   ← looks like a real device
```

The container gets its **own MAC address** and its own IP from your router, as if you
plugged a new physical computer into the network. Needs gateway, interface and other
settings. Advanced, but it's how you make a container appear as a device on your LAN.

---

## Remember

| Mode | Isolation | Internet | Use it for |
|---|---|---|---|
| user-defined bridge | ✅ | ✅ via your laptop | **real apps** |
| bridge (default) | partial | ✅ | quick tests |
| host | ❌ | ✅ as your laptop | rare, Linux only |
| none | total | ❌ | sealed-off jobs |
| overlay | ✅ | ✅ | multi-machine clusters |
| ipvlan / macvlan | ✅ | ✅ | custom IP / "be a real device" |

> **If someone asks in an interview:** "Which Docker network modes exist?" bridge (default
> and user-defined), host, none, overlay, ipvlan and macvlan. Day to day you use a
> user-defined bridge. `host` drops isolation and skips port mapping. `none` disables
> networking entirely. overlay spans multiple hosts, and macvlan makes a container look like
> a physical device on the LAN.
