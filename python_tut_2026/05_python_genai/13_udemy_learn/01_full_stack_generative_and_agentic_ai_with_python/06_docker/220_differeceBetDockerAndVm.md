# Docker vs Virtual Machines

Two fixes for "same environment for everyone": a **virtual machine** ships a whole
operating system, Docker ships a **slice** of one. The difference is the **kernel**. A VM
brings its own, a container **borrows yours**. That one fact is why Docker is light.

---

## Topic at a glance

```text
        Virtual machine                      Docker
            \                                  /
  hypervisor ──\              Docker engine ──/
                \                            /
  own kernel each ──\      shared host kernel
                      ►   SAME ENV, TWO WAYS
  30–40 GB, slow ────/      MBs, seconds ──────\
                    /                            \
  4 GB laptop dies ─/      kernel must match ─────\
            /                                       \
        Downsides                              Docker's catch
```

---

## VM in plain words

A **virtual machine** is a fake computer inside your real one. The **hypervisor**
(VirtualBox / VMware) fakes the hardware, and you install a **complete OS** on it. It
boots, has its own files and kernel, and thinks it's a real machine.

| Question | Answer |
|---|---|
| Is a VM "code"? | No. It's a **30–40 GB disk file** holding the whole OS + tools |
| How is it shared? | copy that giant file to every teammate |
| What does each teammate pay? | a **second full OS** running on their laptop: 2–4 GB RAM + CPU, all the time |
| Who can't run it? | anyone with a low-end (4 GB) laptop |
| What does Docker share instead? | only the **slice** you need, in MBs, on your own kernel |

---

## 🟢 Beginner — solution 1: a virtual machine

Install VMware / VirtualBox, create an Ubuntu VM, install the 10+ dev tools inside, share
the VM with the team. Everyone now runs the **same Ubuntu with the same tools**. Problem
solved. Badly.

| ✅ Works because | ❌ Hurts because |
|---|---|
| identical OS + tools for every dev | a VM is **30–40 GB**. Sharing it is painful |
| Mac, Windows, Linux hosts all run it | a full OS just to run a **text file** (your code) is overkill |
| | a dev with a **4 GB RAM** laptop can't run it at all |
| | eats CPU and RAM the whole time it's up |

---

## 🟡 Intermediate — how each one is built

```text
  VIRTUALIZATION                              DOCKERIZATION

  ┌─────────┬─────────┬─────────┐             ┌────────┬────────┬────────┐
  │ Ubuntu  │  Linux  │ Windows │  ◄ full OS  │ ubuntu │ alpine │busybox │  ◄ slice (image)
  │ +kernel │ +kernel │ +kernel │    each      │  cont. │  cont. │  cont. │    no own kernel
  ├─────────┴─────────┴─────────┤             ├────────┴────────┴────────┤
  │        HYPERVISOR           │  ◄ heavy    │      DOCKER ENGINE       │  ◄ light
  ├─────────────────────────────┤             ├──────────────────────────┤
  │   Host OS (Windows / Mac)   │             │  Host OS + KERNEL (shared)│
  ├─────────────────────────────┤             ├──────────────────────────┤
  │   Hardware: CPU, RAM, disk  │             │  Hardware: CPU, RAM, disk │
  └─────────────────────────────┘             └──────────────────────────┘
```

| Layer | Virtual machine | Docker |
|---|---|---|
| On top of the host OS | **hypervisor** (VMware, VirtualBox) | **Docker engine** |
| What runs on it | **full operating systems**, each with its own kernel | **containers**, each from an **image** |
| Kernel | one per VM | **one, the host's**, shared by all containers |
| Size | 5–10 GB per OS, 30–40 GB per VM | **MBs** per image |
| Hardware access | each VM talks to virtual hardware | containers use the host kernel directly |
| Sharing | copy a huge disk file | share or **publish the image**; anyone runs it |

> **Key idea:** a container is **not** an operating system. It's an **environment**: the
> files and tools of an OS, running on *your* kernel. That's why it's small.

### What goes in an image

MongoDB, Redis, Postgres, Node.js, Python, your app. Anyone with Docker engine runs the
same image: you, your teammate, the production server. One command, same environment.

---

## 🔴 Expert — proof on a Mac, and the catch

### The demo

```bash
uname                          # Darwin         ← macOS host
docker run -it ubuntu          # pulls ~28 MB, drops you into a shell
```

```text
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
...
root@3f2a9c1b7d4e:/#            ← you are now INSIDE an Ubuntu container
```

```bash
uname                          # Linux          ← not your Mac anymore
ls                             # bin boot dev etc home ... ← not your files
cd home && ls
# Ctrl+D                       # exit → back on macOS
```

| Image | Size | What it is |
|---|---|---|
| `ubuntu` | ~28 MB | Ubuntu userland |
| `alpine` | ~5 MB | tiny Linux, popular base image |
| `busybox` | ~1 MB | just the core Unix tools (`ls`, `ping`…) |

```bash
docker run -it busybox         # then: ping google.com
docker run -it alpine
```

Three different Linux environments, each in seconds, each a few MB. `-it` means
interactive terminal (covered in the CLI lecture).

### The catch: the kernel must match

| Host kernel | Can run |
|---|---|
| Linux | Linux containers |
| Windows | Windows containers (and Linux containers via Windows' built-in Linux support) |
| macOS | Linux containers (Docker Desktop runs a small hidden Linux VM to supply the kernel) |

A container **built for Windows** won't run on Mac or Linux. In practice this rarely bites:
almost everything is built as a Linux container and every dev platform can run those.

### Trade-off in one table

| | Virtual machine | Docker |
|---|---|---|
| Isolation | strongest: own kernel | process-level: shared kernel |
| Startup | minutes | seconds |
| Footprint | GBs | MBs |
| Run a different kernel | ✅ | ❌ |
| Share with the team / publish | hard | `docker push`, done |

---

## Gotchas & best practices

- **"Lightweight" has a reason.** Say *why*: no hypervisor, no second kernel, just a slice
  of userland on the host kernel.
- **A container is not a VM.** Don't expect a full OS inside. Many features are missing on
  purpose.
- **Docker engine is the only install.** Once it's there, every image "just runs".
- **Kernel compatibility is the one real limit.** Build Linux images and it disappears.
- **Next:** install Docker and learn the basic CLI.

> **Interview angle:** *"Why is Docker lighter than a VM?"* A VM runs a full guest OS with
> its own kernel on top of a hypervisor. A container shares the host kernel and packages
> only the userland it needs, so images are megabytes, start in seconds, and are trivial
> to share. The cost is weaker isolation and the need for a compatible host kernel.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Virtualization** | hypervisor runs full guest operating systems, each with its own kernel |
| **Hypervisor** | VMware / VirtualBox layer that hosts VMs; heavy |
| **Dockerization** | lightweight virtualization: containers share the host kernel |
| **Docker engine** | the one thing you install; runs containers |
| **Image** | a slice of an OS plus tools: the shareable template |
| **Container** | a running instance of an image |
| **Kernel rule** | containers must match the host kernel type (Linux images almost everywhere) |
| **`docker run -it ubuntu`** | pull a ~28 MB image and drop into an Ubuntu shell |
